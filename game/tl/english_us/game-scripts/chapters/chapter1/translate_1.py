import os
import re

file_path = r'f:\RenPyDevelopment\Projects\DoctorNeonPrototype\game\tl\english_us\game-scripts\chapters\chapter1\1-lab-night.rpy'

# Read translations from a separate file or directly specify
# Here I just redefine the translation dict to keep it self-contained
translations = {
    "Не услышив ответа, он осторожно толкает створку и бесшумно проскальзывает внутрь.": "Hearing no answer, he carefully pushes the door open and silently slips inside.",
    "Девушка в кресле сидела неподвижно, откинувшись. Внешний мир перестал существовать.": "The girl in the chair sat motionless, leaning back. The outside world had ceased to exist.",
    "Каждый раз, когда она включала музыку, она уходила в свой личный космос.": "Every time she turned on the music, she drifted off into her own personal cosmos.",
    "Бесконечный поток ненужной информации, чужих эмоций, вибраций стен... Всё это исчезало, оставляя лишь кристальную ясность.": "The endless stream of useless information, other people's emotions, the vibrations of the walls... It all vanished, leaving only crystal clarity.",
    "{=thoughts}Ещё немного... Здесь, в этом такте... идеальная пауза.": "{=thoughts}Just a little more... Here, in this measure... the perfect pause.",
    "Она чувствовала себя в безопасности. Словно в коконе.": "She felt safe. As if in a cocoon.",
    "Она не слышала, как открылась дверь лаборатории.": "She didn't hear the laboratory door open.",
    "Она не слышала шагов, приближающихся к её столу.": "She didn't hear the footsteps approaching her desk.",
    "Тень упала на её лицо, перекрыв свет монитора.": "A shadow fell across her face, blocking the light from the monitor.",
    "Чья-то рука коснулась её плеча.": "Someone's hand touched her shoulder.",
    "Она вздрогнула так сильно, что едва не выронила планшет. Кокон безопасности был разорван.": "She flinched so hard she nearly dropped the tablet. The cocoon of safety was torn open.",
    "{=yell}Эй!": "{=yell}Hey!",
    "Она инстинктивно отдернула плечо, отрывая взгляд от монитора.": "She instinctively jerked her shoulder away, tearing her gaze from the monitor.",
    "В панике она выдернула наушники из ушей и сунула их глубоко в карман халата, сжав в кулаке, словно защищая самое дорогое.": "In a panic, she pulled the earphones from her ears and shoved them deep into her lab coat pocket, clenching them in her fist as if protecting her most precious possession.",
    "Она даже забыла поставить плеер на паузу — из кармана доносилось едва слышное 'цыканье' ритма.": "She even forgot to pause the player — a faintly audible rhythmic 'tss-tss' came from her pocket.",
    "Её сердце бешено колотилось. Дыхание сбилось.": "Her heart was pounding wildly. Her breath hitched.",
    "Стоило ей только моргнуть, и мир вокруг взорвался звуками: гул серверов, шум вентиляции...": "She only had to blink, and the world around her exploded with sounds: the hum of servers, the roar of ventilation...",
    "А в её глаза смотрел Маркус, её ассистент.": "And looking into her eyes was Marcus, her assistant.",
    "Маркус?! Ты... Как давно ты здесь стоишь?": "Marcus?! You... How long have you been standing there?",
    "Сзади неё стоял Маркус.": "Behind her stood Marcus.",
    "Молодой человек, аккуратный до педантизма: идеально выглаженная рубашка, туго затянутый галстук под безупречно чистым лабораторным халатом.": "A young man, neat to the point of pedantry: a perfectly ironed shirt, a tightly pulled tie under an impeccably clean lab coat.",
    "На его лице играла легкая, едва заметная ухмылка — он видел её уязвимость.": "A faint, barely noticeable smirk played on his lips — he had seen her vulnerability.",
    "Простите, доктор Неон. Я стучал. Трижды. Вы не отвечали. Я даже начал волноваться.": "Forgive me, Doctor Neon. I knocked. Three times. You didn't answer. I even started to worry.",
    "Вы выглядели так... отрешенно. Обычно вы замечаете любой шорох.": "You looked so... detached. Usually, you notice every rustle.",
    "Неон быстро убрала наушники в карман халата, стараясь вернуть себе маску холодного профессионализма. Но чувство вторжения осталось.": "Neon quickly tucked the earphones further into her coat pocket, trying to regain her mask of cold professionalism. But the feeling of intrusion lingered.",
    "Он видел её c 'обнаженной' душой.": "He had seen her with her soul 'bare'.",
    "Я работала. Глубокая концентрация. Тебе это понятие знакомо?": "I was working. Deep concentration. Are you familiar with the concept?",
    "Конечно. Просто не знал, что для концентрации вам нужна... музыка.": "Of course. I just didn't know that you needed... music for concentration.",
    "Что это было? Классика? Выглядело очень... эмоционально.": "What was it? Classical? It looked very... emotional.",
    "Он посмотрел на её карман, где спрятались наушники. Взгляд был цепким, неприятным.": "He looked at her pocket where the earphones were hiding. His gaze was clinging, unpleasant.",
    "Это не твое дело, Марк. Зачем ты пришел? Моя смена еще не окончена.": "That's none of your business, Mark. Why did you come? My shift isn't over yet.",
    "Я знаю, знаю. Просто увидел свет.": "I know, I know. I just saw the light on.",
    "Просто... я спустился к автомату в административном крыле. Там зерна лучше, чем у нас.": "It's just... I went down to the vending machine in the administrative wing. The beans are better there than ours.",
    "Подумал, вам не помешает 'заправка'. Двойной эспрессо, без сахара. Как вы любите.": "I figured you could use a 'refuel'. Double espresso, no sugar. Just the way you like it.",
    "Передохнуть буквально на пять минут?": "Take a breather for literally five minutes?",
    "Он протянул стаканчик. Запах кофе действительно был хорош, но Неон всё ещё чувствовала раздражение от того, что её прервали.": "He held out the cup. The smell of coffee was genuinely good, but Neon still felt annoyed at being interrupted.",
    "Запах свежего, крепкого кофе ударил в нос Неон, мгновенно вызывая рефлекторное желание.": "The smell of fresh, strong coffee hit Neon's nose, instantly triggering a reflexive craving.",
    "Её организм, державшийся на кофеине последние сорок восемь часов, предательски заныл.": "Her body, running on caffeine for the last forty-eight hours, cried out traitorously.",
    "Послушайте, я знаю, что я не лучший ассистент. Я путаюсь под ногами, задаю глупые вопросы...": "Listen, I know I'm not the best assistant. I get in the way, ask stupid questions...",
    "Вы делаете великое открытие, а я... я просто ношу бумажки.": "You're making a great discovery, and I... I just carry papers.",
    "Позвольте мне быть полезным хотя бы в этом? Просто... принести кофе. Чтобы вы не отвлекались.": "Let me be useful at least in this? Just... bringing you coffee. So you won't get distracted.",
    "Спасибо, доктор. Осторожно, горячий.": "Thank you, Doctor. Careful, it's hot.",
    "Вы выглядите уставшей, Неон. Может, стоит сделать перерыв? Вы здесь уже 48 часов.": "You look tired, Neon. Maybe you should take a break? You've been here for 48 hours.",
    "Если хотите, я могу посидеть здесь. Покараулить процесс дешифровки. А вы вздремнете в комнате отдыха.": "If you want, I can sit here. Keep an eye on the decryption process. While you take a nap in the break room.",
    "Неон резко обернулась к монитору. Шкала прогресса показывала 98 процентов.": "Neon sharply turned back to the monitor. The progress bar showed 98 percent.",
    "Она внезапно насторожившись, её глаза сузились.": "She suddenly grew wary, her eyes narrowing.",
    "С чего такой интерес к техническим деталям, Марк? Решил мою работу делать?": "Why the sudden interest in technical details, Mark? Decided to do my job?",
    "Нет. Я закончу сама. Это мой проект, Марк. Иди спать.": "No. I will finish it myself. This is my project, Mark. Go to sleep.",
    "Как скажете. Я лишь хотел помочь.": "As you wish. I only wanted to help.",
    "Он отступил к двери, но перед выходом снова бросил взгляд на её карман.": "He stepped back toward the door, but before leaving, he threw another glance at her pocket.",
    "Берегите слух, доктор. Громкая музыка... отвлекает от реальности.": "Take care of your hearing, Doctor. Loud music... distracts from reality.",
    "То есть, продуктивной ночи.": "I mean, have a productive night.",
    "{=whisper}Идиот...": "{=whisper}Idiot...",
    "Когда дверь закрылась, она выдохнула, отрезая её от остального мира. Наконец-то.": "When the door closed, she exhaled, cutting her off from the rest of the world. Finally.",
    "Тишина лаборатории снова навалилась на неё, но теперь она казалась враждебной. Гул серверов раздражал. А курсор на экране мигал, напоминая о незавершенной работе.": "The silence of the laboratory pressed down on her again, but now it felt hostile. The hum of the servers was annoying. And the cursor on the screen blinked, a reminder of the unfinished work.",
    "Ей нужно было вернуться. Туда. В ту гармонию.": "She needed to return. Back there. Into that harmony.",
    "Она достала наушники. Пальцы слегка дрожали.": "She took out the earphones. Her fingers were trembling slightly.",
    "Рука привычно нырнула в карман халата. Пальцы, всё ещё слегка дрожащие, нащупали гладкий пластик.": "Her hand habitually dived into her lab coat pocket. Her fingers, still trembling slightly, felt the smooth plastic.",
    "Она снова достала их - маленькие, потертые, беспроводные. Похожие на обычные беруши, но скрывающие в себе её личный космос.": "She pulled them out again - small, worn, wireless. Looking like ordinary earplugs, but concealing her personal cosmos within.",
    "Тихое, меланхоличное фортепиано. Она не знала, кто это играет. Она не знала названия этой композиции.": "A quiet, melancholic piano. She didn't know who was playing. She didn't know the name of this composition.",
    "Она нашла этот трек случайно, в каком-то своем старом архиве, без названия, без даты и автора. Цифровой призрак.": "She found this track by accident, in some old archive of hers, with no title, no date, and no author. A digital ghost.",
    "Но каждый раз, когда она включала его, 'Шум' отступал.": "But every time she turned it on, the 'Noise' retreated.",
    "{=thoughts}Нужно досмотреть. Там... ...было что-то ещё. Данные расшифровываются в видеопоток.{/thoughts}": "{=thoughts}I need to finish watching. There... ...was something else. The data is decoding into a video stream.{/thoughts}",
    "Она нажала клавишу ввода на клавиатуре.": "She pressed the enter key on the keyboard.",
    "На экране монитора, сквозь цифровую рябь и 'снег' статики, начало проступать изображение.": "On the monitor screen, through digital ripples and static 'snow', an image began to emerge.",
    "Видео захлебнулось статикой. Последнее, что осталось на сетчатке — это взгляд человека, которого предали в самый важный момент жизни.": "The video choked on static. The last thing left burned into her retina was the gaze of someone who had been betrayed at the most important moment of their life.",
    "Взгляд, который Неон никогда не должна была забывать. Но забыла или вынесла слишком глубоко в подсознание.": "A gaze that Neon should never have forgotten. But she had forgotten, or shoved it too deep into her subconscious.",
    "Экран вспыхнул и погас.": "The screen flashed and went dark.",
    "Неон отшатнулась от стола, хватаясь за сердце. Ощущение 'неправильности' красных глаз на нежном лице всё ещё стояло перед глазами, как ожог.": "Neon recoiled from the desk, clutching her heart. The feeling of 'wrongness' of those red eyes on a delicate face still burned before her eyes like a scorch mark.",
    "Я... я знала этот взгляд.": "I... I knew that look.",
    "Сердце Неон пропускало удары. Это не было похоже на контакт с внеземной цивилизацией.": "Neon's heart skipped beats. This didn't feel like contact with an extraterrestrial civilization.",
    "Это было похоже на то, как если бы она нашла старую видеокассету из своего студенчества, о котором забыла.": "It felt as if she had found an old VHS tape from her student days that she had forgotten about.",
    "Ощущение дежавю было таким сильным, что у неё перехватило дыхание.": "The feeling of deja vu was so strong it took her breath away.",
    "{=thoughts}Это не просто сигнал. Это... воспоминание? Но чьё? Моё? Нет, я никогда не играла... никогда не видела это...": "{=thoughts}This isn't just a signal. It's... a memory? But whose? Mine? No, I've never played... I've never seen this...",
    "{=thoughts}Если это кто-то другой... то Кто?": "{=thoughts}If it's someone else... then Who?",
    "{=thoughts}Почему я чувствую эту боль? Чувство потери... незавершенности. Это же не я...": "{=thoughts}Why do I feel this pain? This sense of loss... of incompleteness. This isn't me...",
    "{=thoughts}Может, это кто-то из... прошлого? Кто-то, кого я знала? Кого я потеряла?": "{=thoughts}Maybe it's someone from the... past? Someone I knew? Someone I lost?",
    "{=thoughts}И почему она прозвала меня 'обманщицей'? Неужели я когда-то... предала кого-то?": "{=thoughts}And why did she call me a 'liar'? Did I really... betray someone once?",
    "{=thoughts}Нет. Это невозможно. Я не могу не помнить такого... Я бы никогда...": "{=thoughts}No. It's impossible. I couldn't just forget something like that... I would never...",
    "{=thoughts}Может, это просто игра моего разума. Усталость. Переутомление. Глюки памяти... Может, я просто слишком много работаю...": "{=thoughts}Maybe it's just my mind playing tricks on me. Exhaustion. Overwork. Memory glitches... Maybe I'm just working too much...",
    "{=thoughts}Мне показалось... я даже не слышала её как она это говорила... Это просто мой мозг подсовывает мне образы...": "{=thoughts}I must have imagined it... I didn't even hear her say it... It's just my brain feeding me images...",
    "{=thoughts}Но если она этого не говорила... то как я её поняла?": "{=thoughts}But if she didn't say it... then how did I understand her?",
    "{=thoughts}Кто ты...?{/thoughts}": "{=thoughts}Who are you...?{/thoughts}",
    "Она коснулась монитора кончиками пальцев, там, где секунду назад было лицо незнакомки.": "She touched the monitor with her fingertips, right where the stranger's face had been a second ago.",
    "Внутри разливалось странное, щемящее чувство потери. Словно она только что увидела близкого друга, который уходит в темноту, хлопнув дверью, а она не успела его остановить.": "A strange, aching sense of loss washed over her inside. As if she had just watched a close friend walk out into the dark, slamming the door, and she hadn't been quick enough to stop them.",
    "{=whisper}Постой...": "{=whisper}Wait...",
    "Её шепот растворился в гуле вентиляторов системного блока. Никто не ответил.": "Her whisper dissolved in the hum of the computer's cooling fans. No one answered.",
    "Усталость, которую она сдерживала адреналином открытия, навалилась с новой, сокрушительной силой.": "The exhaustion she had been holding at bay with the adrenaline of discovery crashed down on her with renewed, crushing force.",
    "Но теперь это была не просто тяжесть в мышцах. Это была тяжесть в груди — свинцовая, тягучая тоска по чему-то, что она не могла назвать.": "But now it wasn't just a heaviness in her muscles. It was a heaviness in her chest — a leaden, viscous longing for something she couldn't name.",
    "{=thoughts}Нужно... прогнать через фильтры... очистить лицо... завтра...{/thoughts}": "{=thoughts}I need... to run it through the filters... clear up the face... tomorrow...{/thoughts}",
    "Она попыталась потянуться к клавиатуре, чтобы ввести команду, но пальцы отказались слушаться. Руки казались чужими, сделанными из ваты.": "She tried to reach for the keyboard to type a command, but her fingers refused to obey. Her hands felt alien, as if made of cotton.",
    "Неон медленно опустила голову на скрещенные руки, прямо поверх жесткого пластика клавиш.": "Neon slowly laid her head down on her crossed arms, right on top of the hard plastic keys.",
    "{=thoughts}Завтра... Я найду тебя завтра...{/thoughts}": "{=thoughts}Tomorrow... I'll find you tomorrow...{/thoughts}",
    "Границы реальности начали размываться.": "The boundaries of reality began to blur.",
    "Зеленые графики на мониторе поплыли, превращаясь в нотные станы. Мигающий курсор стал похож на далекую, пульсирующую звезду.": "The green graphs on the monitor swam, morphing into musical staves. The blinking cursor started to look like a distant, pulsating star.",
    "Образ девушки за роялем наложился на отражение самой Неон в темном экране.": "The image of the girl at the piano superimposed itself over Neon's own reflection in the dark screen.",
    "{=whisper}Марк... этот кофе... он был... слишком... горячим...{/whisper}": "{=whisper}Mark... that coffee... it was... too... hot...{/whisper}",
    "Её бормотание было бессвязным. Разум, защищаясь от перегрузки и боли, выключил рубильник.": "Her muttering was incoherent. Her mind, defending itself from overload and pain, flipped the kill switch.",
    "Глаза закрылись сами собой, окончательно отсекая лабораторию.": "Her eyes closed on their own, finally shutting out the laboratory.",
    "Последнее, что она видела внутренним взором перед тем, как провалиться в глубокий сон — это остаточный образ белых волокон, сияющих в темноте пустого зала.": "The last thing she saw in her mind's eye before falling into a deep sleep was the afterimage of white strands glowing in the dark of the empty hall.",
    "В темноте её собственной души.": "In the darkness of her own soul.",
    "{=thoughts}Просто... побуду с тобой... в тишине...": "{=thoughts}I'll just... stay with you... in the silence...",
    "{=thoughts}В пустоте...": "{=thoughts}In the emptiness..."
}

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

for rus, eng in translations.items():
    # Make sure to handle newlines properly and catch any character prefix
    escaped_rus = re.escape(rus)
    # The pattern matches the comment line with the Russian text:
    # # narrator "Text"
    # Followed by a newline and the empty string declaration:
    # narrator "" -> narrator "Translation"
    pattern_proper = r'(#\s*.+?"' + escaped_rus + r'")\n(\s*(?:\"[^\"]+\"|\w+(?:\s+\w+)*)\s+)""'
    text = re.sub(pattern_proper, r'\1\n\2"' + eng.replace('\\', '\\\\').replace('"', '\\"') + r'"', text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated 1-lab-night.rpy")
