label car_start_sequence:

        # Неон у своей машины на парковке
        # scene parking_garage_dim # Тот же фон
        # music "sounds/parking_garage_tension.ogg" # Музыка продолжается
        # play sound "sounds/car_remote_unlock_beep.ogg" # Звук снятия с сигнализации

        narrator """
        Дрожащими руками она нажала кнопку на брелоке.

        Машина пискнула, снимаясь с сигнализации. Неон рванула дверцу и буквально ввалилась на водительское сиденье.
        """
        # play sound "sounds/car_door_open_slam.ogg" # Звук открытия и захлопывания двери

        show cg cg7_1 with fade # Фон: интерьер машины Неон
        narrator """
        В салоне пахло ее духами с нотками бергамота и чем-то еще – едва уловимым запахом старой бумаги от научных журналов, которые она часто возила с собой.

        Она судорожно вставила ключ в замок зажигания. Руки тряслись так, что она не сразу попала.
        """
        # play sound "sounds/keys_fumbling.ogg"
        narrator "Поворот ключа. Приборная панель ожила, загорелись индикаторы."
        # play sound "sounds/car_ignition_acc_on.ogg"
        narrator "Еще поворот. Стартер издал знакомый, натужный звук, но двигатель не схватил."
        # play sound "sounds/car_starter_fail_1.ogg"

        neon @ frustrated "Давай же! Ну!"
        narrator "Снаружи, со стороны въезда на парковку, послышались приближающиеся крики и топот ног. Ее заметили."
        # play sound "sounds/shouts_approaching_parking.ogg"
        # play sound "sounds/footsteps_running_group_concrete.ogg" # Топот по бетону

        narrator "Она снова повернула ключ. Тот же результат. Двигатель был холодным, машина долго стояла."
        # play sound "sounds/car_starter_fail_2.ogg"
        narrator "Паника ледяной волной захлестнула ее. Она заперла двери."
        # play sound "sounds/car_door_lock_manual.ogg"
        narrator "Взгляд метнулся к зеркалу заднего вида. К машине уже бежал охранник."
        narrator "Третья попытка. Поворот ключа..."
        # play sound "sounds/car_starter_struggle_then_start.ogg" # Стартер борется и заводится
        narrator "Двигатель загудел и, наконец, с ревом ожил!"

        neon @ proud "Да!"
        narrator "Она быстро сняла машину с ручника, воткнула первую передачу. Нога на педаль газа."
        # play sound "sounds/handbrake_release.ogg"
        # play sound "sounds/gear_shift_manual.ogg"
        # play sound "sounds/car_engine_rev_high.ogg" # Рев двигателя
        narrator "Машина дернулась и с визгом шин рванула с места, едва не задев парковочную колонну."
        # play sound "sounds/tires_squeal_short.ogg"
        narrator "А догонявший её охранник, который почти добежал до нее, от страха отскочили в стороны."

        # Переход к сцене выезда с территории
return