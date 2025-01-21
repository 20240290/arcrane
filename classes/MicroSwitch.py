"""
 Copyright 2024 Resurgo

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to sys.path
sys.path.append(script_dir)

from gpiozero import Button
from time import sleep
import constants as const

class MicroSwitch():
    didPressed: bool
    def __init__(self, pin: int):
        """
        Class initializer that accepts the Servo device pin.

        Args:
            None

        Returns:
            None
        """
        
        self.switch = Button(pin)
        self.didPressed = False
        self.switch.when_pressed = self.on_button_released
        self.switch.when_released = self.on_button_pressed
    
    # Define the function to be called when the button is pressed
    def on_button_pressed(self):
        """
        Action when button is pressed.

        Args:
            None

        Returns:
            None
        """
        self.didPressed = True

    # Define the function to be called when the button is released
    def on_button_released(self):
        """
        Action when button is released.

        Args:
            None

        Returns:
            None
        """
        self.didPressed = False
        
    