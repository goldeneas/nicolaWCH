from machine import Pin
from debounced_button import DebouncedButton

class InputSystem:
    def __init__(self):
        self._callback_dict = {}
        self._event_dict = {}

    def register_input(self, pin_id: str, event_name: str, trigger = Pin.IRQ_RISING):
        if pin_id in self._callback_dict:
            self._event_dict[pin_id].append(event_name)
            return

        self._event_dict[pin_id] = [event_name]

        DebouncedButton(pin_id, Pin.PULL_DOWN, trigger,
                        lambda pin: self._execute_callback(pin, event_name))

    def register_callback(self, event_name: str, callback):
        if event_name in self._callback_dict:
            print("ALREADY PRESENT")
            self._callback_dict[event_name].append(callback)
            return

        self._callback_dict[event_name] = [callback]

    def _execute_callback(self, pin, event_name):
        callbacks = self._callback_dict[event_name]

        for callback in callbacks:
            print("ITER")
            callback(pin)

