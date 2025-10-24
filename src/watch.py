from clock import Clock
from machine import I2C, Pin
from mpu import MPU6500
from sh1107g import SH1107G
from time_screen import TimeScreen
from timer_screen import TimerScreen
from duck_screen import DuckScreen
from debounced_button import DebouncedButton
import time

SCREEN_SLEEP_DELTA_MS = 1000 * 3


class Watch:
    def __init__(self, mpu_address):
        self._i2c = I2C(1)
        self._clock = Clock()

        self._display = SH1107G(self.get_i2c())
        self._mpu = MPU6500(i2c=self.get_i2c(), address=mpu_address)

        self._screen_switch_btn = DebouncedButton("PB15", Pin.PULL_DOWN, Pin.IRQ_RISING,
                                                  self.cycle_screen)

        self._screen_cycle_idx = 0
        self._screen_list = [TimeScreen(self), TimerScreen(self), DuckScreen(self)]

        self.set_awake(True)
        self.set_screen(0)

    def update(self):
        screen = self.get_screen()
        screen.update()

        y_gyro = self.get_gyro()[1]

        if (not self.is_awake() and y_gyro > 2):
            screen.on_wake()
            self.set_awake(True)

        now = time.ticks_ms()
        can_sleep = screen.can_sleep()
        should_sleep = time.ticks_diff(now, self._last_wake_timestamp) > SCREEN_SLEEP_DELTA_MS 
        if (can_sleep and self.is_awake() and should_sleep):
            screen.on_sleep()
            self.set_awake(False)

        if (self.is_awake()):
            screen.draw()

    def cycle_screen(self, btn):
        self.set_awake(True)
        
        self._screen_cycle_idx += 1
        idx = self._screen_cycle_idx % len(self._screen_list)
        self.set_screen(idx)

    def set_awake(self, awake: bool):
        self._awake = awake
        self.get_display().set_power(awake)

        if (awake):
            self._last_wake_timestamp = time.ticks_ms()

    def is_awake(self):
        return self._awake

    def set_screen(self, idx: int):
        self._screen = self._screen_list[idx]

    def get_screen(self):
        return self._screen

    def get_temperature(self):
        return self.get_mpu().temperature
    
    def get_gyro(self):
        return self.get_mpu().gyro
    
    def get_acceleration(self):
        return self.get_mpu().acceleration

    def get_datetime(self):
        return self.get_clock().get_datetime()

    def set_datetime(self, datetime):
        self.get_clock().set_datetime(datetime)

    def get_i2c(self):
        return self._i2c

    def get_mpu(self):
        return self._mpu

    def get_display(self):
        return self._display

    def get_clock(self):
        return self._clock
