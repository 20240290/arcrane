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
from classes.CustomButton import CustomButton

""" Device movements class that will holds the motors added."""

class DeviceMovements:
    movements = {}
    down_movement: CustomButton
    up_movement: CustomButton
    right_movement: CustomButton
    left_movement: CustomButton
    trigger_button: CustomButton
    fire_button: CustomButton

    directional_movements = []
    button_registry = {}
    motor_registry = {}

    def __init__(self, 
                 step: int, 
                 drive: int,
                 movements: dict,
                 pins: list,
                 direction_forward=True):
        self.step = step
        self.drive = drive
        self.direction = direction_forward
        self.motor = PWMStepperMotor(step, drive, direction_forward) #used for the simulator
        self.pins = pins
        self.movements = movements

    #set up movements configured in the joystick    
    def setUpMovements(self): 
        for devices in self.pins:
            for key, value in devices.items():
                self.addMovement(key, value)
                    
    def addMovement(self, 
                     movement: str, 
                     pin: int):
        #self.movements[movement] = Button(pin, pull_up=True)
        print(f"movement: {movement}")
        if movement == 'right':
            self.right_movement = CustomButton(pin, tag=movement, pull_up=True) #Button(pin, pull_up=True)
        elif movement == 'down':
            self.down_movement = CustomButton(pin, tag=movement, pull_up=True) #Button(pin, pull_up=True)
        elif movement == 'up':
            self.up_movement = CustomButton(pin, tag=movement, pull_up=True) #Button(pin, pull_up=True)
        elif movement == 'left':
            self.left_movement = CustomButton(pin, tag=movement, pull_up=True) #Button(pin, pull_up=True)        

    def monitorMovements(self):
       print(f"self.movements : {self.movements}")
       while True:
           if self.down_movement.is_active:
                #self.motor.rotate_motor()
                down_motor: PWMStepperMotor = self.get_motor_by_tag(self.down_movement.tag)
                down_motor.rotate_motor()
           elif self.right_movement.is_active:
                #self.motor.rotate_motor()
                right_motor: PWMStepperMotor = self.get_motor_by_tag(self.right_movement.tag)
                right_motor.rotate_motor()
           elif self.up_movement.is_active:
                #self.motor.rotate_motor()
                up_motor: PWMStepperMotor = self.get_motor_by_tag(self.up_movement.tag)
                up_motor.rotate_motor()
           elif self.left_movement.is_active:
               #self.motor.rotate_motor()
               left_motor: PWMStepperMotor = self.get_motor_by_tag(self.right_movement.tag)
               left_motor.rotate_motor()
        # while True:
        #    if self.down_movement.is_active:
        #         down_motor: PWMStepperMotor = self.get_motor_by_tag(self.down_movement.tag)
        #         down_motor.rotate_motor()
        #    elif self.right_movement.is_active:
        #         self.motor.rotate_motor()
        #    elif self.up_movement.is_active:
        #         _motors = self.get_motor_by_tag(self.up_movement.tag)
        #         if len(_motors) > 1:
        #             #have to manually check the motors added minimum of 2 motors  
        #             if self.valid_index(_motors, 0):
        #                 motor1: PWMStepperMotor = _motors[0]
        #                 motor1.rotate_motor()
        #             if self.valid_index(_motors, 1):
        #                 motor2: PWMStepperMotor = _motors[1]
        #                 motor2.rotate_motor()    
        #         else:
        #             up_motor: PWMStepperMotor = _motors[0]
        #             up_motor.rotate_motor()    
        #    elif self.left_movement.is_active:
        #        self.motor.rotate_motor()                       
                
    def configureMovement(self):
        if "pins" in self.movements:
            joystick = self.movements.get('pins')
            print(f"joystick pins: {joystick}")
            for k,v in joystick.items():
                print(f"device:  {v}")
                self.addMovement(k,v)
        if "motors" in self.movements:
            motors = self.movements.get('motors')
            for item in motors:
                print(f"motors : {item.get('step')}")
                self.register_motor(item.get('movement'), PWMStepperMotor(item.get('step'), 
                                                                          item.get('drive'),
                                                                          item.get('direction')))
                # this code needs to be tested
                # if item.get('movement') in self.motor_registry:
                #     _motors = self.motor_registry.get(item.get('movement'))
                #     _motors += PWMStepperMotor(item.get('step'), 
                #                               item.get('drive'),
                #                               item.get('direction'))
                # else:    
                #     self.register_motor(item.get('movement'), [PWMStepperMotor(item.get('step'), 
                #                                                               item.get('drive'),
                #                                                               item.get('direction'))])
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
    
    def valid_index(lst, index):
        try:
            lst[index] 
            return True 
        except IndexError:
            return False

    # Function to register a button
    def register_button(self, tag, button):
        if tag in self.button_registry:
            print(f"Warning: Button with tag '{tag}' already exists.")
        else:
            self.button_registry[tag] = button

    # Function to get a button by its tag
    def get_button_by_tag(self, tag):
        return self.button_registry.get(tag)
    
    # Function to register a button
    def register_motor(self, tag, motor):
        if tag in self.motor_registry:
            print(f"Warning: Motor with tag '{tag}' already exists.")
        else:
            self.motor_registry[tag] = motor

    # Function to get a button by its tag
    def get_motor_by_tag(self, tag):
        return self.motor_registry.get(tag)

