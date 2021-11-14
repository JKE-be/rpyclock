import socket
import random
import time

from datetime import datetime, timedelta
from rpi_ws281x import *

LED_COUNT = 101  # First led out of 10/10
LED_BY_ROW = 10

LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
ONOFF_PIN = 5
MODE_PIN = 10

# index of first lestter by words
WORDS = {
    'IL': 1,
    'EST': 4,
    'DIX': 8,
    'QUATRE': 11,
    'CINQ': 17,
    'UNE': 21,
    'NEUF': 22,
    'TROIS': 26,
    'SEPT': 31,
    'DEUX': 37,
    'ONZE': 42,
    'HUIT': 47,
    'SIX': 51,
    'HEURE': 55,
    'HEURES': 55,
    'MINUIT': 61,
    'MIDI': 67,
    'MOINS': 71,
    'dIX': 78,
    'QUART': 81,
    'TRENTE': 85,
    'VINGT': 91,
    'cINQ': 97,
}

MODES = {
    'random': 15,
    'nowWords': 35,
    'nowFigures': 55,
}

HOURS_ORDERED = 'MINUIT UNE DEUX TROIS QUATRE CINQ SIX SEPT HUIT NEUF DIX ONZE MIDI'.split(' ')

FIGURES = {
    0: [1, 2, 3, 4, 11, 14, 21, 24, 31, 34, 41, 42, 43, 44],
    0: [2, 3, 11, 14, 21, 24, 31, 34, 42, 43],
    1: [3, 12, 13, 23, 33, 43],
    1: [12, 3, 13, 23, 33, 42, 43, 44],
    2: [1, 2, 3, 4, 14, 21, 22, 23, 24, 31, 41, 42, 43, 44],
    3: [1, 2, 3, 4, 14, 22, 23, 24, 34, 41, 42, 43, 44],
    4: [1, 4, 11, 14, 21, 22, 23, 24, 34, 44],
    5: [1, 2, 3, 4, 11, 21, 22, 23, 24, 34, 41, 42, 43, 44],
    6: [1, 2, 3, 4, 11, 21, 22, 23, 24, 31, 34, 41, 42, 43, 44],
    7: [1, 2, 3, 4, 14, 24, 34, 44],
    8: [1, 2, 3, 4, 11, 14, 21, 22, 23, 24, 31, 34, 41, 42, 43, 44],
    9: [1, 2, 3, 4, 11, 14, 21, 22, 23, 24, 34, 41, 42, 43, 44],
    'B': [1, 2, 3, 11, 14, 21, 22, 23, 31, 34, 41, 42, 43],
    'Y': [1, 4, 12, 14, 23, 32, 41],
    'E': [1, 2, 3, 4, 11, 21, 22, 23, 24, 31, 41, 42, 43, 44],
    ' ': [],
    '!': [2, 12, 22, 42],
}


def get_ip(split=' '):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip.split(split)


def round_minute_to_5(m):
    return int(round(m * 2 / 10) * 10 / 2)


def getWordsTime(dtime):
    # return list of word needed to display hours

    h, m = dtime.timetuple()[3:5]
    m = round_minute_to_5(m)  # transform 32 to 30, 33 to 35
    lights = ['IL', 'EST']

    # set hours
    isMidi = h in (11, 12, 13)
    if m <= 35:
        lights.append(HOURS_ORDERED[h % 12])
    else:
        lights.append(HOURS_ORDERED[(h + 1) % 12])

    if lights[-1] in ('MIDI', 'MINUIT'):
        if isMidi:
            lights[-1] = 'MIDI'
    else:
        if lights[-1] != "UNE":
            lights.append('HEURES')
        else:
            lights.append('HEURE')

    # set minute
    if m == 0:
        pass
    elif m <= 5:
        lights.append('cINQ')
    elif m <= 10:
        lights.append('dIX')
    elif m <= 15:
        lights.append('QUART')
    elif m <= 20:
        lights.append('VINGT')
    elif m <= 25:
        lights.append('VINGT')
        lights.append('cINQ')
    elif m <= 30:
        lights.append('TRENTE')
    elif m <= 35:
        lights.append('TRENTE')
        lights.append('cINQ')
    elif m <= 40:
        lights.append('MOINS')
        lights.append('VINGT')
    elif m <= 45:
        lights.append('MOINS')
        lights.append('QUART')
    elif m <= 50:
        lights.append('MOINS')
        lights.append('dIX')
    elif m <= 55:
        lights.append('MOINS')
        lights.append('cINQ')

    return lights


