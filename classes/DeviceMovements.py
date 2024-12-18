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
import signal as signal
from classes.MicroSwitch import MicroSwitch
from classes.CallbackHandler import CallbackHandler

""" """

class DeviceMovements:
    """
    Device movements class that will holds the motors added.
    
    Parameters:
    -----------
    None    
    
    Return:
    -------
    None
    """
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

    mUpSwitch: MicroSwitch
    mDownSwitch: MicroSwitch
    mLeftSwitch: MicroSwitch
    mRightSwitch: MicroSwitch
    motor_registry = {}

    delegate = CallbackHandler()

    steps = 20
    ctr = 0
    
    def __init__(self, 
                 movements: dict,
                 pins: list, 
                id: str):
        """
        Class initializer for the arcrane movements.
        
        Parameters:
        -----------
        movement: dict
            Dictionary data and movements object.
        pins: list
            List of gpiozero pins.
        id: str
            Identifier of the object.    
        
        Return:
        -------
        None
        """  
        self.id = id
        self.movements = movements
        self.pins = pins
        self.setUpJoystickMovement(id)
        
    #set up movements configured in the joystick    
    def setUpJoystickMovement(self, id: str): 
        """
        Setup the joystick movements.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        print(f"setUpJoystickMovement : { id }")
        for devices in self.pins:
            for key, value in devices.items():
                self.addMovement(key, value, id)
                    
    def addMovement(self, 
                     movement: str, 
                     pin: int, 
                     id: str):
        """
        Configure the joystick movements and its corresponding GPIO Button.

        Parameters:
        -----------
        movement: str
            Movement of indicator (up,down,left,right)
        pin: int
            GPIO pin
        id: str
            Joystick identifier        

        Return:
        -------
        None
        """

        print(f"addMovement movement: {movement} pin : {pin} id: {self.id}")
        print(f"device id: {id}")

        if movement == 'right':
            self.right_movement = CustomButton(pin, tag=movement, id=id, pull_up=True)
        elif movement == 'down':
            self.down_movement = CustomButton(pin, tag=movement, id=id, pull_up=True)
        elif movement == 'up':
            self.up_movement = CustomButton(pin, tag=movement, id=id, pull_up=True)
        elif movement == 'left':
            self.left_movement = CustomButton(pin, tag=movement, id=id, pull_up=True)
        elif movement == 'sideR':
            self.joystick2_right_movement = CustomButton(pin, tag=movement, id=id, pull_up=True)
        elif movement == 'backward':
            self.joystick2_down_movement = CustomButton(pin, tag=movement, id=id, pull_up=True)
        elif movement == 'forward':
            self.joystick2_up_movement = CustomButton(pin, tag=movement, id=id, pull_up=True)
        elif movement == 'sideL':
            self.joystick2_left_movement = CustomButton(pin, tag=movement, id=id, pull_up=True)
        elif movement == 'trigger':
            self.joystick2_trigger_button =  CustomButton(pin, tag=movement, id=id, pull_up=True)         
        elif movement == 'fire':
            self.joystick2_fire_button = CustomButton(pin, tag=movement, id=id, pull_up=True)
        elif movement == 'up_stop_pin':
            self.mUpSwitch = MicroSwitch(pin)        
        elif movement == 'down_stop_pin':
            self.mDownSwitch = MicroSwitch(pin)
        elif movement == 'left_stop_pin':
            self.mLeftSwitch = MicroSwitch(pin)        
        elif movement == 'right_stop_pin':
            self.mRightSwitch = MicroSwitch(pin)      
    
    def monitorMovements(self):
        """
        Monitor the arcrane movements.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        #print(f"check motor registry : {self.motor_registry}")
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
                            if self.mDownSwitch.didPressed:
                                down_motor.runMotor(False)
                            else:
                                down_motor.rotate_motor2(not down_motor.direction_forward) 
                        else:
                            if self.mDownSwitch.didPressed:
                                down_motor.runMotor(False)
                            else:
                                down_motor.rotate_motor2(down_motor.direction_forward)    
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
                                    if self.mUpSwitch.didPressed:
                                        motor1.runMotor(False)
                                    else:
                                        motor1.rotate_motor2(not motor1.direction_forward)    
                                else:
                                    if self.mUpSwitch.didPressed:
                                        motor1.runMotor(False)
                                    else:    
                                        motor1.rotate_motor2(motor1.direction_forward) 
                            if self.valid_index(_motors, 1):
                                motor2: PWMStepperMotor = _motors[1]
                                if (motor2.reversable and  (self.up_movement.tag == motor2.reverse_movement)):
                                    if self.mUpSwitch.didPressed:
                                        motor2.runMotor(False)
                                    else:    
                                        motor2.rotate_motor2(not motor2.direction_forward)    
                                else:
                                    if self.mUpSwitch.didPressed:
                                        motor2.runMotor(False)
                                    else:    
                                        motor2.rotate_motor2(motor2.direction_forward) 
                        else:
                            up_motor: PWMStepperMotor = _motors[0]
                            if (up_motor.reversable and (self.up_movement.tag == up_motor.reverse_movement)):
                                if self.mUpSwitch.didPressed:
                                    up_motor.runMotor(False)
                                else:
                                    up_motor.rotate_motor2(not up_motor.direction_forward) 
                            else:
                                if self.mUpSwitch.didPressed:
                                    up_motor.runMotor(False)
                                else:
                                    up_motor.rotate_motor2(up_motor.direction_forward) 
     
            elif self.right_movement.is_active:
                print("right movement")
                if self.get_motor_by_tag(self.right_movement.tag) != None:
                    _motors = self.get_motor_by_tag(self.right_movement.tag)
                    
                    print(f"no of motors: {_motors}")
                    right_motor: PWMStepperMotor = _motors[0]

                    #need to have a special case where we need to stop the motors of the opposite direction for a single driver with 2 motors
                    left_motors = self.get_motor_by_tag(self.left_movement.tag)
                    print(f"_left_motors of motors: {left_motors}")
                    left_motor: PWMStepperMotor = left_motors[0]
                    
                    print(f"RIGHT MOTORS : {right_motor}")
                    if (right_motor.reversable and  (self.right_movement.tag == right_motor.reverse_movement)):
                        if self.mLeftSwitch.didPressed:
                            right_motor.runMotor(False)
                            left_motor.runMotor(False)
                        else:
                            right_motor.rotate_motor2(not right_motor.direction_forward)
                            left_motor.rotate_motor2(not left_motor.direction_forward)
                    else:
                        #print("RIGHT motor not reversible")
                        if self.mLeftSwitch.didPressed:
                            right_motor.runMotor(False)
                            left_motor.runMotor(False)
                        else:
                            right_motor.rotate_motor2(right_motor.direction_forward)   
                            left_motor.rotate_motor2(left_motor.direction_forward)          
            elif self.left_movement.is_active:
                print("left movement")
                if self.get_motor_by_tag(self.left_movement.tag) != None:
                    _motors = self.get_motor_by_tag(self.left_movement.tag)
                    left_motor: PWMStepperMotor = _motors[0]

                    right_motors = self.get_motor_by_tag(self.right_movement.tag)
                    print(f"_left_motors of motors: {right_motors}")
                    right_motor: PWMStepperMotor = right_motors[0]

                    if (left_motor.reversable and  (self.left_movement.tag == left_motor.reverse_movement)):
                        if self.mRightSwitch.didPressed:
                            left_motor.runMotor(False)
                            right_motor.runMotor(False)
                        else:
                            left_motor.rotate_motor2(not left_motor.direction_forward)
                            right_motor.rotate_motor2(not right_motor.direction_forward)
                    else:
                        if self.mRightSwitch.didPressed:
                            left_motor.runMotor(False)
                            right_motor.runMotor(False)
                        else:
                            left_motor.rotate_motor2(left_motor.direction_forward)
                            right_motor.rotate_motor2(right_motor.direction_forward)
            elif self.joystick2_down_movement.is_active:
                print("joystick 2 backward movement")
                #need to handle multiple motors per movements
                if self.get_motor_by_tag(self.joystick2_down_movement.tag) != None:
                    _motors = self.get_motor_by_tag(self.joystick2_down_movement.tag)
                    backward_motor: PWMStepperMotor = _motors[0]
                    if (backward_motor.reversable and  (self.joystick2_down_movement.tag == backward_motor.reverse_movement)):
                        backward_motor.rotate_motor2(not backward_motor.direction_forward)    
                        #self.moveMotorBySteps(not backward_motor.direction_forward, backward_motor, 20)
                    else:
                        backward_motor.rotate_motor2(backward_motor.direction_forward)
                        #self.moveMotorBySteps(backward_motor.direction_forward, backward_motor, 20)
                    print(f"counter movements: {self.ctr}")    
                
            elif self.joystick2_right_movement.is_active:
                self.delegate.notify_subscriber("movement", "TURN_CLAW_RIGHT")
                
            elif self.joystick2_up_movement.is_active:
                print("joystick 2 forward movement")
                if self.get_motor_by_tag(self.joystick2_up_movement.tag) != None:
                    _motors = self.get_motor_by_tag(self.joystick2_up_movement.tag)
                    foward_motor: PWMStepperMotor = _motors[0]
                    print(f"Forward MOTORS : {foward_motor}")
                    if (foward_motor.reversable and  (self.joystick2_up_movement.tag == foward_motor.reverse_movement)):
                        foward_motor.rotate_motor2(not foward_motor.direction_forward)    
                    else:
                        foward_motor.rotate_motor2(foward_motor.direction_forward)                
            elif self.joystick2_left_movement.is_active:
                print("jpystick 2 left movement")
                self.delegate.notify_subscriber("movement", "TURN_CLAW_LEFT")
            elif self.joystick2_trigger_button.is_active:
                print("jpystick 2 trigger movement")
                self.delegate.notify_subscriber("movement", "TRIGGER")
               
            elif self.joystick2_fire_button.is_active:
                print("jpystick 2 fire movement")
                self.delegate.notify_subscriber("movement", "FIRE")
                

    def moveMotorBySteps(self, direction, motor: PWMStepperMotor, steps):
        while self.ctr < steps:
            
            motor.rotate_motor2(direction) 
            self.ctr += 1
        else:
            print("should stop the motor ")    

    def monitorWebMovements(self, movement):
        """
        Monitor movements triggered from the web interface.

        Parameters:
        -----------
        movement: str
            Movement of the jouystick.

        Return:
        -------
        None
        """
        if movement == 'down':
            self.down_movement.is_active = True   
        elif movement == 'up':
            self.up_movement.is_active = True
        elif movement == 'left':
            self.left_movement.is_active = True
        elif movement == 'right':
            self.right_movement.is_active = True
        elif movement == 'backward':
            self.joystick2_down_movement.is_active = True
        elif movement == 'forward':
            self.joystick2_up_movement.is_active = True
        elif movement == 'sideR':
            self.joystick2_right_movement.is_active = True
        elif movement == 'sideL':
            self.joystick2_left_movement.is_active = True
        elif movement == 'trigger':
            self.joystick2_trigger_button.is_active = True
        elif movement == 'fire':
            self.joystick2_fire_button.is_active = True
                                                                           
    def configureMovement(self):
        """
        Configure the motors associated with the movement of the joystick.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        if "motors" in self.movements:
            motors = self.movements.get('motors')
            for item in motors:
                #print(f"motors : {item}")
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
                        print(f"motor is not reversable: {item.get('movement')} with item : {item}")
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
    
    def valid_index(self,lst, index):
        """
        Method to check if the index is valid inside a give list.

        Parameters:
        -----------
        lst: list
            The source array.
        index: int
            The index to check.    

        Return:
        -------
        Bool
            returns the bool value.
        """
        try:
            lst[index] 
            return True 
        except IndexError:
            return False

    
    # Function to register a button
    def register_motor(self, tag, motor):
        """
        Register a motor on a specific movement.

        Parameters:
        -----------
        tag: str
            Movement that the motor associated to.
        motor: PWMStepperMotor
            Stepper motor object.    

        Return:
        -------
        None
        """
        #print(f"registry : {self.motor_registry} register_motor motor tag :{tag}  id: {self.id}")
        #key = tag + self.id
        if tag in self.motor_registry:
            print(f"Warning: Motor with tag '{tag}' already exists.")
        else:
            self.motor_registry[tag] = motor

    # Function to get a button by its tag
    def get_motor_by_tag(self, tag):
        """
        Retrieve motor by the movement key

        Parameters:
        -----------
        tag: str
            Movement that the motor associated to.
        
        Return:
        -------
        motor: PWMStepperMotor
            Motor associated from the movement.
        """
        return self.motor_registry.get(tag)

    def cleanupDevices(self):
        """
        Turn off stepper motors.

        Parameters:
        -----------
        None
        
        Return:
        -------
        None
        """
        for k,v in self.motor_registry:
            if v is PWMStepperMotor:
                v.motor_step.off()
                v.motor_dir.off()