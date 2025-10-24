import watch

class TimeScreen:
    def __init__(self, watch: watch.Watch):
        self._watch = watch

    def update(self):
        pass

    def draw(self):
        datetime = self._watch.get_datetime()
        temp = self._watch.get_temperature()

        x_gyro, y_gyro, z_gyro = self._watch.get_gyro()
        x_accel, y_accel, z_accel = self._watch.get_acceleration()
    
        display = self._watch.get_display()
    
        hours = datetime[4]
        minutes = datetime[5]
        seconds = datetime[6]
    
        day = datetime[2]
        month = datetime[1]
        year = datetime[0]
    
        display.fill(0)
        display.large_text(f"{hours:02d}:{minutes:02d}:{seconds:02d}", 0, 32, 2)
        display.text(f"gyro", 0, 56)
        display.text(f"{x_gyro:03.1f} {y_gyro:03.1f} {z_gyro:03.1f}", 0, 66)
        display.text(f"accel", 0, 80)
        display.text(f"{x_accel:03.1f} {y_accel:03.1f} {z_accel:03.1f}", 0, 90)
        display.rect(0, 118, 128, 10, 1, True)
        display.text(f"{temp:04.1f}C", 0, 120, 0)
        display.text(f"{day:02d}/{month:02d}/{year:04d}/", 48, 120, 0)
        display.update()

    def on_wake(self):
        pass

    def on_sleep(self):
        pass

    def can_sleep(self):
        return True
