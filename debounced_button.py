from machine import Pin
import time

BOUNCING_MAX_DELTA_MS = 200


class DebouncedButton():
    def __init__(self, id, pull, trigger, callback):
        self._pin = Pin(id, Pin.IN, pull)
        self._callback = callback

        self._last_pressed_timestamp = time.ticks_ms()
        self._pin.irq(lambda btn: self._on_press(btn), trigger)

    def _on_press(self, btn):
        now = time.ticks_ms()

        diff = time.ticks_diff(now, self._last_pressed_timestamp)
        if (diff < BOUNCING_MAX_DELTA_MS):
            return

        self._last_pressed_timestamp = now
        self._callback(btn)
