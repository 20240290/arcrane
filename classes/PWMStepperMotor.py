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

""" Generic Stepper Motor Class """

class PWMStepperMotor():
    motor_step: OutputDevice
    motor_dir: OutputDevice
    reversable: bool
    reverse_movement: str
    utility = utilities.Utilities()


    #add a tag to the motor
    def __init__(self, step: int, drive: int, direction_forward=True, reversable=False, reverse_movement = ''):
        """
        Default Class initializer with that accepts the Output device pin.

        Parameters:
        -----------
        None

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
    
    def setMotor(self, step: int, drive: int, direction_forward=True):
        """
        Setup and pin out output device.

        Parameters:
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

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        """"""
        self.motor_dir.value = self.direction_forward
        self.motor_step.on()
        sleep(self.utility.get_configuration('step_delay'))
        self.motor_step.off()
        sleep(self.utility.get_configuration('step_delay'))
        # with self.motor_step as device, self.motor_dir as drive:  # Automatically cleans up on exit
        #     drive.value = self.direction_forward
        #     device.on()
        #     sleep(const.STEP_DELAY)
        #     device.off()

    def rotate_motor2(self, direction):
        """
        Rotate the specified motor one step.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        """"""
        self.motor_dir.value = direction
        self.motor_step.on()
        sleep(self.utility.get_configuration('step_delay'))
        self.motor_step.off()
        sleep(self.utility.get_configuration('step_delay'))
        # with self.motor_step as device, self.motor_dir as drive:  # Automatically cleans up on exit
        #     drive.value = self.direction_forward
        #     device.on()
        #     sleep(const.STEP_DELAY)
        #     device.off()