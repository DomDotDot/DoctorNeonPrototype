init -990 python:
    import os
    import threading
    import time
    import json
    import subprocess
    import tempfile
    
    # === UPDATER CONFIG ===
    github_api_url = "https://api.github.com/repos/DomDotDot/DoctorNeonPrototype/releases"
    
    updater_state = {
        "status": "idle", # idle, checking, update_available, downloading, running, error
        "progress": 0.0,
        "mb_cur": 0.0,
        "mb_total": 0.0,
        "error_msg": None,
        "releases": {"stable": [], "early": []},
        "selected_track": "early",
        "selected_release": None,
        "new_version": None,
        "download_url": None,
        "exe_path": None,
        "should_cancel": False
    }

    if not renpy.variant("web"):
        import requests
    else:
        requests = None

    def check_for_updates():
        global updater_state
        if renpy.variant("web"):
            return
            
        updater_state["status"] = "checking"
        t = threading.Thread(target=_updater_check_thread)
        t.daemon = True
        t.start()
        
    def _updater_check_thread():
        global updater_state
        try:
            resp = requests.get(github_api_url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if not data:
                    updater_state["status"] = "idle"
                    return
                    
                has_newer = False
                newest_tag = ""
                
                updater_state["releases"] = {"stable": [], "early": []}
                
                # Parse all releases
                for idx, release in enumerate(data):
                    tag = release.get("tag_name", "")
                    ver = tag.lstrip('v')
                    name = release.get("name", tag)
                    body = release.get("body", "")
                    published_at = release.get("published_at", "")
                    
                    # Find .exe asset
                    exe_url = None
                    for asset in release.get("assets", []):
                        if asset.get("name", "").endswith(".exe"):
                            exe_url = asset.get("browser_download_url")
                            break
                            
                    is_early = "-early" in ver.lower() or "-dev" in ver.lower()
                    
                    rel_obj = {
                        "version": ver,
                        "name": name,
                        "body": body,
                        "exe_url": exe_url,
                        "published_at": published_at,
                        "is_early": is_early
                    }
                    
                    if is_early:
                        updater_state["releases"]["early"].append(rel_obj)
                    else:
                        updater_state["releases"]["stable"].append(rel_obj)
                        
                    # Trigger the prompt if the absolute newest release differs from current version
                    if idx == 0 and _version_compare('v' + ver, config.version) and ver != "":
                        has_newer = True
                        newest_tag = ver
                        
                if has_newer:
                    updater_state["new_version"] = newest_tag
                    updater_state["status"] = "update_available"
                    
                    # Pre-select the newest release based on its track
                    if "-early" in newest_tag.lower() or "-dev" in newest_tag.lower():
                        updater_state["selected_track"] = "early"
                        if updater_state["releases"]["early"]:
                            updater_state["selected_release"] = updater_state["releases"]["early"][0]
                    else:
                        updater_state["selected_track"] = "stable"
                        if updater_state["releases"]["stable"]:
                            updater_state["selected_release"] = updater_state["releases"]["stable"][0]
                            
                    return
                        
            updater_state["status"] = "idle"
        except Exception as e:
            updater_state["status"] = "error"
            updater_state["error_msg"] = str(e)
            print("Update Check Error: " + str(e))

    def start_game_update(release_obj=None):
        global updater_state
        
        if release_obj:
            updater_state["selected_release"] = release_obj
            
        rel = updater_state["selected_release"]
        if not rel or not rel["exe_url"]:
            return
            
        updater_state["download_url"] = rel["exe_url"]
        updater_state["new_version"] = rel["version"]
        
        updater_state["status"] = "downloading"
        updater_state["progress"] = 0.0
        updater_state["should_cancel"] = False
        
        t = threading.Thread(target=_updater_download_thread)
        t.daemon = True
        t.start()
        
    def cancel_update():
        global updater_state
        updater_state["should_cancel"] = True
        updater_state["status"] = "idle"

    def _updater_download_thread():
        global updater_state
        url = updater_state["download_url"]
        
        # Save to temp dir so it doesn't pollute the game folder
        temp_dir = tempfile.gettempdir()
        filename = "DoctorNeonPrototype_Update_" + str(updater_state["new_version"]) + ".exe"
        exe_path = os.path.join(temp_dir, filename)
        updater_state["exe_path"] = exe_path
        
        try:
            headers = {'User-Agent': 'RenPy-Game-Client'}
            with requests.get(url, stream=True, headers=headers, timeout=(5, 10)) as response:
                if response.status_code != 200:
                    raise Exception("HTTP Code: {}".format(response.status_code))
                
                total_length = response.headers.get('content-length')
                if total_length:
                    updater_state["mb_total"] = int(total_length) / 1048576.0
                else:
                    updater_state["mb_total"] = 0.0
                
                downloaded_bytes = 0
                
                with open(exe_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=65536):
                        if updater_state["should_cancel"]:
                            break
                        if chunk:
                            f.write(chunk)
                            downloaded_bytes += len(chunk)
                            updater_state["mb_cur"] = downloaded_bytes / 1048576.0
                            if total_length:
                                updater_state["progress"] = float(downloaded_bytes) / int(total_length)
                
            if not updater_state["should_cancel"]:
                updater_state["status"] = "running"
                # Launch the exe
                subprocess.Popen([exe_path])
                
        except Exception as e:
            updater_state["status"] = "error"
            updater_state["error_msg"] = str(e)
            print("Update Download Error: " + str(e))
