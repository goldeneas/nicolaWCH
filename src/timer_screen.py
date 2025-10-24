import watch
from machine import ADC, Pin
from builtins import min
from debounced_button import DebouncedButton

class TimerScreen:
    def __init__(self, watch: watch.Watch):
        self._watch = watch
        self._timer_knob = ADC("PA0")
        self._time_btn = DebouncedButton("PB14", Pin.PULL_DOWN, Pin.IRQ_RISING,
                                         self.cycle_time_units)

        # hrs, mins, secs
        self._timer_units = [0, 0, 0]
        self._timer_units_idx = 0

    def update(self):
        value = int(self._timer_knob.read_u16() / 1000)
        value = min(value, 60)

        self._timer_units[self._timer_units_idx] = value

    def draw(self):
        display = self._watch.get_display()
        hours = self._timer_units[0]
        minutes = self._timer_units[1] 
        seconds = self._timer_units[2] 

        display.fill(0)
        display.large_text(f"{hours:02d}:{minutes:02d}:{seconds:02d}", 0, 32, 2)
        display.rect(0, 118, 128, 10, 1, True)
        display.text("Timer Screen", 18, 120, 0)
        display.update()

    def on_wake(self):
        pass

    def on_sleep(self):
        pass

    def can_sleep(self):
        return False

    def cycle_time_units(self, btn):
        self._timer_units_idx = (self._timer_units_idx + 1) % len(self._timer_units)

