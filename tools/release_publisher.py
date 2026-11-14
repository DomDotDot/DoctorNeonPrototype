#!/usr/bin/env python3
"""
Ren'Py GitHub Release Publisher for The Brightest Neon: Semitone Resonance.

Features:
- Auto-moves fresh DoctorNeonPrototype-*-dists folders into ../DrNeonVersions/.
- Lists *-dists folders sorted newest-first by semantic version & modification time.
- Auto-parses version, channel (early/stable/bt), tag, title, pre-release flag, and changelog.
- Manages Git tags (creates on HEAD and pushes to origin if missing; never alters working tree).
- Detects existing GitHub releases (including drafts), marks already-uploaded assets, and
  allows seamless resume/top-up or overwrite, plus optional DLC assets.zip attachment.
- Parallel multi-stream upload (1 MB chunks, 4 MB SO_SNDBUF, TCP_NODELAY) using explicit
  Content-Length via http.client.HTTPSConnection to bypass the ~1 MB/s browser upload bottleneck.
- Draft-then-publish workflow so .github/workflows/update_cdn_hash.yml runs only after all
  archives finish uploading.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import ctypes
import http.client
import json
import mimetypes
import os
import queue
import re
import shutil
import socket
import ssl
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# ---------------------------------------------------------------------------
# Paths & Constants
# ---------------------------------------------------------------------------

TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
PROJECTS_DIR = PROJECT_ROOT.parent
VERSIONS_DIR = PROJECTS_DIR / "DrNeonVersions"
ICON_PATH = PROJECT_ROOT / "icon.ico"

DEFAULT_REPO = "DomDotDot/DoctorNeonPrototype"
USER_AGENT = "DoctorNeon-ReleasePublisher/1.0"
GITHUB_API_VERSION = "2022-11-28"

CHUNK_SIZE = 1024 * 1024          # 1 MB streaming chunks
SOCKET_SNDBUF = 4 * 1024 * 1024   # 4 MB TCP send buffer
CONNECT_TIMEOUT = 30
UPLOAD_TIMEOUT = 180
MAX_RETRIES = 3

ARCHIVE_EXTENSIONS = (".zip", ".tar.bz2", ".tar.gz", ".7z", ".exe", ".dmg", ".apk", ".aab")

DIST_FOLDER_RE = re.compile(
    r"^DoctorNeonPrototype-(?P<version>.+?)(?:-(?P<channel>early(?:-test)?|stable|bt|beta|alpha|test))?-dists$",
    re.IGNORECASE,
)
GENERIC_DIST_RE = re.compile(
    r"^(?P<name>.+?)-(?P<version>\d+(?:\.\d+)+[a-zA-Z0-9_]*)(?:-(?P<channel>early(?:-test)?|stable|bt|beta|alpha|test))?-dists$",
    re.IGNORECASE,
)
GITHUB_REPO_RE = re.compile(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+?)(?:\.git)?/?$")

CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


# ---------------------------------------------------------------------------
# Formatting Utilities
# ---------------------------------------------------------------------------

def format_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} Б"
    if num_bytes < 1024 ** 2:
        return f"{num_bytes / 1024:.1f} КБ"
    if num_bytes < 1024 ** 3:
        return f"{num_bytes / (1024 ** 2):.1f} МБ"
    return f"{num_bytes / (1024 ** 3):.2f} ГБ"


def format_eta(seconds: Optional[float]) -> str:
    if seconds is None or seconds < 0 or seconds > 86400 * 7:
        return "--:--"
    total = int(seconds)
    mins, secs = divmod(total, 60)
    hours, mins = divmod(mins, 60)
    if hours > 0:
        return f"{hours}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def version_sort_key(version_str: str) -> tuple:
    """Parse version like '0.8.15' or '0.7.0r' into a comparable tuple."""
    parts = re.split(r"[._-]", version_str.strip().lstrip("vV"))
    parsed: list[tuple[int, int, str]] = []
    has_numeric = False
    for part in parts:
        m = re.match(r"^(\d+)([a-zA-Z]*)$", part)
        if m:
            has_numeric = True
            parsed.append((1, int(m.group(1)), m.group(2).lower()))
        else:
            parsed.append((0, 0, part.lower()))
    return (1 if has_numeric else 0, tuple(parsed))


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class ArchiveItem:
    name: str
    path: Path
    size: int
    is_dlc: bool = False
    selected: bool = True
    remote_asset_id: Optional[int] = None
    remote_size: Optional[int] = None
    remote_url: Optional[str] = None
    status_text: str = "Готов к загрузке"
    progress: float = 0.0
    uploaded_bytes: int = 0
    speed_mbps: float = 0.0
    eta_sec: Optional[float] = None
    state: str = "idle"  # idle | queued | uploading | done | error | skipped


@dataclass
class ParsedDistMetadata:
    folder: Path
    version: str
    channel: str
    tag: str
    title: str
    prerelease: bool


# ---------------------------------------------------------------------------
# Git Helper (Tags, Repo Slug, Credentials)
# ---------------------------------------------------------------------------

class GitHelper:
    def __init__(self, repo_dir: Path = PROJECT_ROOT) -> None:
        self.repo_dir = repo_dir

    def _run_git(self, args: list[str], stdin_text: Optional[str] = None, check: bool = True) -> subprocess.CompletedProcess[str]:
        kwargs: dict[str, Any] = {
            "cwd": str(self.repo_dir),
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
            "capture_output": True,
        }
        if stdin_text is not None:
            kwargs["input"] = stdin_text
        if os.name == "nt":
            kwargs["creationflags"] = CREATE_NO_WINDOW
        proc = subprocess.run(["git", *args], **kwargs)
        if check and proc.returncode != 0:
            err = proc.stderr.strip() or proc.stdout.strip() or f"exit code {proc.returncode}"
            raise RuntimeError(f"git {' '.join(args)}: {err}")
        return proc

    def get_repo_slug(self) -> str:
        proc = self._run_git(["remote", "get-url", "origin"], check=False)
        if proc.returncode == 0:
            url = proc.stdout.strip()
            m = GITHUB_REPO_RE.search(url)
            if m:
                return f"{m.group('owner')}/{m.group('repo')}"
        return DEFAULT_REPO

    def get_token(self) -> tuple[str, str]:
        """Return (token, source_label). Checks env, .env, then git credential fill."""
        for env_key in ("GITHUB_TOKEN", "GH_TOKEN"):
            val = os.environ.get(env_key, "").strip()
            if val:
                return val, f"env:{env_key}"

        for env_path in (self.repo_dir / ".env", TOOLS_DIR / ".env"):
            if env_path.is_file():
                try:
                    for line in env_path.read_text(encoding="utf-8").splitlines():
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k in ("GITHUB_TOKEN", "GH_TOKEN") and v:
                            return v, f"file:{env_path.name}"
                except OSError:
                    pass

        proc = self._run_git(
            ["credential", "fill"],
            stdin_text="protocol=https\nhost=github.com\n\n",
            check=False,
        )
        if proc.returncode == 0:
            for line in proc.stdout.splitlines():
                if line.startswith("password="):
                    token = line.split("=", 1)[1].strip()
                    if token:
                        return token, "Git Credential Manager"
        return "", "не найден"

    def get_head_info(self) -> dict[str, str]:
        branch_proc = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"], check=False)
        commit_proc = self._run_git(["log", "-1", "--format=%h|%s"], check=False)
        branch = branch_proc.stdout.strip() if branch_proc.returncode == 0 else "unknown"
        short_hash, subject = "?", ""
        if commit_proc.returncode == 0 and "|" in commit_proc.stdout:
            short_hash, subject = commit_proc.stdout.strip().split("|", 1)
        return {"branch": branch, "hash": short_hash, "subject": subject}

    def get_tags(self) -> list[str]:
        proc = self._run_git(["tag", "--sort=-creatordate"], check=False)
        if proc.returncode != 0:
            return []
        tags = [t.strip() for t in proc.stdout.splitlines() if t.strip()]
        return tags

    def tag_exists_local(self, tag: str) -> bool:
        proc = self._run_git(["rev-parse", "-q", "--verify", f"refs/tags/{tag}"], check=False)
        return proc.returncode == 0

    def tag_exists_remote(self, tag: str) -> bool:
        proc = self._run_git(["ls-remote", "--tags", "origin", f"refs/tags/{tag}"], check=False)
        return proc.returncode == 0 and bool(proc.stdout.strip())

    def ensure_tag_pushed(self, tag: str, log_cb: Callable[[str], None]) -> None:
        if not self.tag_exists_local(tag):
            log_cb(f"Создание локального Git-тега '{tag}' на текущем HEAD...")
            self._run_git(["tag", tag])
        else:
            log_cb(f"Локальный тег '{tag}' уже существует.")

        if not self.tag_exists_remote(tag):
            log_cb(f"Отправка тега '{tag}' в origin...")
            self._run_git(["push", "origin", f"refs/tags/{tag}"])
            log_cb(f"Тег '{tag}' успешно отправлен на GitHub.")
        else:
            log_cb(f"Тег '{tag}' уже присутствует на origin.")

    def get_previous_tag(self, current_tag: str, all_tags: Optional[list[str]] = None) -> Optional[str]:
        tags = all_tags if all_tags is not None else self.get_tags()
        if not tags:
            return None
        if current_tag in tags:
            idx = tags.index(current_tag)
            if idx + 1 < len(tags):
                return tags[idx + 1]
            return None
        return tags[0]

    def get_commits_between(self, prev_tag: Optional[str], target_ref: str = "HEAD", limit: int = 40) -> list[str]:
        ref_range = f"{prev_tag}..{target_ref}" if prev_tag else target_ref
        proc = self._run_git(["log", ref_range, f"-n{limit}", "--format=- %s (`%h`)"], check=False)
        if proc.returncode != 0:
            return []
        return [line for line in proc.stdout.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# Distribution Scanner & Metadata Parser
# ---------------------------------------------------------------------------

class DistManager:
    def __init__(
        self,
        project_root: Path = PROJECT_ROOT,
        projects_dir: Path = PROJECTS_DIR,
        versions_dir: Path = VERSIONS_DIR,
    ) -> None:
        self.project_root = project_root
        self.projects_dir = projects_dir
        self.versions_dir = versions_dir

    def auto_move_fresh_dists(self, log_cb: Optional[Callable[[str], None]] = None) -> list[Path]:
        """Move newly built DoctorNeonPrototype-*-dists from ../ into ../DrNeonVersions/."""
        moved: list[Path] = []
        if not self.projects_dir.is_dir():
            return moved

        self.versions_dir.mkdir(parents=True, exist_ok=True)
        for entry in self.projects_dir.iterdir():
            if not entry.is_dir():
                continue
            name_lower = entry.name.lower()
            if not (name_lower.startswith("doctorneonprototype-") and name_lower.endswith("-dists")):
                continue
            dest = self.versions_dir / entry.name
            if dest.exists():
                if log_cb:
                    log_cb(f"⚠ Папка '{entry.name}' найдена в {self.projects_dir.name}, но уже есть в DrNeonVersions — оставлена на месте.")
                continue
            try:
                shutil.move(str(entry), str(dest))
                moved.append(dest)
                if log_cb:
                    log_cb(f"📦 Перенесена свежая сборка '{entry.name}' -> DrNeonVersions/")
            except OSError as exc:
                if log_cb:
                    log_cb(f"⚠ Не удалось перенести '{entry.name}': {exc}")
        return moved

    def _folder_sort_key(self, folder: Path) -> tuple:
        meta = self.parse_folder_metadata(folder, existing_tags=[])
        vkey = version_sort_key(meta.version)
        channel_order = {
            "stable": 5,
            "": 4,
            "early": 3,
            "early-test": 2,
            "bt": 1,
            "beta": 1,
            "alpha": 1,
            "test": 0,
        }.get(meta.channel.lower(), 1)
        try:
            mtime = folder.stat().st_mtime
        except OSError:
            mtime = 0.0
        return (vkey, channel_order, mtime)

    def list_dist_folders(self) -> list[Path]:
        candidates: list[Path] = []
        if self.versions_dir.is_dir():
            for entry in self.versions_dir.iterdir():
                if entry.is_dir() and entry.name.lower().endswith("-dists"):
                    candidates.append(entry)
        if self.projects_dir.is_dir():
            for entry in self.projects_dir.iterdir():
                if (
                    entry.is_dir()
                    and entry.name.lower().startswith("doctorneonprototype-")
                    and entry.name.lower().endswith("-dists")
                    and entry not in candidates
                ):
                    candidates.append(entry)
        candidates.sort(key=self._folder_sort_key, reverse=True)
        return candidates

    def parse_folder_metadata(self, folder: Path, existing_tags: list[str]) -> ParsedDistMetadata:
        name = folder.name
        version = name
        channel = ""

        m = DIST_FOLDER_RE.match(name) or GENERIC_DIST_RE.match(name)
        if m:
            version = m.group("version").strip()
            channel = (m.group("channel") or "").strip().lower()
        elif name.lower().endswith("-dists"):
            version = name[:-6]

        # Match existing tag style (e.g. v0.8.15 or v0.6.10-early)
        has_digits = bool(re.match(r"^\d", version))
        base_tag = f"v{version}" if has_digits else version
        channel_tag = f"{base_tag}-{channel}" if channel else base_tag

        if base_tag in existing_tags:
            tag = base_tag
        elif channel_tag in existing_tags:
            tag = channel_tag
        else:
            tag = base_tag

        if channel:
            prefix = f"[{channel.upper()}] "
            prerelease = channel != "stable"
        else:
            prefix = ""
            prerelease = True if ("early" in version.lower() or "bt" in version.lower() or "prototype" in version.lower()) else False

        title = f"{prefix}{tag}"
        return ParsedDistMetadata(
            folder=folder,
            version=version,
            channel=channel,
            tag=tag,
            title=title,
            prerelease=prerelease,
        )

    def scan_archives(self, folder: Path) -> list[ArchiveItem]:
        items: list[ArchiveItem] = []
        if folder.is_dir():
            files = [
                f for f in folder.iterdir()
                if f.is_file() and f.name.lower().endswith(ARCHIVE_EXTENSIONS)
            ]
            files.sort(key=lambda p: p.name.lower())
            for f in files:
                items.append(
                    ArchiveItem(
                        name=f.name,
                        path=f,
                        size=f.stat().st_size,
                        is_dlc=False,
                        selected=True,
                    )
                )

        dlc_path = self.project_root / "assets.zip"
        if dlc_path.is_file():
            items.append(
                ArchiveItem(
                    name="assets.zip",
                    path=dlc_path,
                    size=dlc_path.stat().st_size,
                    is_dlc=True,
                    selected=False,
                    status_text="DLC-архив из корня проекта (опционально)",
                )
            )
        return items


# ---------------------------------------------------------------------------
# High-Speed GitHub Release Client (Direct HTTPSConnection Streaming)
# ---------------------------------------------------------------------------

class TunedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPSConnection with enlarged SO_SNDBUF and TCP_NODELAY for high-speed uploads."""

    def connect(self) -> None:
        super().connect()
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SOCKET_SNDBUF)
            self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except OSError:
            pass


