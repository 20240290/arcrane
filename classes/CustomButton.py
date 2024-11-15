from gpiozero import Button
from time import sleep

class CustomButton(Button):
    def __init__(self, pin, tag=None, **kwargs):
        super().__init__(pin, **kwargs)
        self.tag = tag

    def __str__(self):
        return f"Button {self.tag} on Pin {self.pin}"
