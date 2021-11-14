#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import random
import subprocess

from tools import *

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)


try:
    strip = MyPixelSquare(LED_COUNT, LED_PIN, brightness=150, words=WORDS, figures=FIGURES, led_by_row=LED_BY_ROW)
    strip.begin()
    strip.show()

    ###############
    # CHECK PIXEL #
    ###############
    strip.clear()
    strip.rainbow(wait_ms=5)
    strip.clear()

    # for color in [Color(255, 0, 0, 0), Color(0, 255, 0, 0), Color(0, 0, 255, 0), Color(255, 255, 255, 1)]:
    #     for r in range(0, strip.numPixels()):
    #         strip.setPixelColor(strip.pos(r), color)
    #         strip.show()
    #         time.sleep(0.005)

    ##############
    # DISPLAY IP #
    ##############
    colors = [strip.randcolor(), strip.randcolor(), strip.randcolor(), strip.randcolor()]
    idx = [(0, 0), (6, 0), (3, 5)]

    for i, subip in enumerate(get_ip('.')):
        strip.clear()
        figs = []
        for n, char in enumerate(subip):  # 192
            figs.append((int(char), (len(subip) == 1 and 3 or 0) + idx[n][0], len(subip) <= 2 and 3 or idx[n][1], False))
            print(subip, len(subip), figs)
        strip.lightFigures(figs, colors[i])
        time.sleep(0.7)
    strip.clear()

    ##############
    # OFF BUTTON #
    ##############
    def callbackOnOff(channel):
        strip.sayBye()
        subprocess.call(['shutdown', '-h', 'now'], shell=False)

    # https://pinout.xyz/pinout/pin5_gpio3
    GPIO.setup(ONOFF_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(ONOFF_PIN, GPIO.RISING, callback=callbackOnOff, bouncetime=300)

    #################
    # SWITCH BUTTON #
    #################

    last_switch_mode = time.time() - 10
    modes = list(MODES.keys())
    current_mode_name = 'random'

    def callbackSwitchMode(channel):
        global last_switch_mode
        global current_mode_name

        # custom debounce
        now = time.time()
        if now > last_switch_mode + 1:
            last_switch_mode = now
            current_mode_name = modes[(modes.index(current_mode_name) + 1) % len(modes)]
            print('switch mode = %s' % current_mode_name)

            strip.last_lights = []
            strip.clear()
            strip.setPixelColor(strip.pos(MODES[current_mode_name]), strip.randcolor())
            strip.show()

    def tick():
        refresh = 10  # seconds
        i = 1

        random_function = 'nowWords'

        while True:
            i += 1
            if i == (60 / refresh) * 20:  # each 20 minutes, choose random mode
                i = 0
                random_function = random.choice(['nowWords', 'nowFigures'])

            current_func = current_mode_name != 'random' and current_mode_name or random_function
            getattr(strip, current_func)()
            time.sleep(refresh)

    GPIO.setup(MODE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(MODE_PIN, GPIO.RISING, callback=callbackSwitchMode, bouncetime=300)

    tick()
except KeyboardInterrupt:
    strip.sayBye()
    time.sleep(3)
    pass
