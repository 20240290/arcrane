from gpiozero import Button
from time import sleep

class CustomButton(Button):
    def __init__(self, pin, tag=str, **kwargs):
        super().__init__(pin, **kwargs)
        self.tag = tag
    
    def close(self):
        # Make sure to clean up the GPIO when done
        super().close()