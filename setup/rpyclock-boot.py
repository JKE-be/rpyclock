#!/usr/bin/env python3

import random
import RPi.GPIO as GPIO
import time
from rpi_ws281x import *

LED_COUNT      = 101      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_BY_ROW     = 10


def clear():
    led = 0
    while led < LED_COUNT:
        strip.setPixelColorRGB(led, 0, 0, 0, 0)
        led += 1
    strip.show()

def randcolor():
    return Color(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        white=random.randint(0, 1),
    )


def pos_from_alim(i):
    assert i >= 0
    n = i

    # 20/40/60/...
    if (i % LED_BY_ROW == 0):
        if (i // LED_BY_ROW) % 2 == 0:
            n = (i // LED_BY_ROW) * LED_BY_ROW - 9
    elif (i // LED_BY_ROW) % 2 == 1:  # if line even
        n = (i // LED_BY_ROW) * LED_BY_ROW + (LED_BY_ROW - (i % LED_BY_ROW))
        n += 1
    return n


def pos(i):
    return pos_from_alim(LED_COUNT - i)


GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
strip.show()

clear()

for r in range(0, LED_COUNT):
    strip.setPixelColor(pos(r), randcolor())
    strip.show()
    time.sleep(0.025)

clear()
