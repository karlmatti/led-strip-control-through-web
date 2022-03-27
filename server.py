from flask import Flask, render_template
import time
from rpi_ws281x import PixelStrip, Color

app = Flask(__name__)
strip = PixelStrip(60, 18, 800000, 10, False, 150, 0)
strip.begin()


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def clearWipe():
    colorWipe(strip, Color(0, 0, 0), 10)


def showColorWipes():
    colorWipe(strip, Color(255, 0, 0))  # Red wipe
    colorWipe(strip, Color(0, 255, 0))  # Green wipe
    colorWipe(strip, Color(0, 0, 255))  # Blue wipe
    clearWipe()


def showTheatherChases():
    theaterChase(strip, Color(127, 127, 127))  # White theater chase
    theaterChase(strip, Color(127, 0, 0))  # Red theater chase
    theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
    clearWipe()


def showRainbowEffects():
    rainbow(strip)
    rainbowCycle(strip)
    theaterChaseRainbow(strip)
    clearWipe()


def runAll():
    showColorWipes()
    showTheatherChases()
    showRainbowEffects()


@app.route('/', methods=['GET'])
def fetchForm():
    return render_template('form.html')


@app.route('/show/<effect>', methods=['POST'])
def submitForm(effect):
    if effect == 'wipe':
        showColorWipes()
    elif effect == 'theather':
        showTheatherChases()
    elif effect == 'rainbow':
        showRainbowEffects()
    else:
        abort(404)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