class UploadCancelledError(Exception):
    pass


class GitHubReleaseClient:
    def __init__(self, repo: str, token: str) -> None:
        self.repo = repo
        self.token = token
        self._ssl_ctx = ssl.create_default_context()
        self._active_conns_lock = threading.Lock()
        self._active_conns: set[TunedHTTPSConnection] = set()

    def abort_active_uploads(self) -> None:
        with self._active_conns_lock:
            conns = list(self._active_conns)
        for conn in conns:
            try:
                if conn.sock is not None:
                    conn.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                conn.close()
            except Exception:
                pass

    def _api_request(self, method: str, path: str, payload: Optional[dict[str, Any]] = None) -> Any:
        url = path if path.startswith("https://") else f"https://api.github.com{path}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
            "User-Agent": USER_AGENT,
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        data: Optional[bytes] = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json; charset=utf-8"

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, context=self._ssl_ctx, timeout=CONNECT_TIMEOUT) as resp:
                raw = resp.read()
                if not raw:
                    return None
                return json.loads(raw.decode("utf-8"))
        except urllib.error.HTTPError as err:
            body_text = err.read().decode("utf-8", errors="replace")
            try:
                err_json = json.loads(body_text)
                msg = err_json.get("message") or body_text
                errors = err_json.get("errors")
                if errors:
                    msg = f"{msg} ({errors})"
            except json.JSONDecodeError:
                msg = body_text or str(err)
            raise RuntimeError(f"GitHub API {err.code} [{method} {path}]: {msg}") from err

    def validate_auth(self) -> dict[str, Any]:
        if not self.token:
            raise RuntimeError("Токен GitHub не найден. Настройте Git Credential Manager или GITHUB_TOKEN.")
        return self._api_request("GET", "/user")

    def find_release_by_tag(self, tag: str) -> Optional[dict[str, Any]]:
        """Find published OR draft release matching tag."""
        releases = self._api_request("GET", f"/repos/{self.repo}/releases?per_page=40")
        if isinstance(releases, list):
            for rel in releases:
                if rel.get("tag_name") == tag:
                    return rel
        # Fallback for older tags outside first 40 releases
        encoded_tag = urllib.parse.quote(tag, safe="")
        try:
            return self._api_request("GET", f"/repos/{self.repo}/releases/tags/{encoded_tag}")
        except RuntimeError as exc:
            if "GitHub API 404" in str(exc):
                return None
            raise

    def get_release(self, release_id: int) -> dict[str, Any]:
        return self._api_request("GET", f"/repos/{self.repo}/releases/{release_id}")

    def create_release(
        self,
        tag_name: str,
        name: str,
        body: str,
        prerelease: bool,
        draft: bool,
    ) -> dict[str, Any]:
        payload = {
            "tag_name": tag_name,
            "name": name,
            "body": body,
            "prerelease": prerelease,
            "draft": draft,
        }
        return self._api_request("POST", f"/repos/{self.repo}/releases", payload)

    def update_release(
        self,
        release_id: int,
        name: Optional[str] = None,
        body: Optional[str] = None,
        prerelease: Optional[bool] = None,
        draft: Optional[bool] = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if body is not None:
            payload["body"] = body
        if prerelease is not None:
            payload["prerelease"] = prerelease
        if draft is not None:
            payload["draft"] = draft
        return self._api_request("PATCH", f"/repos/{self.repo}/releases/{release_id}", payload)

    def list_assets(self, release_id: int) -> list[dict[str, Any]]:
        res = self._api_request("GET", f"/repos/{self.repo}/releases/{release_id}/assets?per_page=100")
        return res if isinstance(res, list) else []

    def delete_asset(self, asset_id: int) -> None:
        self._api_request("DELETE", f"/repos/{self.repo}/releases/assets/{asset_id}")

    def _delete_asset_by_name_if_exists(self, release_id: int, filename: str) -> bool:
        for asset in self.list_assets(release_id):
            if asset.get("name") == filename:
                self.delete_asset(int(asset["id"]))
                return True
        return False

    def upload_asset(
        self,
        release_id: int,
        upload_url_template: str,
        file_path: Path,
        asset_name: str,
        cancel_event: threading.Event,
        progress_cb: Callable[[int, float, Optional[float]], None],
        log_cb: Callable[[str], None],
    ) -> dict[str, Any]:
        """
        Stream file in 1 MB chunks with explicit Content-Length over TunedHTTPSConnection.
        Retries up to MAX_RETRIES times on transient failures, cleaning partial remote assets.
        """
        base_upload_url = upload_url_template.split("{", 1)[0]
        parsed = urllib.parse.urlparse(base_upload_url)
        host = parsed.netloc
        encoded_name = urllib.parse.quote(asset_name, safe="")
        request_path = f"{parsed.path}?name={encoded_name}"

        file_size = file_path.stat().st_size
        content_type = mimetypes.guess_type(asset_name)[0] or "application/octet-stream"

        last_error: Optional[Exception] = None
        for attempt in range(1, MAX_RETRIES + 1):
            if cancel_event.is_set():
                raise UploadCancelledError("Загрузка отменена пользователем.")

            conn: Optional[TunedHTTPSConnection] = None
            try:
                # Ensure no colliding/partial asset exists before attempting upload
                if attempt > 1:
                    if self._delete_asset_by_name_if_exists(release_id, asset_name):
                        log_cb(f"[{asset_name}] Удалён незавершённый ассет перед повтором #{attempt}.")

                conn = TunedHTTPSConnection(host, timeout=UPLOAD_TIMEOUT, context=self._ssl_ctx)
                with self._active_conns_lock:
                    self._active_conns.add(conn)
                conn.connect()
                conn.putrequest("POST", request_path, skip_host=False, skip_accept_encoding=True)
                conn.putheader("Authorization", f"Bearer {self.token}")
                conn.putheader("Accept", "application/vnd.github+json")
                conn.putheader("X-GitHub-Api-Version", GITHUB_API_VERSION)
                conn.putheader("User-Agent", USER_AGENT)
                conn.putheader("Content-Type", content_type)
                conn.putheader("Content-Length", str(file_size))
                conn.endheaders()

                sent_bytes = 0
                start_ts = time.monotonic()
                last_tick_ts = start_ts
                last_tick_bytes = 0
                ema_speed = 0.0

                with file_path.open("rb") as fh:
                    while True:
                        if cancel_event.is_set():
                            raise UploadCancelledError("Загрузка отменена пользователем.")
                        chunk = fh.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        conn.send(chunk)
                        sent_bytes += len(chunk)

                        now = time.monotonic()
                        dt = now - last_tick_ts
                        if dt >= 0.15 or sent_bytes == file_size:
                            inst_speed = ((sent_bytes - last_tick_bytes) / (1024 * 1024)) / max(dt, 1e-3)
                            ema_speed = inst_speed if ema_speed == 0.0 else (0.35 * inst_speed + 0.65 * ema_speed)
                            remaining_mb = (file_size - sent_bytes) / (1024 * 1024)
                            eta = remaining_mb / ema_speed if ema_speed > 0.01 else None
                            progress_cb(sent_bytes, ema_speed, eta)
                            last_tick_ts = now
                            last_tick_bytes = sent_bytes

                resp = conn.getresponse()
                resp_raw = resp.read().decode("utf-8", errors="replace")
                if 200 <= resp.status < 300:
                    avg_speed = (file_size / (1024 * 1024)) / max(time.monotonic() - start_ts, 0.01)
                    progress_cb(file_size, avg_speed, 0.0)
                    return json.loads(resp_raw)

                if resp.status == 422 and "already_exists" in resp_raw:
                    log_cb(f"[{asset_name}] Обнаружен существующий ассет (422) — удаляем и перезагружаем...")
                    self._delete_asset_by_name_if_exists(release_id, asset_name)
                    raise RuntimeError("Asset conflict (422 already_exists)")

                raise RuntimeError(f"HTTP {resp.status}: {resp_raw[:300]}")

            except UploadCancelledError:
                if conn is not None:
                    try:
                        conn.close()
                    except Exception:
                        pass
                raise
            except Exception as exc:
                last_error = exc
                if attempt < MAX_RETRIES and not cancel_event.is_set():
                    backoff = 2 * attempt
                    log_cb(f"⚠ [{asset_name}] Сбой попытки #{attempt}: {exc}. Повтор через {backoff} сек...")
                    for _ in range(backoff * 10):
                        if cancel_event.is_set():
                            raise UploadCancelledError("Загрузка отменена пользователем.")
                        time.sleep(0.1)
                else:
                    raise RuntimeError(f"Не удалось загрузить {asset_name} после {MAX_RETRIES} попыток: {last_error}") from exc
            finally:
                if conn is not None:
                    with self._active_conns_lock:
                        self._active_conns.discard(conn)
                    try:
                        conn.close()
                    except Exception:
                        pass

        raise RuntimeError(f"Не удалось загрузить {asset_name}: {last_error}")


# ---------------------------------------------------------------------------
# Dark Neon Tkinter GUI
# ---------------------------------------------------------------------------

COLORS = {
    "bg": "#10121a",
    "card": "#181b28",
    "card_alt": "#1f2334",
    "input": "#12141f",
    "border": "#2d334d",
    "fg": "#eef1fb",
    "muted": "#8c96b8",
    "accent": "#00e5ff",
    "accent_hover": "#38ecff",
    "purple": "#7c4dff",
    "success": "#2ee59d",
    "warning": "#ffb74d",
    "danger": "#ff5c7c",
}


class ReleasePublisherGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.git = GitHelper(PROJECT_ROOT)
        self.dist_mgr = DistManager(PROJECT_ROOT, PROJECTS_DIR, VERSIONS_DIR)

        self.repo_slug = self.git.get_repo_slug()
        self.token, self.token_source = self.git.get_token()
        self.client: Optional[GitHubReleaseClient] = (
            GitHubReleaseClient(self.repo_slug, self.token) if self.token else None
        )

        self.dist_folders: list[Path] = []
        self.all_tags: list[str] = []
        self.archives: list[ArchiveItem] = []
        self.current_release: Optional[dict[str, Any]] = None
        self.release_lookup_seq = 0
        self.is_uploading = False
        self.cancel_event = threading.Event()
        self.ui_queue: queue.Queue[Callable[[], None]] = queue.Queue()

        self.archive_rows: list[dict[str, Any]] = []

        self._setup_window()
        self._setup_styles()
        self._build_ui()
        self._poll_ui_queue()

        # Initial load after window renders
        self.root.after(60, self._initial_refresh)

    def _setup_window(self) -> None:
        self.root.title("Semitone Resonance — Сборщик релизов GitHub")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(880, 700)

        width, height = 1040, 820
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max(0, (sw - width) // 2)
        y = max(0, (sh - height) // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        if ICON_PATH.is_file():
            try:
                self.root.iconbitmap(str(ICON_PATH))
            except tk.TclError:
                pass

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_styles(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.root.option_add("*TCombobox*Listbox.background", COLORS["input"])
        self.root.option_add("*TCombobox*Listbox.foreground", COLORS["fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", COLORS["purple"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")

        style.configure(".", background=COLORS["bg"], foreground=COLORS["fg"], font=("Segoe UI", 10))
        style.configure("Card.TFrame", background=COLORS["card"])
        style.configure("CardAlt.TFrame", background=COLORS["card_alt"])
        style.configure("Header.TLabel", background=COLORS["bg"], foreground=COLORS["accent"], font=("Segoe UI", 14, "bold"))
        style.configure("Section.TLabel", background=COLORS["card"], foreground=COLORS["accent"], font=("Segoe UI", 10, "bold"))
        style.configure("Card.TLabel", background=COLORS["card"], foreground=COLORS["fg"], font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=COLORS["card"], foreground=COLORS["muted"], font=("Segoe UI", 9))
        style.configure("Row.TLabel", background=COLORS["card_alt"], foreground=COLORS["fg"], font=("Segoe UI", 10))
        style.configure("RowMuted.TLabel", background=COLORS["card_alt"], foreground=COLORS["muted"], font=("Segoe UI", 9))

        style.configure(
            "TEntry",
            fieldbackground=COLORS["input"],
            foreground=COLORS["fg"],
            insertcolor=COLORS["accent"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
            padding=5,
        )
        style.configure(
            "TCombobox",
            fieldbackground=COLORS["input"],
            background=COLORS["card_alt"],
            foreground=COLORS["fg"],
            arrowcolor=COLORS["accent"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
            padding=5,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", COLORS["input"])],
            foreground=[("readonly", COLORS["fg"])],
            selectbackground=[("readonly", COLORS["input"])],
            selectforeground=[("readonly", COLORS["fg"])],
        )

        style.configure(
            "TCheckbutton",
            background=COLORS["card"],
            foreground=COLORS["fg"],
            font=("Segoe UI", 10),
        )
        style.map(
            "TCheckbutton",
            background=[("active", COLORS["card"])],
            foreground=[("disabled", COLORS["muted"])],
        )
        style.configure(
            "Row.TCheckbutton",
            background=COLORS["card_alt"],
            foreground=COLORS["fg"],
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Row.TCheckbutton",
            background=[("active", COLORS["card_alt"])],
            foreground=[("disabled", COLORS["muted"])],
        )

        style.configure(
            "Secondary.TButton",
            background=COLORS["card_alt"],
            foreground=COLORS["fg"],
            bordercolor=COLORS["border"],
            padding=(10, 5),
            font=("Segoe UI", 9),
        )
        style.map(
            "Secondary.TButton",
            background=[("active", COLORS["border"]), ("pressed", COLORS["purple"])],
        )

        style.configure(
            "Primary.TButton",
            background=COLORS["purple"],
            foreground="#ffffff",
            bordercolor=COLORS["purple"],
            padding=(16, 8),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#916bff"), ("disabled", COLORS["card_alt"])],
            foreground=[("disabled", COLORS["muted"])],
        )

        style.configure(
            "Danger.TButton",
            background="#4b1f2d",
            foreground=COLORS["danger"],
            bordercolor=COLORS["danger"],
            padding=(12, 8),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#6a273c"), ("disabled", COLORS["card_alt"])],
            foreground=[("disabled", COLORS["muted"])],
        )

        style.configure(
            "Neon.Horizontal.TProgressbar",
            troughcolor=COLORS["input"],
            background=COLORS["accent"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["accent"],
            darkcolor=COLORS["accent"],
            thickness=8,
        )
        style.configure(
            "Done.Horizontal.TProgressbar",
            troughcolor=COLORS["input"],
            background=COLORS["success"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["success"],
            darkcolor=COLORS["success"],
            thickness=8,
        )

    def _build_ui(self) -> None:
        container = tk.Frame(self.root, bg=COLORS["bg"], padx=14, pady=12)
        container.pack(fill=tk.BOTH, expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(2, weight=3)  # Release metadata + description
        container.rowconfigure(3, weight=2)  # Assets list
        container.rowconfigure(4, weight=1)  # Log box

        # --- Top Header Bar ---
        header = tk.Frame(container, bg=COLORS["bg"])
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.columnconfigure(1, weight=1)

        ttk.Label(header, text="⚡ GitHub Release Publisher", style="Header.TLabel").grid(row=0, column=0, sticky="w")

        self.repo_label = tk.Label(
            header,
            text=f"  •  {self.repo_slug}",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            cursor="hand2",
        )
        self.repo_label.grid(row=0, column=1, sticky="w", padx=(6, 0))
        self.repo_label.bind("<Button-1>", lambda _e: webbrowser.open(f"https://github.com/{self.repo_slug}/releases"))

        right_badges = tk.Frame(header, bg=COLORS["bg"])
        right_badges.grid(row=0, column=2, sticky="e")

        self.git_head_label = tk.Label(
            right_badges,
            text="Git: ...",
            bg=COLORS["card"],
            fg=COLORS["fg"],
            font=("Segoe UI", 9),
            padx=8,
            pady=3,
        )
        self.git_head_label.pack(side=tk.LEFT, padx=(0, 8))

        self.auth_btn = tk.Button(
            right_badges,
            text="🔑 Проверка токена...",
            bg=COLORS["card"],
            fg=COLORS["warning"],
            activebackground=COLORS["card_alt"],
            activeforeground=COLORS["fg"],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=3,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            command=self._prompt_token_dialog,
        )
        self.auth_btn.pack(side=tk.LEFT)

        # --- Section 1: Dist Folder Picker ---
        sec1 = self._make_card(container, row=1, pady=(0, 10))
        sec1.columnconfigure(1, weight=1)

        ttk.Label(sec1, text="1. Папка дистрибутивов (*-dists)", style="Section.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 6)
        )

        ttk.Label(sec1, text="Сборка:", style="Card.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 8))
        self.dist_var = tk.StringVar()
        self.dist_combo = ttk.Combobox(sec1, textvariable=self.dist_var, state="readonly")
        self.dist_combo.grid(row=1, column=1, sticky="ew", padx=(0, 8))
        self.dist_combo.bind("<<ComboboxSelected>>", lambda _e: self._on_dist_selected())

        ttk.Button(sec1, text="🔄 Обновить", style="Secondary.TButton", command=self._refresh_all).grid(
            row=1, column=2, padx=(0, 6)
        )
        ttk.Button(sec1, text="📁 Обзор...", style="Secondary.TButton", command=self._browse_dist_folder).grid(
            row=1, column=3, padx=(0, 6)
        )
        ttk.Button(sec1, text="📂 Открыть", style="Secondary.TButton", command=self._open_current_dist).grid(
            row=1, column=4
        )

        self.dist_path_label = ttk.Label(sec1, text="", style="Muted.TLabel")
        self.dist_path_label.grid(row=2, column=1, columnspan=4, sticky="w", pady=(4, 0))

        # --- Section 2: Release & Git Tag Settings ---
        sec2 = self._make_card(container, row=2, pady=(0, 10))
        sec2.columnconfigure(1, weight=1)
        sec2.columnconfigure(3, weight=1)
        sec2.rowconfigure(4, weight=1)

        header_row2 = tk.Frame(sec2, bg=COLORS["card"])
        header_row2.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 6))
        ttk.Label(header_row2, text="2. Параметры Git-тега и релиза", style="Section.TLabel").pack(side=tk.LEFT)
        self.release_status_badge = tk.Label(
            header_row2,
            text="Ожидание выбора папки...",
            bg=COLORS["card_alt"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=2,
        )
        self.release_status_badge.pack(side=tk.RIGHT)

        # Row 1: Tag + Release Title
        ttk.Label(sec2, text="Git-тег:", style="Card.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=3)
        tag_frame = tk.Frame(sec2, bg=COLORS["card"])
        tag_frame.grid(row=1, column=1, sticky="ew", padx=(0, 14), pady=3)
        tag_frame.columnconfigure(0, weight=1)

        self.tag_var = tk.StringVar()
        self.tag_combo = ttk.Combobox(tag_frame, textvariable=self.tag_var)
        self.tag_combo.grid(row=0, column=0, sticky="ew")
        self.tag_combo.bind("<<ComboboxSelected>>", lambda _e: self._on_tag_changed())
        self.tag_combo.bind("<FocusOut>", lambda _e: self._on_tag_changed())
        self.tag_combo.bind("<Return>", lambda _e: self._on_tag_changed())

        ttk.Button(tag_frame, text="🔍 Проверить", style="Secondary.TButton", command=self._on_tag_changed).grid(
            row=0, column=1, padx=(6, 0)
        )

        ttk.Label(sec2, text="Название:", style="Card.TLabel").grid(row=1, column=2, sticky="w", padx=(0, 8), pady=3)
        title_frame = tk.Frame(sec2, bg=COLORS["card"])
        title_frame.grid(row=1, column=3, sticky="ew", pady=3)
        title_frame.columnconfigure(0, weight=1)

        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(title_frame, textvariable=self.title_var)
        self.title_entry.grid(row=0, column=0, sticky="ew")

        for col_idx, prefix in enumerate(("[EARLY]", "[STABLE]", "[BT]"), start=1):
            ttk.Button(
                title_frame,
                text=prefix,
                style="Secondary.TButton",
                command=lambda p=prefix: self._apply_title_prefix(p),
            ).grid(row=0, column=col_idx, padx=(4, 0))

        # Row 2: Tag status + Options (Pre-release, Draft, Threads)
        self.git_tag_status_label = ttk.Label(sec2, text="", style="Muted.TLabel")
        self.git_tag_status_label.grid(row=2, column=1, sticky="w", pady=(0, 4))

        opts_frame = tk.Frame(sec2, bg=COLORS["card"])
        opts_frame.grid(row=2, column=2, columnspan=2, sticky="ew", pady=(0, 4))

        self.prerelease_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(opts_frame, text="Pre-release", variable=self.prerelease_var).pack(side=tk.LEFT, padx=(0, 14))

        self.draft_only_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opts_frame, text="Оставить черновиком (Draft)", variable=self.draft_only_var).pack(
            side=tk.LEFT, padx=(0, 14)
        )

        ttk.Label(opts_frame, text="Потоки:", style="Card.TLabel").pack(side=tk.LEFT, padx=(4, 4))
        self.threads_var = tk.StringVar(value="3")
        self.threads_combo = ttk.Combobox(
            opts_frame, textvariable=self.threads_var, values=("1", "2", "3", "4"), width=3, state="readonly"
        )
        self.threads_combo.pack(side=tk.LEFT)

        # Row 3: Description toolbar
        desc_hdr = tk.Frame(sec2, bg=COLORS["card"])
        desc_hdr.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(4, 4))
        ttk.Label(desc_hdr, text="Описание релиза (Markdown):", style="Card.TLabel").pack(side=tk.LEFT)
        ttk.Button(desc_hdr, text="📋 + Коммиты с прошлого тега", style="Secondary.TButton", command=self._append_git_commits).pack(
            side=tk.RIGHT, padx=(6, 0)
        )
        ttk.Button(desc_hdr, text="🔄 Авто-Changelog", style="Secondary.TButton", command=self._reset_changelog_body).pack(
            side=tk.RIGHT
        )

        # Row 4: Description text box
        desc_box_frame = tk.Frame(sec2, bg=COLORS["border"], bd=1)
        desc_box_frame.grid(row=4, column=0, columnspan=4, sticky="nsew")
        desc_box_frame.columnconfigure(0, weight=1)
        desc_box_frame.rowconfigure(0, weight=1)

        self.body_text = tk.Text(
            desc_box_frame,
            height=5,
            bg=COLORS["input"],
            fg=COLORS["fg"],
            insertbackground=COLORS["accent"],
            selectbackground=COLORS["purple"],
            relief=tk.FLAT,
            font=("Consolas", 9),
            wrap=tk.WORD,
            padx=8,
            pady=6,
        )
        self.body_text.grid(row=0, column=0, sticky="nsew")
        body_scroll = ttk.Scrollbar(desc_box_frame, orient=tk.VERTICAL, command=self.body_text.yview)
        body_scroll.grid(row=0, column=1, sticky="ns")
        self.body_text.configure(yscrollcommand=body_scroll.set)

        # --- Section 3: Assets List ---
        sec3 = self._make_card(container, row=3, pady=(0, 10))
        sec3.columnconfigure(0, weight=1)
        sec3.rowconfigure(1, weight=1)

        assets_hdr = tk.Frame(sec3, bg=COLORS["card"])
        assets_hdr.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(assets_hdr, text="3. Файлы для выгрузки (Assets)", style="Section.TLabel").pack(side=tk.LEFT)
        ttk.Button(assets_hdr, text="Снять всё", style="Secondary.TButton", command=lambda: self._select_all_assets(False)).pack(
            side=tk.RIGHT, padx=(6, 0)
        )
        ttk.Button(assets_hdr, text="Выбрать недостающие", style="Secondary.TButton", command=self._select_missing_assets).pack(
            side=tk.RIGHT, padx=(6, 0)
        )
        ttk.Button(assets_hdr, text="Выбрать все", style="Secondary.TButton", command=lambda: self._select_all_assets(True)).pack(
            side=tk.RIGHT
        )

        # Scrollable canvas for archive rows
        canvas_wrap = tk.Frame(sec3, bg=COLORS["card"])
        canvas_wrap.grid(row=1, column=0, sticky="nsew")
        canvas_wrap.columnconfigure(0, weight=1)
        canvas_wrap.rowconfigure(0, weight=1)

        self.assets_canvas = tk.Canvas(canvas_wrap, bg=COLORS["card"], highlightthickness=0, height=145)
        self.assets_canvas.grid(row=0, column=0, sticky="nsew")
        assets_scroll = ttk.Scrollbar(canvas_wrap, orient=tk.VERTICAL, command=self.assets_canvas.yview)
        assets_scroll.grid(row=0, column=1, sticky="ns")
        self.assets_canvas.configure(yscrollcommand=assets_scroll.set)

        self.assets_inner = tk.Frame(self.assets_canvas, bg=COLORS["card"])
        self.assets_window_id = self.assets_canvas.create_window((0, 0), window=self.assets_inner, anchor="nw")
        self.assets_inner.bind("<Configure>", lambda _e: self.assets_canvas.configure(scrollregion=self.assets_canvas.bbox("all")))
        self.assets_canvas.bind("<Configure>", lambda e: self.assets_canvas.itemconfigure(self.assets_window_id, width=e.width))
        self.assets_canvas.bind("<Enter>", lambda _e: self.assets_canvas.bind_all("<MouseWheel>", self._on_assets_mousewheel))
        self.assets_canvas.bind("<Leave>", lambda _e: self.assets_canvas.unbind_all("<MouseWheel>"))

        # --- Section 4: Log Console ---
        sec4 = self._make_card(container, row=4, pady=(0, 10))
        sec4.columnconfigure(0, weight=1)
        sec4.rowconfigure(1, weight=1)

        ttk.Label(sec4, text="4. Журнал операций", style="Section.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 4))
        log_wrap = tk.Frame(sec4, bg=COLORS["border"], bd=1)
        log_wrap.grid(row=1, column=0, sticky="nsew")
        log_wrap.columnconfigure(0, weight=1)
        log_wrap.rowconfigure(0, weight=1)

        self.log_text = tk.Text(
            log_wrap,
            height=5,
            bg=COLORS["input"],
            fg=COLORS["muted"],
            relief=tk.FLAT,
            font=("Consolas", 9),
            state=tk.DISABLED,
            wrap=tk.WORD,
            padx=8,
            pady=6,
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll = ttk.Scrollbar(log_wrap, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scroll.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=log_scroll.set)

        # --- Bottom Action Bar ---
        bottom = tk.Frame(container, bg=COLORS["bg"])
        bottom.grid(row=5, column=0, sticky="ew")
        bottom.columnconfigure(0, weight=1)

        self.total_status_label = tk.Label(
            bottom,
            text="Готов к работе",
            bg=COLORS["bg"],
            fg=COLORS["fg"],
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        )
        self.total_status_label.grid(row=0, column=0, sticky="ew", padx=(0, 12))

        self.open_gh_btn = ttk.Button(
            bottom,
            text="🌐 Открыть на GitHub",
            style="Secondary.TButton",
            command=self._open_release_in_browser,
        )
        self.open_gh_btn.grid(row=0, column=1, padx=(0, 8))

        self.cancel_btn = ttk.Button(
            bottom,
            text="⏹ Отмена",
            style="Danger.TButton",
            command=self._cancel_upload,
            state=tk.DISABLED,
        )
        self.cancel_btn.grid(row=0, column=2, padx=(0, 8))

        self.publish_btn = ttk.Button(
            bottom,
            text="🚀 Опубликовать / Дозагрузить релиз",
            style="Primary.TButton",
            command=self._start_publish,
        )
        self.publish_btn.grid(row=0, column=3)

    def _make_card(self, parent: tk.Misc, row: int, pady: tuple[int, int] = (0, 0)) -> tk.Frame:
        outer = tk.Frame(parent, bg=COLORS["border"], bd=1)
        outer.grid(row=row, column=0, sticky="nsew", pady=pady)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)
        inner = tk.Frame(outer, bg=COLORS["card"], padx=12, pady=10)
        inner.grid(row=0, column=0, sticky="nsew")
        return inner

    # -----------------------------------------------------------------------
    # UI Queue & Logging
    # -----------------------------------------------------------------------

    def _post_ui(self, fn: Callable[[], None]) -> None:
        self.ui_queue.put(fn)

    def _poll_ui_queue(self) -> None:
        try:
            while True:
                fn = self.ui_queue.get_nowait()
                fn()
        except queue.Empty:
            pass
        self.root.after(60, self._poll_ui_queue)

    def _log(self, msg: str) -> None:
        stamp = time.strftime("%H:%M:%S")
        line = f"[{stamp}] {msg}\n"

        def _append() -> None:
            self.log_text.configure(state=tk.NORMAL)
            self.log_text.insert(tk.END, line)
            self.log_text.see(tk.END)
            self.log_text.configure(state=tk.DISABLED)

        if threading.current_thread() is threading.main_thread():
            _append()
        else:
            self._post_ui(_append)

    # -----------------------------------------------------------------------
    # Initialization & Data Refresh
    # -----------------------------------------------------------------------

    def _initial_refresh(self) -> None:
        self._refresh_git_head()
        self._verify_token_async()
        self._refresh_all()

    def _refresh_git_head(self) -> None:
        info = self.git.get_head_info()
        self.git_head_label.configure(text=f"Git: {info['branch']} @ {info['hash']}")
        self.all_tags = self.git.get_tags()
        self.tag_combo.configure(values=self.all_tags)

    def _verify_token_async(self) -> None:
        if not self.client:
            self.auth_btn.configure(text="🔑 Токен не найден (нажмите для ввода)", fg=COLORS["danger"])
            self._log("⚠ GitHub токен не найден автоматически. Нажмите кнопку токена справа вверху.")
            return

        def _worker() -> None:
            try:
                user = self.client.validate_auth()  # type: ignore[union-attr]
                login = user.get("login", "OK")
                self._post_ui(
                    lambda: (
                        self.auth_btn.configure(text=f"🔑 {login} ({self.token_source})", fg=COLORS["success"]),
                        self._log(f"Авторизация GitHub: @{login} ({self.token_source})."),
                    )
                )
            except Exception as exc:
                self._post_ui(
                    lambda: (
                        self.auth_btn.configure(text="🔑 Ошибка токена (изменить)", fg=COLORS["danger"]),
                        self._log(f"⚠ Ошибка проверки токена GitHub: {exc}"),
                    )
                )

        threading.Thread(target=_worker, daemon=True).start()

    def _refresh_all(self) -> None:
        if self.is_uploading:
            return
        self._refresh_git_head()
        moved = self.dist_mgr.auto_move_fresh_dists(log_cb=self._log)
        if moved:
            self._log(f"Перенесено папок в DrNeonVersions: {len(moved)}")

        self.dist_folders = self.dist_mgr.list_dist_folders()
        display_names = [f.name for f in self.dist_folders]
        self.dist_combo.configure(values=display_names)

        current_name = self.dist_var.get()
        if display_names:
            if current_name in display_names:
                self.dist_var.set(current_name)
            else:
                self.dist_var.set(display_names[0])
            self._on_dist_selected()
        else:
            self.dist_var.set("")
            self.dist_path_label.configure(text="Папки *-dists не найдены. Выберите папку вручную через «Обзор...»")
            self.archives = []
            self._rebuild_asset_rows()

    def _browse_dist_folder(self) -> None:
        if self.is_uploading:
            return
        initial = str(VERSIONS_DIR if VERSIONS_DIR.is_dir() else PROJECTS_DIR)
        chosen = filedialog.askdirectory(title="Выберите папку со сборками (*-dists)", initialdir=initial)
        if not chosen:
            return
        path = Path(chosen)
        if path not in self.dist_folders:
            self.dist_folders.insert(0, path)
            self.dist_combo.configure(values=[f.name for f in self.dist_folders])
        self.dist_var.set(path.name)
        self._on_dist_selected(explicit_path=path)

    def _open_current_dist(self) -> None:
        folder = self._selected_dist_folder()
        if folder and folder.is_dir():
            os.startfile(str(folder))  # type: ignore[attr-defined]

    def _selected_dist_folder(self) -> Optional[Path]:
        name = self.dist_var.get().strip()
        for f in self.dist_folders:
            if f.name == name:
                return f
        return None

    def _on_dist_selected(self, explicit_path: Optional[Path] = None) -> None:
        folder = explicit_path or self._selected_dist_folder()
        if not folder:
            return
        self.dist_path_label.configure(text=f"Путь: {folder}")

        meta = self.dist_mgr.parse_folder_metadata(folder, self.all_tags)
        self.tag_var.set(meta.tag)
        self.title_var.set(meta.title)
        self.prerelease_var.set(meta.prerelease)
        self._reset_changelog_body()

        self.archives = self.dist_mgr.scan_archives(folder)
        self._rebuild_asset_rows()
        self._on_tag_changed()

    def _apply_title_prefix(self, prefix: str) -> None:
        title = self.title_var.get().strip()
        cleaned = re.sub(r"^\[[A-Z0-9_-]+\]\s*", "", title)
        tag = self.tag_var.get().strip()
        base = cleaned or tag
        self.title_var.set(f"{prefix} {base}".strip())
        self.prerelease_var.set(prefix != "[STABLE]")

    def _reset_changelog_body(self) -> None:
        tag = self.tag_var.get().strip()
        prev_tag = self.git.get_previous_tag(tag, self.all_tags)
        if prev_tag and tag:
            text = f"**Full Changelog**: https://github.com/{self.repo_slug}/compare/{prev_tag}...{tag}"
        else:
            text = ""
        self.body_text.delete("1.0", tk.END)
        self.body_text.insert("1.0", text)

    def _append_git_commits(self) -> None:
        tag = self.tag_var.get().strip()
        prev_tag = self.git.get_previous_tag(tag, self.all_tags)
        target_ref = tag if self.git.tag_exists_local(tag) else "HEAD"
        commits = self.git.get_commits_between(prev_tag, target_ref=target_ref)
        if not commits:
            self._log("Нет коммитов для вставки относительно предыдущего тега.")
            return
        existing = self.body_text.get("1.0", tk.END).strip()
        block = "## Что изменилось\n" + "\n".join(commits)
        new_body = f"{block}\n\n{existing}" if existing else block
        self.body_text.delete("1.0", tk.END)
        self.body_text.insert("1.0", new_body)

    # -----------------------------------------------------------------------
    # Tag & Remote Release Lookup
    # -----------------------------------------------------------------------

    def _on_tag_changed(self) -> None:
        tag = self.tag_var.get().strip()
        if not tag:
            return
        self.release_lookup_seq += 1
        seq = self.release_lookup_seq

        local_exists = self.git.tag_exists_local(tag)
        self.git_tag_status_label.configure(
            text="Git: локальный тег есть (проверяем GitHub...)"
            if local_exists
            else "Git: тег новый — будет создан на HEAD и отправлен в origin"
        )
        self.release_status_badge.configure(text="⏳ Проверка релиза на GitHub...", fg=COLORS["muted"])

        def _worker() -> None:
            remote_tag_exists = self.git.tag_exists_remote(tag)
            release_data: Optional[dict[str, Any]] = None
            lookup_err: Optional[str] = None
            if self.client:
                try:
                    release_data = self.client.find_release_by_tag(tag)
                except Exception as exc:
                    lookup_err = str(exc)

            def _apply() -> None:
                if seq != self.release_lookup_seq:
                    return
                self.current_release = release_data
                if local_exists and remote_tag_exists:
                    tag_msg = "Git: тег уже есть локально и на origin"
                elif local_exists:
                    tag_msg = "Git: тег есть локально (будет отправлен на origin)"
                else:
                    tag_msg = "Git: новый тег (создастся на HEAD + push origin)"
                self.git_tag_status_label.configure(text=tag_msg)

                if lookup_err:
                    self.release_status_badge.configure(text="⚠ Ошибка проверки GitHub", fg=COLORS["warning"])
                    self._log(f"Ошибка проверки релиза '{tag}': {lookup_err}")
                    self._sync_assets_with_remote(None)
                    return

                if release_data:
                    assets = release_data.get("assets") or []
                    is_draft = bool(release_data.get("draft"))
                    draft_tag = " [ЧЕРНОВИК]" if is_draft else ""
                    self.release_status_badge.configure(
                        text=f"🟢 Релиз уже есть{draft_tag} • файлов на GitHub: {len(assets)}",
                        fg=COLORS["success"] if not is_draft else COLORS["warning"],
                    )
                    if release_data.get("name"):
                        self.title_var.set(release_data["name"])
                    if "prerelease" in release_data:
                        self.prerelease_var.set(bool(release_data["prerelease"]))
                    if release_data.get("body"):
                        self.body_text.delete("1.0", tk.END)
                        self.body_text.insert("1.0", release_data["body"])
                    self.draft_only_var.set(is_draft)
                else:
                    self.release_status_badge.configure(
                        text="🆕 Релиза с этим тегом ещё нет (будет создан)",
                        fg=COLORS["accent"],
                    )
                    self.draft_only_var.set(False)

                self._sync_assets_with_remote(release_data)

            self._post_ui(_apply)

        threading.Thread(target=_worker, daemon=True).start()

    def _sync_assets_with_remote(self, release_data: Optional[dict[str, Any]]) -> None:
        remote_map: dict[str, dict[str, Any]] = {}
        if release_data:
            for asset in release_data.get("assets") or []:
                remote_map[asset.get("name", "")] = asset

        for item in self.archives:
            remote = remote_map.get(item.name)
            item.progress = 0.0
            item.uploaded_bytes = 0
            item.speed_mbps = 0.0
            item.eta_sec = None
            item.state = "idle"
            if remote:
                item.remote_asset_id = int(remote["id"])
                item.remote_size = int(remote.get("size", 0))
                item.remote_url = remote.get("browser_download_url")
                item.selected = False
                item.status_text = f"Уже на GitHub ({format_size(item.remote_size)}) — отметьте для перезаписи"
            else:
                item.remote_asset_id = None
                item.remote_size = None
                item.remote_url = None
                item.selected = not item.is_dlc
                item.status_text = (
                    "DLC-архив из корня проекта (опционально)" if item.is_dlc else "Готов к дозагрузке" if release_data else "Готов к загрузке"
                )
        self._rebuild_asset_rows()

    # -----------------------------------------------------------------------
    # Asset List UI Rows
    # -----------------------------------------------------------------------

    def _rebuild_asset_rows(self) -> None:
        for child in self.assets_inner.winfo_children():
            child.destroy()
        self.archive_rows.clear()

        if not self.archives:
            empty_lbl = ttk.Label(
                self.assets_inner,
                text="В выбранной папке не найдено архивов (.zip, .tar.bz2, .7z, .exe...)",
                style="Muted.TLabel",
            )
            empty_lbl.pack(anchor="w", padx=6, pady=12)
            return

        for item in self.archives:
            row_frame = tk.Frame(self.assets_inner, bg=COLORS["card_alt"], padx=10, pady=7)
            row_frame.pack(fill=tk.X, pady=(0, 6))
            row_frame.columnconfigure(1, weight=1)

            var = tk.BooleanVar(value=item.selected)
            label_prefix = "[DLC] " if item.is_dlc else ""
            chk = ttk.Checkbutton(
                row_frame,
                text=f"{label_prefix}{item.name}",
                variable=var,
                style="Row.TCheckbutton",
                command=lambda it=item, v=var: setattr(it, "selected", v.get()),
            )
            chk.grid(row=0, column=0, sticky="w")

            size_lbl = ttk.Label(row_frame, text=format_size(item.size), style="RowMuted.TLabel")
            size_lbl.grid(row=0, column=1, sticky="w", padx=(12, 0))

            status_lbl = tk.Label(
                row_frame,
                text=item.status_text,
                bg=COLORS["card_alt"],
                fg=COLORS["success"] if item.remote_asset_id else COLORS["muted"],
                font=("Segoe UI", 9),
                anchor="e",
            )
            status_lbl.grid(row=0, column=2, sticky="e", padx=(10, 0))

            pbar = ttk.Progressbar(
                row_frame,
                orient=tk.HORIZONTAL,
                mode="determinate",
                maximum=100.0,
                value=100.0 if item.remote_asset_id else 0.0,
                style="Done.Horizontal.TProgressbar" if item.remote_asset_id else "Neon.Horizontal.TProgressbar",
            )
            pbar.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(5, 0))

            self.archive_rows.append(
                {
                    "item": item,
                    "var": var,
                    "chk": chk,
                    "status_lbl": status_lbl,
                    "pbar": pbar,
                }
            )

        # Show helpful note if assets.zip DLC is not present in project root
        if not (PROJECT_ROOT / "assets.zip").is_file():
            hint = ttk.Label(
                self.assets_inner,
                text="ℹ DLC assets.zip в корне проекта не найден (опционально собирается внутри игры через devtools).",
                style="Muted.TLabel",
            )
            hint.pack(anchor="w", padx=4, pady=(2, 0))

    def _select_all_assets(self, value: bool) -> None:
        if self.is_uploading:
            return
        for row in self.archive_rows:
            row["item"].selected = value
            row["var"].set(value)

    def _select_missing_assets(self) -> None:
        if self.is_uploading:
            return
        for row in self.archive_rows:
            item: ArchiveItem = row["item"]
            should_select = (item.remote_asset_id is None) and (not item.is_dlc)
            item.selected = should_select
            row["var"].set(should_select)

    def _on_assets_mousewheel(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        first, last = self.assets_canvas.yview()
        if first <= 0.0 and last >= 1.0:
            return
        self.assets_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _update_row_visual(
        self,
        item: ArchiveItem,
        progress: Optional[float] = None,
        status_text: Optional[str] = None,
        state: Optional[str] = None,
    ) -> None:
        prog_val = item.progress if progress is None else progress
        stat_val = item.status_text if status_text is None else status_text
        state_val = item.state if state is None else state
        for row in self.archive_rows:
            if row["item"] is not item:
                continue
            pbar: ttk.Progressbar = row["pbar"]
            lbl: tk.Label = row["status_lbl"]
            pbar["value"] = prog_val
            lbl.configure(text=stat_val)

            if state_val == "done":
                pbar.configure(style="Done.Horizontal.TProgressbar")
                lbl.configure(fg=COLORS["success"])
            elif state_val == "error":
                lbl.configure(fg=COLORS["danger"])
            elif state_val == "uploading":
                pbar.configure(style="Neon.Horizontal.TProgressbar")
                lbl.configure(fg=COLORS["accent"])
            else:
                lbl.configure(fg=COLORS["muted"])
            break

    # -----------------------------------------------------------------------
    # Token Prompt Dialog
    # -----------------------------------------------------------------------

    def _prompt_token_dialog(self) -> None:
        dlg = tk.Toplevel(self.root)
        dlg.title("GitHub Personal Access Token")
        dlg.configure(bg=COLORS["card"])
        dlg.geometry("500x210")
        dlg.transient(self.root)
        dlg.grab_set()
        if ICON_PATH.is_file():
            try:
                dlg.iconbitmap(str(ICON_PATH))
            except tk.TclError:
                pass

        ttk.Label(
            dlg,
            text="Токен автоматически берётся из Git Credential Manager.\nВы можете временно задать другой токен (с правами repo):",
            style="Card.TLabel",
        ).pack(anchor="w", padx=14, pady=(14, 8))

        token_var = tk.StringVar(value=self.token)
        entry = ttk.Entry(dlg, textvariable=token_var, show="•")
        entry.pack(fill=tk.X, padx=14, pady=(0, 12))
        entry.focus_set()

        btns = tk.Frame(dlg, bg=COLORS["card"])
        btns.pack(fill=tk.X, padx=14, pady=(4, 10))

        def _apply() -> None:
            new_tok = token_var.get().strip()
            if new_tok:
                self.token = new_tok
                self.token_source = "ручной ввод"
                self.client = GitHubReleaseClient(self.repo_slug, self.token)
                self._verify_token_async()
                self._on_tag_changed()
            dlg.destroy()

        ttk.Button(btns, text="Отмена", style="Secondary.TButton", command=dlg.destroy).pack(side=tk.RIGHT, padx=(8, 0))
        ttk.Button(btns, text="Применить", style="Primary.TButton", command=_apply).pack(side=tk.RIGHT)

    # -----------------------------------------------------------------------
    # Publish / Parallel Upload Orchestration
    # -----------------------------------------------------------------------

    def _set_controls_locked(self, locked: bool) -> None:
        self.is_uploading = locked
        state = tk.DISABLED if locked else tk.NORMAL
        self.publish_btn.configure(state=state)
        self.cancel_btn.configure(state=tk.NORMAL if locked else tk.DISABLED)
        self.dist_combo.configure(state=tk.DISABLED if locked else "readonly")
        self.tag_combo.configure(state=state)
        self.title_entry.configure(state=state)
        self.threads_combo.configure(state=tk.DISABLED if locked else "readonly")
        for row in self.archive_rows:
            row["chk"].configure(state=state)

    def _cancel_upload(self) -> None:
        if self.is_uploading:
            self.cancel_event.set()
            if self.client:
                self.client.abort_active_uploads()
            self._log("⏹ Запрошена отмена загрузки...")
            self.total_status_label.configure(text="Отмена загрузки...")

    def _open_release_in_browser(self) -> None:
        if self.current_release and self.current_release.get("html_url"):
            webbrowser.open(self.current_release["html_url"])
        else:
            tag = self.tag_var.get().strip()
            if tag:
                webbrowser.open(f"https://github.com/{self.repo_slug}/releases/tag/{urllib.parse.quote(tag)}")
            else:
                webbrowser.open(f"https://github.com/{self.repo_slug}/releases")

    def _start_publish(self) -> None:
        if self.is_uploading:
            return
        if not self.client or not self.token:
            messagebox.showerror("Нет токена GitHub", "GitHub токен не найден. Нажмите кнопку токена вверху и введите PAT с правами repo.")
            return

        tag = self.tag_var.get().strip()
        title = self.title_var.get().strip() or tag
        body = self.body_text.get("1.0", tk.END).strip()
        prerelease = bool(self.prerelease_var.get())
        keep_draft = bool(self.draft_only_var.get())
        try:
            max_workers = max(1, min(4, int(self.threads_var.get())))
        except ValueError:
            max_workers = 3

        if not tag:
            messagebox.showwarning("Не указан тег", "Введите Git-тег для релиза (например, v0.8.15).")
            return

        selected_items = [row["item"] for row in self.archive_rows if row["var"].get()]
        if not selected_items:
            proceed = messagebox.askyesno(
                "Файлы не выбраны",
                "Не выбран ни один файл для загрузки.\nСоздать / обновить только сам релиз (тег, название и описание)?",
            )
            if not proceed:
                return

        self.cancel_event.clear()
        self._set_controls_locked(True)
        self.total_status_label.configure(text="Подготовка Git-тега и релиза...")

        for item in selected_items:
            item.selected = True
            item.state = "queued"
            item.progress = 0.0
            item.uploaded_bytes = 0
            item.speed_mbps = 0.0
            item.eta_sec = None
            item.status_text = "В очереди..."
            self._update_row_visual(item)

        threading.Thread(
            target=self._publish_worker,
            args=(tag, title, body, prerelease, keep_draft, max_workers, selected_items),
            daemon=True,
        ).start()

    def _publish_worker(
        self,
        tag: str,
        title: str,
        body: str,
        prerelease: bool,
        keep_draft: bool,
        max_workers: int,
        selected_items: list[ArchiveItem],
    ) -> None:
        assert self.client is not None
        client = self.client
        release_obj: Optional[dict[str, Any]] = None
        created_new_release = False

        try:
            # 1. Ensure Git tag exists & pushed
            self.git.ensure_tag_pushed(tag, self._log)
            if self.cancel_event.is_set():
                raise UploadCancelledError("Отменено пользователем.")

            # 2. Find existing release or create a Draft first (protects update_cdn_hash.yml)
            existing = client.find_release_by_tag(tag)
            if existing:
                release_obj = existing
                self._log(f"Используем существующий релиз id={release_obj['id']} (draft={release_obj.get('draft')}).")
            else:
                self._log(f"Создаём черновик релиза '{title}' ({tag}) перед загрузкой архивов...")
                release_obj = client.create_release(
                    tag_name=tag,
                    name=title,
                    body=body,
                    prerelease=prerelease,
                    draft=True,
                )
                created_new_release = True
                self._log(f"Черновик релиза создан (id={release_obj['id']}).")

            release_id = int(release_obj["id"])
            upload_url = str(release_obj["upload_url"])

            # Refresh remote assets map right before upload
            remote_assets = {a["name"]: a for a in client.list_assets(release_id)}

            # 3. Parallel upload of selected assets
            if selected_items:
                total_bytes = sum(it.size for it in selected_items)
                progress_lock = threading.Lock()
                start_all_ts = time.monotonic()

                def _update_overall() -> None:
                    with progress_lock:
                        done_bytes = sum(it.uploaded_bytes for it in selected_items)
                        total_speed = sum(it.speed_mbps for it in selected_items if it.state == "uploading")
                    pct = (done_bytes / total_bytes * 100.0) if total_bytes > 0 else 100.0
                    rem_mb = max(0.0, (total_bytes - done_bytes) / (1024 * 1024))
                    eta = rem_mb / total_speed if total_speed > 0.05 else None
                    msg = (
                        f"Загрузка: {pct:.1f}% ({format_size(done_bytes)} / {format_size(total_bytes)})"
                        f"  •  Скорость: {total_speed:.1f} МБ/с  •  Осталось: {format_eta(eta)}"
                    )
                    self._post_ui(lambda m=msg: self.total_status_label.configure(text=m))

                def _upload_one(item: ArchiveItem) -> None:
                    if self.cancel_event.is_set():
                        raise UploadCancelledError("Отменено.")

                    # Delete colliding asset if overwriting
                    if item.name in remote_assets:
                        old_id = int(remote_assets[item.name]["id"])
                        self._log(f"[{item.name}] Удаление старого файла на GitHub (asset_id={old_id})...")
                        client.delete_asset(old_id)

                    def _on_prog(sent: int, speed: float, eta: Optional[float]) -> None:
                        pct = (sent / item.size * 100.0) if item.size > 0 else 100.0
                        txt = f"Загрузка: {pct:.1f}% ({speed:.1f} МБ/с, ~{format_eta(eta)})"
                        with progress_lock:
                            item.state = "uploading"
                            item.uploaded_bytes = sent
                            item.progress = pct
                            item.speed_mbps = speed
                            item.eta_sec = eta
                            item.status_text = txt
                        self._post_ui(lambda it=item, p=pct, t=txt: self._update_row_visual(it, p, t, "uploading"))
                        _update_overall()

                    self._log(f"⬆ Старт загрузки: {item.name} ({format_size(item.size)})")
                    uploaded_asset = client.upload_asset(
                        release_id=release_id,
                        upload_url_template=upload_url,
                        file_path=item.path,
                        asset_name=item.name,
                        cancel_event=self.cancel_event,
                        progress_cb=_on_prog,
                        log_cb=self._log,
                    )
                    with progress_lock:
                        item.state = "done"
                        item.progress = 100.0
                        item.uploaded_bytes = item.size
                        item.remote_asset_id = int(uploaded_asset["id"])
                        item.remote_size = int(uploaded_asset.get("size", item.size))
                        item.remote_url = uploaded_asset.get("browser_download_url")
                        done_txt = f"✅ Загружено ({item.speed_mbps:.1f} МБ/с)"
                        item.status_text = done_txt
                    self._post_ui(lambda it=item, t=done_txt: self._update_row_visual(it, 100.0, t, "done"))
                    _update_overall()
                    self._log(f"✅ Загружен: {item.name}")

                self._log(f"Запуск параллельной загрузки ({len(selected_items)} файл(ов), потоков: {max_workers})...")
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
                    futures = [pool.submit(_upload_one, it) for it in selected_items]
                    errors: list[str] = []
                    for fut, it in zip(futures, selected_items):
                        try:
                            fut.result()
                        except UploadCancelledError:
                            it.state = "idle"
                            it.status_text = "Отменено"
                            self._post_ui(lambda item_ref=it: self._update_row_visual(item_ref))
                            errors.append("Отменено пользователем")
                        except Exception as exc:
                            it.state = "error"
                            it.status_text = f"❌ Ошибка: {exc}"
                            self._post_ui(lambda item_ref=it: self._update_row_visual(item_ref))
                            self._log(f"❌ [{it.name}] {exc}")
                            errors.append(f"{it.name}: {exc}")

                if self.cancel_event.is_set():
                    raise UploadCancelledError("Загрузка отменена пользователем.")
                if errors:
                    raise RuntimeError("Ошибки при загрузке файлов:\n" + "\n".join(errors))

                elapsed = max(time.monotonic() - start_all_ts, 0.01)
                avg_total = (total_bytes / (1024 * 1024)) / elapsed
                self._log(f"Все файлы загружены за {format_eta(elapsed)} (средняя скорость: {avg_total:.1f} МБ/с).")

            # 4. Finalize metadata & publish (sets draft=False if not keep_draft)
            final_draft = keep_draft
            action_word = "Сохранение черновика" if final_draft else "Публикация релиза"
            self._log(f"{action_word} '{title}' ({tag})...")
            final_release = client.update_release(
                release_id=release_id,
                name=title,
                body=body,
                prerelease=prerelease,
                draft=final_draft,
            )

            def _on_success() -> None:
                self.current_release = final_release
                self._set_controls_locked(False)
                self._on_tag_changed()
                state_msg = "Черновик сохранён" if final_draft else "Релиз опубликован!"
                self.total_status_label.configure(text=f"✅ {state_msg} ({tag})")
                self._log(f"🎉 Готово! URL: {final_release.get('html_url')}")
                messagebox.showinfo("Успешно", f"{state_msg}\n\n{final_release.get('html_url')}")

            self._post_ui(_on_success)

        except UploadCancelledError as exc:
            self._log(f"⏹ {exc}")
            if created_new_release and release_obj:
                self._log(f"ℹ Черновик релиза id={release_obj['id']} сохранён на GitHub — вы можете продолжить дозагрузку позже.")

            def _on_cancel() -> None:
                self._set_controls_locked(False)
                self.total_status_label.configure(text="Загрузка отменена")
                self._on_tag_changed()

            self._post_ui(_on_cancel)

        except Exception as exc:
            err_str = str(exc)
            self._log(f"❌ Ошибка: {err_str}")

            def _on_err() -> None:
                self._set_controls_locked(False)
                self.total_status_label.configure(text="Ошибка при публикации (см. журнал)")
                self._on_tag_changed()
                messagebox.showerror("Ошибка публикации", err_str)

            self._post_ui(_on_err)

    def _on_close(self) -> None:
        if self.is_uploading:
            if not messagebox.askyesno("Идёт загрузка", "Сейчас выполняется загрузка на GitHub.\nПрервать загрузку и закрыть окно?"):
                return
            self.cancel_event.set()
            if self.client:
                self.client.abort_active_uploads()
        self.root.destroy()


# ---------------------------------------------------------------------------
# Self-Test (Non-Interactive Verification)
# ---------------------------------------------------------------------------

def run_self_test() -> int:
    print("=== Release Publisher Self-Test ===")
    git = GitHelper(PROJECT_ROOT)
    dist_mgr = DistManager(PROJECT_ROOT, PROJECTS_DIR, VERSIONS_DIR)

    repo = git.get_repo_slug()
    head = git.get_head_info()
    tags = git.get_tags()
    print(f"Repo: {repo}")
    print(f"HEAD: {head['branch']} @ {head['hash']} ({head['subject']})")
    print(f"Recent tags ({len(tags)} total): {tags[:5]}")

    folders = dist_mgr.list_dist_folders()
    print(f"Found *-dists folders: {len(folders)}")
    for idx, folder in enumerate(folders[:5], start=1):
        print(f"  {idx}. {folder.name}")
    assert folders, "Expected at least one *-dists folder"

    top_folder = folders[0]
    meta = dist_mgr.parse_folder_metadata(top_folder, tags)
    prev_tag = git.get_previous_tag(meta.tag, tags)
    archives = dist_mgr.scan_archives(top_folder)
    print(f"Parsed top folder: version={meta.version!r}, channel={meta.channel!r}, tag={meta.tag!r}, title={meta.title!r}, prerelease={meta.prerelease}")
    print(f"Previous tag for changelog: {prev_tag!r}")
    print(f"Archives found ({len(archives)}):")
    for item in archives:
        print(f"  - {item.name} ({format_size(item.size)}, dlc={item.is_dlc})")

    token, source = git.get_token()
    print(f"Auth token source: {source} (present={bool(token)})")
    if token:
        client = GitHubReleaseClient(repo, token)
        user = client.validate_auth()
        print(f"GitHub authenticated as: @{user.get('login')}")
        rel = client.find_release_by_tag(meta.tag)
        if rel:
            remote_names = [a["name"] for a in (rel.get("assets") or [])]
            print(f"Existing release for {meta.tag}: id={rel['id']}, title={rel.get('name')!r}, draft={rel.get('draft')}, assets={remote_names}")
            missing = [a.name for a in archives if not a.is_dlc and a.name not in remote_names]
            print(f"Missing dist assets ready for top-up: {missing}")
        else:
            print(f"No existing release found for {meta.tag} (would create new release).")
    print("=== Self-Test PASSED ===")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Ren'Py GitHub Release Publisher GUI")
    parser.add_argument("--self-test", action="store_true", help="Run non-interactive environment & GitHub API verification.")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if os.name == "nt":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()
    ReleasePublisherGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
