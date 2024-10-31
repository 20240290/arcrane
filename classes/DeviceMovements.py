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
 limitations under
 """

from gpiozero import OutputDevice
from time import sleep
import constants as const
from classes.PWMStepperMotor import PWMStepperMotor

""" Device movements class that will holds the motors added."""

class DeviceMovements:
    #motor = PWMStepperMotor()
    used_pins = set() #track used pins
    def __init__(self, step: int, drive: int, direction_forward=True):
        """Initialize movement coordinates."""
        self.x = 0
        self.y = 0

        print(f"self.is_pin_in_use {self.is_pin_in_use}")
        self.step = step
        self.drive = drive
        self.direction = direction_forward
        self.motor = PWMStepperMotor(step, drive, direction_forward)
        

    def setDeviceOutput(self):
        """ Set Device Output """
        pass
        # self.motor.setMotor(step=self.step,
        #                     drive=self.drive, 
        #                     direction_forward=self.direction)

    def move_up(self, distance=1):
        """Move up by a specified distance."""
        self.y += distance
        return self.get_position()

    def move_down(self, distance=1):
        """Move down by a specified distance."""
        self.y -= distance
        return self.get_position()

    def move_left(self, distance=1):
        """Move left by a specified distance."""
        self.x -= distance
        self.motor.rotate_motor()
        return self.get_position()

    def move_right(self, distance=1):
        """Move right by a specified distance."""
        self.x += distance

        self.motor.rotate_motor()

        return self.get_position()

    def get_position(self):
        """Return the current position as a tuple (x, y)."""
        return (self.x, self.y)
    
    def is_pin_in_use(self, pin):
        return pin in self.used_pins

    def add_pin(self, pin):
        self.used_pins.add(pin)

    def remove_pin(self, pin):
        self.used_pins.discard(pin)
