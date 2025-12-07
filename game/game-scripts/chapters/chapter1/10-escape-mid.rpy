label car_start_sequence:

        # play sound "sounds/car_remote_unlock_beep.opus" # Звук снятия с сигнализации

        narrator """
        Дрожащими руками она нажала кнопку на брелоке.

        Машина пискнула, снимаясь с сигнализации. Неон рванула дверцу и буквально ввалилась на водительское сиденье.
        """
        # play sound "sounds/car_door_open_slam.opus" # Звук открытия и захлопывания двери

        show cg cg7_1 with fade
        narrator """
        В салоне пахло ее духами с нотками бергамота и чем-то еще – едва уловимым запахом старой бумаги от научных журналов, которые она часто возила с собой.

        Она судорожно вставила ключ в замок зажигания. Руки тряслись так, что она не сразу попала.
        """

        # play sound "sounds/keys_fumbling.opus"
        narrator "Поворот ключа. Приборная панель ожила, загорелись индикаторы."
        # play sound "sounds/car_ignition_acc_on.opus"
        narrator "Еще поворот. Стартер издал знакомый, натужный звук, но двигатель не схватил."
        # play sound "sounds/car_starter_fail_1.opus"

        neon @ frustrated "Давай же! Ну!"
        narrator "Снаружи, со стороны въезда на парковку, послышались приближающиеся крики и топот ног. Ее заметили."
        # play sound "sounds/shouts_approaching_parking.opus"
        # play sound "sounds/footsteps_running_group_concrete.opus" # Топот по бетону

        narrator "Она снова повернула ключ. Тот же результат. Двигатель был холодным, машина долго стояла."
        # play sound "sounds/car_starter_fail_2.opus"
        narrator "Паника ледяной волной захлестнула ее. Она заперла двери."
        # play sound "sounds/car_door_lock_manual.opus"
        narrator "Взгляд метнулся к зеркалу заднего вида. К машине уже бежал охранник."
        narrator "Третья попытка. Поворот ключа..."
        # play sound "sounds/car_starter_struggle_then_start.opus" # Стартер заводится
        narrator "Двигатель загудел и, наконец, с ревом ожил!"

        neon @ proud "Да!"
        narrator "Она быстро сняла машину с ручника, воткнула первую передачу. Нога на педаль газа."
        # play sound "sounds/handbrake_release.opus"
        # play sound "sounds/gear_shift_manual.opus"
        # play sound "sounds/car_engine_rev_high.opus" # Рев двигателя
        narrator "Машина дернулась и с визгом шин рванула с места, едва не задев парковочную колонну."
        # play sound "sounds/tires_squeal_short.opus"
        narrator "А догонявший её охранник, который почти добежал до нее, от страха отскочили в стороны."
return