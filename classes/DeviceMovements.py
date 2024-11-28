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

    joystick2_down_movement: CustomButton
    joystick2_up_movement: CustomButton
    joystick2_right_movement: CustomButton
    joystick2_left_movement: CustomButton
    joystick2_trigger_button: CustomButton
    joystick2_fire_button: CustomButton

    directional_movements = []
    button_registry = {}
    motor_registry = {}
    id = ""

    def __init__(self, 
                 movements: dict,
                 pins: list, 
                 id: str):
        self.pins = pins
        self.movements = movements
        self.id = id

    #set up movements configured in the joystick    
    def setCraneUpMovements(self): 
        """
        Setup the crane movements.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """

        for devices in self.pins:
            for key, value in devices.items():
                self.addMovement(key, value)
                    
    def addMovement(self, 
                     movement: str, 
                     pin: int):
        """
        Configure the joystick movements and its corresponding GPIO Button.

        Parameters:
        -----------
        movement: str
            Movement of indicator (up,down,left,right)
        pin: int
            GPIO pin    

        Return:
        -------
        None
        """

        #self.movements[movement] = Button(pin, pull_up=True)
        print(f"addMovement movement: {movement} pin : {pin}")
        #print(f"trigger button check {self.trigger_button}")
        print(f"device id: {self.id}")

        if self.id == "j1":
            if movement == 'right':
                self.right_movement = CustomButton(pin, tag=movement, id=self.id, pull_up=True)
            elif movement == 'down':
                self.down_movement = CustomButton(pin, tag=movement, id=self.id, pull_up=True)
            elif movement == 'up':
                self.up_movement = CustomButton(pin, tag=movement, id=self.id, pull_up=True)
            elif movement == 'left':
                self.left_movement = CustomButton(pin, tag=movement, id=self.id, pull_up=True)
            
        elif self.id == "j2":
            if movement == 'right':
                self.joystick2_right_movement = CustomButton(pin, tag=movement, id=self.id, pull_up=True)
            elif movement == 'down':
                self.joystick2_down_movement = CustomButton(pin, tag=movement, id=self.id, pull_up=True)
            elif movement == 'up':
                self.joystick2_up_movement = CustomButton(pin, tag=movement, id=self.id, pull_up=True)
            elif movement == 'left':
                self.joystick2_left_movement = CustomButton(pin, tag=movement, id=self.id, pull_up=True)
            elif movement == 'trigger':
                self.joystick2_trigger_button =  CustomButton(pin, tag=movement, id=self.id, pull_up=True)         
            elif movement == 'fire':
                self.joystick2_fire_button = CustomButton(pin, tag=movement, id=self.id, pull_up=True)    
    
    def monitorCraneMovements(self):
        """
        Monitor the crane movements.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        while True:
            if self.down_movement.is_active:
                print("down movement")
                #print(f"check down movement: {get_motor_by_tag(down_movement.tag)}")
                if self.get_motor_by_tag(self.down_movement.tag) != None:
                    _motors = self.get_motor_by_tag(self.down_movement.tag)
                    print("down more than 1")
                    if len(_motors) > 1:
                        #have to manually check the motors added minimum of 2 motors  
                        if self.valid_index(_motors, 0):
                            motor1: PWMStepperMotor = _motors[0]
                            if (motor1.reversable and  (self.down_movement.tag == motor1.reverse_movement)):
                                motor1.rotate_motor2(not motor1.direction_forward)
                            else:
                                motor1.rotate_motor2(motor1.direction_forward)

                        if self.valid_index(_motors, 1):
                            motor2: PWMStepperMotor = _motors[1]
                            if (motor2.reversable and (self.down_movement.tag == motor2.reverse_movement)):
                                motor2.rotate_motor2(not motor2.direction_forward)
                            else:
                                motor2.rotate_motor2(motor2.direction_forward)
                    else:
                        down_motor: PWMStepperMotor = _motors[0]
                        if (down_motor.reversable and (self.down_movement.tag == down_motor.reverse_movement)):
                            down_motor.rotate_motor2(not down_motor.direction_forward) 
                        else:
                            down_motor.rotate_motor2(down_motor.direction_forward)
            elif self.right_movement.is_active:
                print("right movement")
                if self.get_motor_by_tag(self.right_movement.tag) != None:
                    _motors = self.get_motor_by_tag(self.right_movement.tag)
                    if len(_motors) > 1:
                        print("right more than 1")
                        #have to manually check the motors added minimum of 2 motors  
                        if self.valid_index(_motors, 0):
                            motor1: PWMStepperMotor = _motors[0]
                            if (motor1.reversable and  (self.right_movement.tag == motor1.reverse_movement)):
                                motor1.rotate_motor2(not motor1.direction_forward)    
                            else:
                                motor1.rotate_motor2(motor1.direction_forward) 
                        if self.valid_index(_motors, 1):
                            motor2: PWMStepperMotor = _motors[1]
                            if (motor2.reversable and  (self.right_movement.tag == motor2.reverse_movement)):
                                motor2.rotate_motor2(not motor2.direction_forward)    
                            else:
                                motor2.rotate_motor2(motor2.direction_forward) 
                    else:
                        right_motor: PWMStepperMotor = _motors[0]
                        #print(f"right else: {right_motor.direction_forward} tag: {right_movement.tag}")
                        if (right_motor.reversable and  (self.right_movement.tag == right_motor.reverse_movement)):
                            right_motor.rotate_motor2(not right_motor.direction_forward)    
                        else:
                            right_motor.rotate_motor2(right_motor.direction_forward) 
            elif self.up_movement.is_active:
                    print("up movement")
                    if self.get_motor_by_tag(self.up_movement.tag) != None:
                        _motors = self.get_motor_by_tag(self.up_movement.tag)
                        if len(_motors) > 1:
                            print("up more than 1")
                            #have to manually check the motors added minimum of 2 motors  
                            if self.valid_index(_motors, 0):
                                motor1: PWMStepperMotor = _motors[0]
                                if (motor1.reversable and (self.up_movement.tag == motor1.reverse_movement)):
                                    motor1.rotate_motor2(not motor1.direction_forward)    
                                else:
                                    motor1.rotate_motor2(motor1.direction_forward) 
                            if self.valid_index(_motors, 1):
                                motor2: PWMStepperMotor = _motors[1]
                                if (motor2.reversable and  (self.up_movement.tag == motor2.reverse_movement)):
                                    motor2.rotate_motor2(not motor2.direction_forward)    
                                else:
                                    motor2.rotate_motor2(motor2.direction_forward) 
                        else:
                            up_motor: PWMStepperMotor = _motors[0]
                            #print(f"up else: {up_motor.direction_forward} tag: {up_movement.tag}")
                            if (up_motor.reversable and (self.up_movement.tag == up_motor.reverse_movement)):
                                up_motor.rotate_motor2(not up_motor.direction_forward)    
                            else:
                                up_motor.rotate_motor2(up_motor.direction_forward)    
                                
            elif self.left_movement.is_active:
                print("left movement")
                if self.get_motor_by_tag(self.left_movement.tag) != None:
                    _motors = self.get_motor_by_tag(self.left_movement.tag)
                    if len(_motors) > 1:
                        print("left more than 1")
                        #have to manually check the motors added minimum of 2 motors  
                        if self.valid_index(_motors, 0):
                            motor1: PWMStepperMotor = _motors[0]
                            if (motor1.reversable and  (self.left_movement.tag == motor1.reverse_movement)):
                                motor1.rotate_motor2(not motor1.direction_forward)    
                            else:
                                motor1.rotate_motor2(motor1.direction_forward) 
                        if self.valid_index(_motors, 1):
                            motor2: PWMStepperMotor = _motors[1]
                            if (motor2.reversable and  (self.left_movement.tag == motor2.reverse_movement)):
                                motor2.rotate_motor2(not motor2.direction_forward)    
                            else:
                                motor2.rotate_motor2(motor2.direction_forward) 
                    else:
                        left_motor: PWMStepperMotor = _motors[0]
                        #print(f"left else: {right_motor.left_movement} tag: {left_movement.tag}")
                        if (left_motor.reversable and  (self.left_movement.tag == left_motor.reverse_movement)):
                            left_motor.rotate_motor2(not left_motor.direction_forward)    
                        else:
                            left_motor.rotate_motor2(left_motor.direction_forward)  
            # elif self.trigger_button != None:
            #         if self.trigger_button.is_active:
            #             print(f"pingiw pingiw bang bang ") 
            # elif self.fire_button != None:
            #         if self.fire_button.is_active:
            #             print(f"fire in the hole")   

    def setUpClawMovements(self):
        """
        Setup the claw movements.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        if self.id == "j1":
            print("j1 joystick in action")
        elif self.id == "j2":
            print("j2 joystick in action")
    def configureClawMovement(self):
        """
        Configure the motors associated 

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        pass

    def monitorClawMovements(self):
        """
        Default Class initializer with that accepts the Output device pin.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        pass

    def monitorWebMovements(self, movement):
        print(f"Web movement: {movement}")
        if movement == 'down':
            print("down movement")
            #print(f"check down movement: {get_motor_by_tag(down_movement.tag)}")
            if self.get_motor_by_tag(movement) != None:
                _motors = self.get_motor_by_tag(movement)
                print("down more than 1")
                if len(_motors) > 1:
                    #have to manually check the motors added minimum of 2 motors  
                    if self.valid_index(_motors, 0):
                        motor1: PWMStepperMotor = _motors[0]
                        if (motor1.reversable and  (movement == motor1.reverse_movement)):
                            motor1.rotate_motor2(not motor1.direction_forward)
                        else:
                            motor1.rotate_motor2(motor1.direction_forward)

                    if self.valid_index(_motors, 1):
                        motor2: PWMStepperMotor = _motors[1]
                        if (motor2.reversable and  (movement == motor2.reverse_movement)):
                            motor2.rotate_motor2(not motor2.direction_forward)
                        else:
                            motor2.rotate_motor2(motor2.direction_forward)
                else:
                    down_motor: PWMStepperMotor = _motors[0]
                    if (down_motor.reversable and  (movement == down_motor.reverse_movement)):
                        down_motor.rotate_motor2(not down_motor.direction_forward) 
                    else:
                        down_motor.rotate_motor2(down_motor.direction_forward)
        elif movement == 'right':
                print("right movement")
                if self.get_motor_by_tag(movement) != None:
                    _motors = self.get_motor_by_tag(movement)
                    if len(_motors) > 1:
                        print("right more than 1")
                        #have to manually check the motors added minimum of 2 motors  
                        if self.valid_index(_motors, 0):
                            motor1: PWMStepperMotor = _motors[0]
                            if (motor1.reversable and  (movement == motor1.reverse_movement)):
                                motor1.rotate_motor2(not motor1.direction_forward)    
                            else:
                                motor1.rotate_motor2(motor1.direction_forward) 
                        if self.valid_index(_motors, 1):
                            motor2: PWMStepperMotor = _motors[1]
                            if (motor2.reversable and  (movement == motor2.reverse_movement)):
                                motor2.rotate_motor2(not motor2.direction_forward)    
                            else:
                                motor2.rotate_motor2(motor2.direction_forward) 
                    else:
                        right_motor: PWMStepperMotor = _motors[0]
                        #print(f"right else: {right_motor.direction_forward} tag: {right_movement.tag}")
                        if (right_motor.reversable and  (movement == right_motor.reverse_movement)):
                            right_motor.rotate_motor2(not right_motor.direction_forward)    
                        else:
                            right_motor.rotate_motor2(right_motor.direction_forward)   
        elif movement == 'up':
                print("up movement")
                if self.get_motor_by_tag(movement) != None:
                    _motors = self.get_motor_by_tag(movement)
                    if len(_motors) > 1:
                        print("up more than 1")
                        #have to manually check the motors added minimum of 2 motors  
                        if self.valid_index(_motors, 0):
                            motor1: PWMStepperMotor = _motors[0]
                            if (motor1.reversable and  (movement == motor1.reverse_movement)):
                                motor1.rotate_motor2(not motor1.direction_forward)    
                            else:
                                motor1.rotate_motor2(motor1.direction_forward) 
                        if self.valid_index(_motors, 1):
                            motor2: PWMStepperMotor = _motors[1]
                            if (motor2.reversable and  (movement == motor2.reverse_movement)):
                                motor2.rotate_motor2(not motor2.direction_forward)    
                            else:
                                motor2.rotate_motor2(motor2.direction_forward) 
                    else:
                        up_motor: PWMStepperMotor = _motors[0]
                        #print(f"up else: {up_motor.direction_forward} tag: {up_movement.tag}")
                        if (up_motor.reversable and  (movement == up_motor.reverse_movement)):
                            up_motor.rotate_motor2(not up_motor.direction_forward)    
                        else:
                            up_motor.rotate_motor2(up_motor.direction_forward)    
                            
        elif movement == 'left':
            print("left movement")
            # if self.get_motor_by_tag(self.left_movement.tag) != None:
            #         _motors = self.get_motor_by_tag(self.left_movement.tag)
            #         left_motor: PWMStepperMotor = _motors[0]
            #         left_motor.rotate_motor2(left_motor.direction_forward)
            if self.get_motor_by_tag(movement) != None:
                _motors = self.get_motor_by_tag(movement)
                if len(_motors) > 1:
                    print("left more than 1")
                    #have to manually check the motors added minimum of 2 motors  
                    if self.valid_index(_motors, 0):
                        motor1: PWMStepperMotor = _motors[0]
                        if (motor1.reversable and  (movement == motor1.reverse_movement)):
                            motor1.rotate_motor2(not motor1.direction_forward)    
                        else:
                            motor1.rotate_motor2(motor1.direction_forward) 
                    if self.valid_index(_motors, 1):
                        motor2: PWMStepperMotor = _motors[1]
                        if (motor2.reversable and  (movement == motor2.reverse_movement)):
                            motor2.rotate_motor2(not motor2.direction_forward)    
                        else:
                            motor2.rotate_motor2(motor2.direction_forward) 
                else:
                    print("left movement only one")
                    left_motor: PWMStepperMotor = _motors[0]
                    #print(f"left else: {right_motor.left_movement} tag: {left_movement.tag}")
                    if (left_motor.reversable and  (movement == left_motor.reverse_movement)):
                        left_motor.rotate_motor2(not left_motor.direction_forward)    
                    else:
                        left_motor.rotate_motor2(left_motor.direction_forward) 
        elif movement == 'trigger':
                print(f"pingiw pingiw bang bang ") 
        elif movement == 'fire':
                print(f"fire in the hole")                                
                
    def configureCraneMovement(self):
        
        if "motors" in self.movements:
            motors = self.movements.get('motors')
            for item in motors:
                print(f"motors : {item}")
                #this code needs to be tested
                movement = item.get('movement')
                print(f"configure movement is: {movement}")
                if movement in self.motor_registry:
                    _motors: list = self.motor_registry.get(movement)
                    print(f"number of motors with the same movement: { len(_motors) }")
                    if item.get('reversable'): 
                        reversible_motor = PWMStepperMotor(item.get('step'), item.get('drive'),item.get('direction'), item.get('reversable'), item.get('reverse_movement'), movement)
                        _motors.append(reversible_motor)
                        self.motor_registry[movement] = _motors

                        if item.get('reverse_movement') in self.motor_registry:
                            _reverseMotors: list = self.motor_registry.get(item.get('reverse_movement'))
                            _reverseMotors.append(reversible_motor)
                            self.motor_registry[movement] = _reverseMotors
                        print(f"number of motors with the same movement: { len(self.motor_registry.get(movement)) }")             
                    else:
                        #print(f"motor is not reversable: {item.get('movement')} with item : {item}")
                        _motors.append(PWMStepperMotor(item.get('step'), 
                                            item.get('drive'),
                                            item.get('direction'), 
                                            item.get('reversable'), 
                                            item.get('reverse_movement'), 
                                            item.get('movement')))
                        self.register_motor(item.get('movement'), _motors)                                             
                else:
                    print(f"does not exist") 
                    if item.get('reversable'): 
                        print(f"motor is reversable: {item.get('movement')} with item : {item}")
                        reversible_motor = PWMStepperMotor(item.get('step'), 
                                                        item.get('drive'),
                                                        item.get('direction'), 
                                                        item.get('reversable'),
                                                            item.get('reverse_movement'), 
                                                            movement)

                        self.register_motor(movement, [reversible_motor])
                        self.register_motor(item.get('reverse_movement'), [reversible_motor])
                                                                            
                    else:
                        print(f"motor is not reversable: {item.get('movement')} with item : {item}")     

                        self.register_motor(movement, [PWMStepperMotor(item.get('step'), 
                                                                            item.get('drive'),
                                                                            item.get('direction'), 
                                                                            item.get('reversable'), 
                                                                            item.get('reverse_movement'), 
                                                                            movement)])

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
    
    def valid_index(self,lst, index):
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

    def cleanupDevices(self):
        for k,v in self.motor_registry:
            if v is PWMStepperMotor:
                v.motor_step.off()
                v.motor_dir.off()