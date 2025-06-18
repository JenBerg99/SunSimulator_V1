import time
import threading
from adafruit_pixelbuf import PixelBuf
import board
from adafruit_raspberry_pi5_neopixel_write import neopixel_write
from cache import cache 

NEOPIXEL = board.D23
NUM_PIXELS = 100

# Custom PixelBuf for Raspberry Pi 5
class Pi5Pixelbuf(PixelBuf):
    def __init__(self, pin, size, **kwargs):
        self._pin = pin
        super().__init__(size=size, **kwargs)

    def _transmit(self, buf):
        neopixel_write(self._pin, buf)

pixels = Pi5Pixelbuf(NEOPIXEL, NUM_PIXELS, auto_write=True, byteorder="GRB")

def update_led_loop(interval: float = 1.0):
    """
    Periodically reads sunlight properties from the cache
    and updates the LED strip accordingly.
    """
    while True:
        sunlight = cache.get_sunlight_properties()
        rgb = sunlight.rgb_color
        brightness = sunlight.brightness_percent / 100.0

        pixels.brightness = brightness
        pixels.fill(rgb)
        time.sleep(interval)

def start_led_thread():
    """
    Starts the LED update loop in a background thread.
    """
    t = threading.Thread(target=update_led_loop, daemon=True)
    t.start()

def shutdown_led():
    """
    Turns off the LED Strip
    """
    pixels.fill((0,0,0))
    pixels.brightness = 0
    pixels.show()