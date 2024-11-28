from gpiozero import Button
from time import sleep

class CustomButton(Button):
    def __init__(self, pin, tag=None, id=None, **kwargs):
        super().__init__(pin, **kwargs)
        self.tag = tag
        self.id = id

    def __str__(self):
        return f"Button {self.tag} on Pin {self.pin} with ID {self.id}"
