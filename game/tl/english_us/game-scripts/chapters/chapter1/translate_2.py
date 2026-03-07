import os
import re

files_and_translations = {
  r'f:\RenPyDevelopment\Projects\DoctorNeonPrototype\game\tl\english_us\game-scripts\chapters\chapter1\2-lab-morning.rpy': {
    "Она судорожно задвигала мышкой, игнорируя испорченную клавиатуру.": "She frantically moved the mouse, ignoring the ruined keyboard.",
    "Да! Да! ДА!!!": "Yes! Yes! YES!!!",
    "Сон...? Ах, да. Сон. Девушка с волосами цвета снега и ночи. Ее смех. Концерт...": "A dream...? Ah, yes. A dream. The girl with hair the color of snow and night. Her laugh. The concert...",
    "Длинные светлые кудри пружинили при каждом движении, красный, с нежным оттенком, джемпер вызывающе контрастировал с белыми халатами, которые Алекс принципиально не носила.": "Long blonde curls bounced with every movement; a red, softly-tinted jumper contrasted sharply with the white lab coats that Alex fundamentally refused to wear.",
    "Неон и Алекс – подруги поневоле, связавшие себя годами совместной работы, обедов и взаимных прикрытий перед начальством.": "Neon and Alex — involuntary friends bound together by years of teamwork, lunches, and covering for each other in front of management.",
    "Не зависть – нет. Скорее, глухая ярость от несправедливости, от того, что ее собственные титанические усилия как будто обесценивались легкостью, с которой Алекс порхала по жизни, пока их пути не разошлись.": "Not envy — no. Rather, a muffled rage at the injustice, at the fact that her own titanic efforts seemed to be devalued by the ease with which Alex fluttered through life until their paths diverged.",
    "А я думала, ты уже дома дрыхнешь! Решила зайти птичек за окном послушать, пока начальства нет, а тут – сюрприз!": "And I thought you were already crashing at home! Decided to drop by and listen to the birds outside while the bosses are gone, and here – a surprise!",
    "Алекс, ну нельзя же так! Я чуть концы не отдала...": "Alex, you can't just do that! You scared me to death...",
    "Ты опять всю ночь тут просидела, да? Признавайся!": "You spent the whole night here again, didn't you? Confess!",
    "Господи, Неон, ты на себя в зеркало смотрела? Мешки под глазами скоро до колен достанут!": "Lord, Neon, have you looked in the mirror? The bags under your eyes will reach your knees soon!",
    "Ты уже неделю не выходила из комплекса! Там, внизу, вообще-то есть жизнь!": "You haven't left the complex in a week! You know, there's actually a life down there!",
    "Так же нельзя, подруга! С такой физиономией тебя ни один приличный парень на свидание не позовет! А тебе всего двадцать два!": "You can't do this, friend! With a face like that, no decent guy will ask you out! And you're only twenty-two!",
    "Молодость проходит!": "Your youth is slipping away!",
    "Ха-ха! Парни? Алекс, ты серьезно?": "Haha! Guys? Alex, are you serious?",
    "Ну как успехи? Поймала своих зеленых человечков?": "So, how’s it going? Caught your little green men?",
    "Да. Закончила. Все штатно. Только вот...": "Yes. Finished. All nominal. It's just...",
    "...": "...",
    "Что? Что случилось?": "What? What happened?",
    "Сломала? Как?!": "Broke it? How?!",
    "ПХА-ХА-ХА-ХА-ХА! СЛЮНОЙ?! Серьёзно?!": "BWA-HA-HA-HA-HA! WITH SPIT?! Seriously?!",
    "Ты серьезно?! Уснула мордой в клаву и залила ее?!": "Are you serious?! You fell asleep face-first on the keyboard and flooded it?!",
    "Ха-ха-ха!": "Hahaha!",
    "Фух... Ладно... ха...": "Phew... Alright... ha...",
    "Всё, ты сделала мой день, Неон!": "You just made my day, Neon!",
    "Алекс утерла выступившие слезы от смеха, после чего продолжила.": "Alex wiped away tears of laughter, then continued.",
    "Какая же ты все-таки... не меняешься! Годы идут, открытия мирового масштаба, а ты все та же неряха! Обожаю!": "You really are... you never change! Years pass, making world-class discoveries, yet you're perfectly as clumsy as ever! I love it!",
    "Ой, да ладно тебе.": "Oh, come on.",
    "Серьезно, Неон. Ну почему ты такая электрическая?": "Seriously, Neon. Why are you so electric?",
    "Каждый раз, когда я к тебе прикасаюсь — как будто оголенный провод трогаю.": "Every time I touch you, it feels like I'm touching an exposed wire.",
    "Мне кажется, ты просто накопитель энергии какой-то. Ходячая батарейка!": "I think you're just some kind of energy capacitor. A walking battery!",
    "Алекс посмотрела на Неон, взволнованным взглядом, который так и говорил: 'Я за тебя переживаю'": "Alex cast a worried glance at Neon, one that practically shouted, 'I'm worried about you.'",
    "А Неон потерла плечо, где произошел контакт. Там осталось странное ощущение. Не боль, а... пустота. Будто на секунду в этом месте исчезла гравитация.": "Neon rubbed her shoulder where the contact happened. A strange sensation lingered. Not pain, but... emptiness. As if gravity vanished from that spot for a second.",
    "Ой...": "Oh...",
    "Похоже, что скоро все будут работать из дома. Даже мы с тобой.": "Looks like soon everyone will be working from home. Even you and me.",
    "Надеюсь, эта дрянь до нас не доберется...": "I hope that crap doesn't reach us...",
    "Алекс, ну сколько можно? Ты в это реально веришь? Это же неофициальные слухи. Где-то в мессенджерах люди панику разводят. Верить всему подряд нельзя.": "Alex, how much more of this? Do you really believe that? It's all unofficial rumors. People spreading panic in chats. You can't believe everything.",
    "Э-это правда! Ну почему ты мне не веришь? Мы же друзья! Я-я же показывала фотки... там все желтое!": "I-it's true! Why don't you believe me? We're friends! I-I showed you the photos... everything's yellow there!",
    "Давай не будем об этом...": "Let's not talk about it...",
    "Алекс на секунду замерла, глядя на спокойное лицо подруги.": "Alex froze for a second, looking at her friend's calm face.",
    "Затем она глубоко вздохнула, тряхнула кудрями, словно физически сбрасывая с себя липкий страх.": "Then she took a deep breath and tossed her curls, as if physically shaking off the sticky fear.",
    "Она убрала телефон, тряхнула кудрями, снова улыбнулась, но уже с блеском в глазах.": "She put the phone away, tossed her curls, and smiled again, but with a gleam in her eyes.",
    "Ладно, к черту. Пока мы вместе — мне ничего не страшно! Даже желтый туман. Ты же тоже так думаешь, Неон?": "Alright, screw it. As long as we're together, I'm not afraid of anything! Not even yellow fog. You think so too, right, Neon?",
    "Я тебя никогда не брошу.": "I'll never abandon you.",
    "Ну вот видишь? Раз уж я все равно тут торчу и ключи от архива у меня с собой...": "See? Well, since I’m stuck here anyway and have the archive keys with me...",
    "Ты... серьезно? Но это же моя работа... А если узнают...": "Are you... serious? But that's my job... What if they find out...",
    "Ой, да кто узнает? У меня в архиве даже мыши от скуки дохнут. А тебе надо готовиться к триумфу!": "Oh, who's going to find out? Even the mice in my archive die of boredom. And you need to prepare for your triumph!",
    "А ты садись и пиши доклад о своем великом открытии. На бумаге, раз печатать не можешь.": "You sit down and write the report on your great discovery. On paper, since you can't type.",
    "Ручка-то у тебя найдется? Или тоже слюной растворила?": "You got a pen? Or did you dissolve that with spit too?",
    "Найдется. Спасибо, Алекс. Ты... ты лучшая.": "I have one. Thank you, Alex. You... you're the best.",
    "Знаю! В общем, давай, действуй. Хе-хе. Созвонимся позже!": "I know! Anyway, get to it. Hehe. Call you later!"
  },
  
  r'f:\RenPyDevelopment\Projects\DoctorNeonPrototype\game\tl\english_us\game-scripts\chapters\chapter1\3-lab-noon.rpy': {
    "Мимо промелькнули индикаторы других этажей: \\n 'Уровень 3: Жилой блок' \\n 'Уровень 2: Основные лаборатории' \\n": "Indicators for the other floors flashed by: \\n 'Level 3: Residential Block' \\n 'Level 2: Main Laboratories' \\n",
    "Спасибо за поддержку, Ханс. Ладно, пойду я... доклад готовить.": "Thanks for the support, Hans. Alright, I'm going... to prepare the report.",
    "Она снова погрузилась в лабиринт коридоров. Она зашла в лобби. Этот комплекс был огромен.": "She dove back into the labyrinth of corridors. She entered the lobby. This complex was immense."
  },

  r'f:\RenPyDevelopment\Projects\DoctorNeonPrototype\game\tl\english_us\game-scripts\chapters\chapter1\3.1-library.rpy': {
    "Храм тишины посреди вечного, низкочастотного гула комплекса — 'шума' как бы выразилась Неон, который Неон научилась ненавидеть.": "A temple of silence amidst the complex's eternal, low-frequency hum — the 'noise,' as Neon would put it, which she had learned to hate.",
    "Этот сигнал. Он не был похож на другие. Вселенная полна бессмысленного гула: холодное эхо мертвых звезд, монотонный пульс пустоты, вездесущее шипение радиации. Это был предсказуемый, мертвый хаос.": "This signal. It wasn't like the others. The universe is full of meaningless hum: the cold echo of dead stars, the monotonous pulse of the void, the omnipresent hiss of radiation. That was predictable, dead chaos.",
    "Но этот голос... он был другим. В нем была... жизнь. Почти что забытая песня.": "But this voice... it was different. It had... life in it. A nearly forgotten song.",
    "Словно кто-то пытался что-то сказать, но слова застревали в вакууме, оставляя лишь ритмичные паузы. Эту тишину между звуками она и пыталась расшифровать.": "As though someone was trying to say something, but the words got stuck in the vacuum, leaving only rhythmic pauses. It was this silence between the sounds that she was trying to decrypt.",
    "Попыткой вспомнить, откуда в ее душе это странное, щемящее чувство... узнавания, которое возникало всякий раз, когда она улавливала этот тонкий мотив.": "An attempt to remember where this strange, aching sense of... recognition in her soul came from, arising every time she caught this subtle motif.",
    "Написав эту фразу, она снова закрыла глаза, пытаясь поймать ритм. И тогда, как удар молнии, в ее сознании вспыхнуло видение.": "Having written that phrase, she closed her eyes again, trying to catch the rhythm. And then, like a lightning strike, a vision flashed in her mind.",
    "Ручка замерла. Дешевый пластик. Почти такая же была у нее в университете.": "The pen stopped. Cheap plastic. She had one almost exactly like it at the university.",
    "И снова, как укол, всплыл образ из утреннего сна. Но в этот раз... он был ярче.": "And again, like a sting, the image from her morning dream surfaced. But this time... it was brighter.",
    "Запах дешевых чернил смешался с запахом мела и старых аудиторий.": "The smell of cheap ink mingled with the scent of chalk and old lecture halls."
  },

  r'f:\RenPyDevelopment\Projects\DoctorNeonPrototype\game\tl\english_us\game-scripts\chapters\chapter1\3.2-library-desk.rpy': {
    "Кто же она? Кто был тем голосом, который так странно отзывался в моей душе, когда я о ней думала? И почему он казался таким знакомым, таким родным?": "Who is she? Who was that voice that resonated so strangely in my soul when I thought of her? And why did it seem so familiar, so dear?",
    "С новой решимостью Неон вернулась к докладу. Ручка оставила на бумаге первую строчку: \\n 'Анализ аномальной ритмики в секторе Дельта-4'.": "With renewed determination, Neon returned to the report. The pen left the first line on the paper: \\n 'Analysis of Anomalous Rhythmics in Sector Delta-4'.",
    "Она писала быстро, почти не задумываясь, словно слова уже давно ждали своего часа, чтобы вырваться на бумагу.": "She wrote quickly, almost without thinking, as if the words had long been waiting for their time to burst onto the paper.",
    "{=thoughts}'...устойчивый ритм исключает случайность. Не просто всплеск энергии. Это... композиция. Смысл, скрытый за завесой пустоты...'": "{=thoughts}'...a stable rhythm rules out coincidence. Not just a surge of energy. It's... a composition. Meaning, hidden behind the veil of the void...'",
    "Особенно там, в той маленькой деревушке у подножия гор, где прошло ее детство и юность. До Цюриха. До звезд.": "Especially there, in that little village at the foot of the mountains, where her childhood and youth passed. Before Zurich. Before the stars.",
    "Нужно было закончить. Нужно доказать.": "It had to be finished. It had to be proven.",
    "'{=thoughts}...ритм повторяется. Это не шум. Это не природа...'": "'{=thoughts}...the rhythm repeats. It's not noise. It's not nature...'",
    "'{=thoughts}...это кто-то создал. Кто-то, кто знает, что такое тишина...'": "'{=thoughts}...someone created this. Someone who knows what silence is...'",
    "'{=thoughts}...с высокой степенью вероятности — это послание. Или память...'": "'{=thoughts}...with a high degree of probability, it is a message. Or a memory...'",
    "Послание. Память. Не хаос. Это было ключевое слово. Ее оправдание.": "Message. Memory. Not chaos. This was the key word. Her vindication."
  },

  r'f:\RenPyDevelopment\Projects\DoctorNeonPrototype\game\tl\english_us\game-scripts\chapters\chapter1\4-meeting-start.rpy': {
    "Неон почувствовала укол странной смеси облегчения и беспокойства.": "Neon felt a sting of a strange mix of relief and anxiety.",
    "Облегчения – потому что Марк, ее тихий, исполнительный ассистент, кажется, наконец-то сделал что-то значительное.": "Relief — because Mark, her quiet, dutiful assistant, finally seemed to have done something substantial.",
    "Беспокойства – потому что это означало, что ее собственное открытие может померкнуть на его фоне.": "Anxiety — because it meant her own discovery might fade into the background.",
    "Для меня огромная честь сообщить вам, что в ходе моих независимых исследований мне удалось не только зафиксировать...": "It is a great honor for me to inform you that in the course of my independent research I have managed not only to record...",
    "...Но и успешно расшифровать сложный когерентный сигнал, который, по всем признакам, имеет искусственное внеземное происхождение!": "...But also to successfully decrypt a complex coherent signal, which, by all indications, is of artificial extraterrestrial origin!",
    "Это были её данные. Её расчеты. Её месяцы бессонных ночей и лихорадочной работы.": "These were her data. Her calculations. Her months of sleepless nights and feverish work.",
    "Это моя работа! Я расшифровала этот сигнал! Это мои расчеты! Как они оказались у него?!": "That's my work! I decrypted that signal! Those are my calculations! How did he get them?!",
    "Во-первых, где официальные отчеты о ваших исследованиях за последний квартал, подписанные и сданные в установленный срок – сегодня до полудня?": "First of all, where are the official reports on your research for the last quarter, signed and submitted by the deadline — today before noon?",
    "Их нет. Следовательно, официально, для руководства вы {i}ничем конкретным{/i} не занимались.": "They are absent. Therefore, officially, to the management, you have been engaged in {i}nothing specific{/i}.",
    "Во-вторых, вы сами только что признались, что ваша 'презентация' не готова для такого уровня.": "Secondly, you yourself just admitted that your 'presentation' is not ready for this level.",
    "Вы пришли на заседание совета директоров с... с... какими-то черновиками? Вы вообще понимаете, где находитесь и каков регламент?": "You came to a board meeting with... with... some drafts? Do you even understand where you are and what the protocol is?",
    "Она снова почувствовала себя той девочкой. Маленькой, другой, неправильной.": "She felt like that little girl again. Small, different, wrong."
  }
}

for file_path, translations in files_and_translations.items():
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    for rus, eng in translations.items():
        escaped_rus = re.escape(rus)
        pattern_proper = r'(#\s*.+?"' + escaped_rus + r'")\n(\s*(?:\"[^\"]+\"|\w+(?:\s+\w+)*)\s+)""'
        text = re.sub(pattern_proper, r'\1\n\2"' + eng.replace('\\', '\\\\').replace('"', '\\"') + r'"', text)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

print("Updated translation for intermediate chapter1 files.")
