#!/usr/bin/env python3

from rpi_ws281x import *

import RPi.GPIO as GPIO
import socket
import time
import random

LED_OFFSET = 1 # First led out of 10/10
LED_COUNT = 100 + LED_OFFSET
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_BY_ROW = 10


def get_ip(split=' '):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip.split(split)


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

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN)
strip.begin()
strip.show()


clear()

for r in range(0, LED_COUNT):
    strip.setPixelColor(pos(r), randcolor())
    strip.show()
    time.sleep(0.025)

clear()

colors = [Color(255, 255, 255, 1), Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]

current_led = 1
for i, subip in enumerate(get_ip('.')):
    for char in subip:
        for n in range(int(char)):
            strip.setPixelColor(pos(current_led + n), colors[i])
        current_led = current_led + n + 2
    current_led = (current_led + 9) // LED_BY_ROW * LED_BY_ROW + 1  # go to next line
strip.show()
time.sleep(10)
clear()
