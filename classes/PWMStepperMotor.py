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
from gpiozero import OutputDevice
from time import sleep
import constants as const
import Utilities as utilities

class PWMStepperMotor():
    """
    Stepper motor class that will holds the motors added.
    
    Args:
    -----------
    None    
    
    Return:
    -------
    None
    """
    motor_step: OutputDevice
    motor_dir: OutputDevice
    reversable: bool
    reverse_movement: str
    utility = utilities.Utilities()

    #add a tag to the motor
    def __init__(self, 
                 step: int, 
                 drive: int, 
                 direction_forward=True, 
                 reversable=False, 
                 reverse_movement = '', 
                 movement = ''):
        """
        Stepper motor class initializer that accepts the Output device pin.

        Args:
        -----------
        step: int
            The motor pin.
        drive: int
            The drive pin.
        direction_forward: boolean
            Boolean flag to determine the motor direction, clockwise & counter clockwise.
        reversable: boolean           
            Boolean flag to determine if the motor is reversable.
        reverse_movement: str
            Reverse movement of the motor.
        movement: str
            The movement associated of the motor.    

        Return:
        -------
        None
        """
        self.motor_step = OutputDevice(step)
        self.motor_dir = OutputDevice(drive)
        self.step = step
        self.drive = drive
        self.direction_forward = direction_forward
        self.reversable = reversable
        self.reverse_movement = reverse_movement
        self.movement = movement
        if movement == 'forward' or movement == 'backward':
            self.motor_delay = self.utility.get_configuration('claw_step_delay')
        else:   
            self.motor_delay = self.utility.get_configuration('step_delay')

    def setMotor(self, step: int, drive: int, direction_forward=True):
        """
        Setup and pin out output device.

        Args:
        -----------
        step: int
            - stepper pin value.
        drive: int
            - drive pin value.
        direction_forward: bool
            - direction of the motor.

        Return:
        -------
        None
        """
        self.motor_step = OutputDevice(step)
        self.motor_dir = OutputDevice(drive)
        self.direction_forward = direction_forward

    
    def rotate_motor(self):
        """
        Rotate the specified motor one step.

        Args:
        -----------
        None

        Return:
        -------
        None
        """
        """"""
        self.motor_dir.value = self.direction_forward
        self.motor_step.on()
        sleep(self.motor_delay)
        self.motor_step.off()
        sleep(self.motor_delay)

    def rotate_motor2(self, direction):
        """
        Rotate the specified motor one step.

        Args:
        -----------
        direction: boolean
            Boolean flag to determine the motor direction, clockwise & counter clockwise.

        Return:
        -------
        None
        """
        self.motor_dir.value = direction
        self.motor_step.on()
        sleep(float(self.motor_delay))
        self.motor_step.off()
        sleep(float(self.motor_delay))

    def runMotor(self, run: bool):
        """
        Turn on & off the motor.

        Args:
            run (boolean) : Start or stop the motor movement.

        Returns:
            None
        """
        if run:
            self.motor_step.on()
        else:
            self.motor_step.off()        
