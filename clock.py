from machine import RTC

# datetime tuple:(year, month, day, weekday, hours, minutes, seconds, subseconds) 


class Clock:
    """A class wrapping around the RTC found on the STM32F411"""

    def __init__(self):
        self._rtc = RTC()

    def rtc(self):
        return self._rtc

    def get_datetime(self):
        return self.rtc().datetime()

    def set_datetime(self, datetime):
        self.rtc().datetime(datetime)

    def set_alarm(self, id, time: int, repeat=False):
        self.rtc().alarm(id, time, repeat=repeat)

    def get_until_alarm(self, id):
        """Returns the milliseconds left before the alarm expires"""
        self.rtc().alarm_left(id)

    def cancel_alarm(self, id):
        self.rtc().alarm_cancel(id)

    def set_alarm_irq(self, wake, handler=None):
        '''
        Creates an IRQ triggered when the alarm goes off
            Parameters:
                handler (function): the function callback
                wake (enum): the sleep mode from where this interrupt can wake
                    up the system
        '''
        self.rtc().irq(trigger=RTC.ALARM0, handler=handler, wake=wake)
