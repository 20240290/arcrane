from gpiozero import Button
from time import sleep

class CustomButton(Button):
    # def __init__(self, pin, tag=str, **kwargs):
    #     super().__init__(pin, **kwargs)
    #     self.tag = tag
    
    # def close(self):
    #     # Make sure to clean up the GPIO when done
    #     super().close()

    # def __init__(self, pin, label, **kwargs):
    #     # Initialize the parent Button class
    #     super().__init__(pin, **kwargs)
    #     # Add a custom label attribute
    #     self.label = label

    # def __str__(self):
    #     # Override string representation to include the label
    #     return f"Button {self.label} (Pin {self.pin})"
    
    # def press_with_label(self):
    #     # Custom method that can be added to trigger actions with the label
    #     print(f"{self.label} button pressed!")
    def __init__(self, pin, tag=None, **kwargs):
        super().__init__(pin, **kwargs)
        self.tag = tag

    def __str__(self):
        return f"Button {self.tag} on Pin {self.pin}"
