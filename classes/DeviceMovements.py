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

from gpiozero import Button
from time import sleep
import constants as const
from classes.PWMStepperMotor import PWMStepperMotor


""" Device movements class that will holds the motors added."""

class DeviceMovements:
    used_pins = set() #track used pins
    motors = {}
    movements = {}
    down_movement: Button
    up_movement: Button

    def __init__(self, 
                 step: int, 
                 drive: int, 
                 pins: list,
                 direction_forward=True):
        print(f"self.is_pin_in_use {self.is_pin_in_use}")
        self.step = step
        self.drive = drive
        self.direction = direction_forward
        self.motor = PWMStepperMotor(step, drive, direction_forward)
        self.pins = pins

    #set up movements configured in the joystick    
    def setUpMovements(self): 
        for devices in self.pins:
            for key, value in devices.items():
                self.addMovement(key, value)
                    
    def addMovement(self, 
                     movement: str, 
                     pin: int):
        #self.movements[movement] = Button(pin, pull_up=True)
        #  if movement == 'up':
        #      self.up_movement = Button(pin, pull_up=True)
        #  elif movement == 'down':
        self.down_movement = Button(pin, pull_up=True)

    def monitorMovements(self):
       print(f"self.movements : {self.movements}")
       while True:
           if self.down_movement.is_active:
                self.motor.rotate_motor()
                
            # for key, value in self.movements.items():
            #     print(f"movement value: {value}")
            #     if (key == 'up' & Button(value).is_active):
            #         print("Up pressed") 
            #     elif (key == 'down' & Button(value).is_active):
            #         print("Down pressed")    
            #     elif (key == 'left' & Button(value).is_active):
            #         print("Left pressed")   
            #     elif  (key == 'right' & Button(value).is_active):
            #         print("Right pressed")   
                
            
    def setDeviceOutput(self, motors: list):
        """ Set Device Output """
        for item in motors:
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