def getFiguresTime(dtime, hours_color=False, mins_color=False, rounding=False):
    # return list of number + offset to display dtime hours

    h, m = dtime.timetuple()[3:5]
    m = rounding and round_minute_to_5(m) or m  # transform 32 to 30, 33 to 35
    if m == 60:
        h += 1
        m = 0
    figs = []

    # hours
    hours_color = hours_color or MyPixelSquare.randcolor()
    figs.append((h // 10, 0, 0, hours_color))
    figs.append((h % 10, 6, 0, hours_color))

    # mins
    mins_color = mins_color or MyPixelSquare.randcolor()
    figs.append((m // 10, 0, 5, mins_color))
    figs.append((m % 10, 6, 5, mins_color))

    return figs


class MyPixelSquare(PixelStrip):
    # keep current display (figures or words to avoid refresh with random color)
    last_lights = []
    list_words = []
    list_figures = []
    led_by_row = 0

    def __init__(self, num, pin, brightness=255, gamma=None, words=[], figures=[], led_by_row=10):
        super().__init__(num, pin, brightness=255, gamma=None)
        self.list_words = words
        self.list_figures = figures
        self.led_by_row = led_by_row

    def clear(self):
        led = 0
        while led < self.numPixels():
            self.setPixelColorRGB(led, 0, 0, 0, 0)
            led += 1
        self.show()

    def lightWords(self, words, color=False):
        # words = list of word as string that exists in WORDS
        if not isinstance(words, type([])):
            words = [words]

        for w in words:
            word_color = color or self.randcolor()
            word_idx = self.list_words[w]
            for led in list(range(word_idx, word_idx + len(w))):
                self.setPixelColor(self.pos(led), word_color)
        self.show()

    def lightFigures(self, figures, glob_color=False):
        # figures = [(figure, offsetX, offsetY, color)]
        if not isinstance(figures, type([])):
            figures = [figures]

        for f, offsetX, offsetY, color in figures:
            fig = map(lambda i: i + offsetX + (offsetY * self.led_by_row), self.list_figures[f])
            randcol = self.randcolor()
            for led in fig:
                self.setPixelColor(self.pos(led), glob_color or color or randcol)
        self.show()

    def nowWords(self):
        words = getWordsTime(datetime.now())
        if words != self.last_lights:
            self.last_lights = words
            self.clear()
            self.lightWords(words)
            print(words)

    def nowFigures(self):
        figs = getFiguresTime(datetime.now() + timedelta(minutes=0), rounding=False)
        # ignore refresh if just color is != (color is random)
        if len(figs) != len(self.last_lights) or any(filter(lambda f: f[0][:2] != f[1][:2], zip(figs, self.last_lights))):
            print(datetime.now(), '->', figs)
            self.last_lights = figs
            self.clear()
            self.lightFigures(figs)

    def sayBye(self):
        for char in 'BYE !':
            self.clear()
            self.lightFigures((char, 3, 3, False))
            self.show()
            time.sleep(0.4)
        time.sleep(2)
        self.clear()

    def rainbow(self, wait_ms=10, iterations=1):
        for j in range(256 * iterations):
            for i in range(self.numPixels()):
                self.setPixelColor(self.pos(i), self.wheel((i + j) & 255))
            self.show()
            time.sleep(wait_ms / 1000.0)

    # Helper
    @staticmethod
    def randcolor():
        return Color(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            white=0,  # random.randint(0, 1),
        )

    @staticmethod
    def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def pos_from_alim(self, i):
        # return the pos, with alim on bottom right
        #
        #    9  8  7 \
        #  / 4  5  6 /
        #  \ 3  2  1 - 0 --ALIM
        assert i >= 0
        n = i

        # 20/40/60/...
        if (i % self.led_by_row == 0):
            if (i // self.led_by_row) % 2 == 0:
                n = (i // self.led_by_row) * self.led_by_row - 9
        elif (i // self.led_by_row) % 2 == 1:  # if line even
            n = (i // self.led_by_row) * self.led_by_row + (self.led_by_row - (i % self.led_by_row))
            n += 1
        return n

    def pos(self, i):
        # return the pos, from the matrix
        #
        #  1  2  3
        #  4  5  6
        #  7  8  9
        return self.pos_from_alim(self.numPixels() - i)
