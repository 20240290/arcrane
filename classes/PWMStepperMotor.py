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
import Directions as direction
import constants as const

""" Generic Stepper Motor Class """

class PWMStepperMotor():

    def __init__(self, step: int, drive: int, direction_forward=True):
        """
        Default Class initializer with that accepts the Output device pin.

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
        self.direction = direction_forward

    #    def rotate_motor(step_pin, dir_pin, direction_forward=True):
    # """Rotate the specified motor one step."""
    # dir_pin.value = direction_forward
    # step_pin.on()
    # sleep(step_delay)
    # step_pin.off()
    # sleep(step_delay) 

    # if key == curses.KEY_LEFT:
    #         stdscr.addstr(f"Rotating Motor {current_motor} counterclockwise (continuous)\n")
    #         row_count += 1
    #         if current_motor == 1:
    #             rotate_motor(motor1_step, motor1_dir, direction_forward=False)
    #         elif current_motor == 2:
    #             rotate_motor(motor2_step, motor2_dir, direction_forward=False)
    #         elif current_motor == 3:
    #             rotate_motor(motor3_step, motor3_dir, direction_forward=False)
    #         elif current_motor == 4:
    #             rotate_motor(motor4_step, motor4_dir, direction_forward=False)

    # Set up the GPIO pins for each motor
    # motor1_step = OutputDevice(M1_STEP_PIN)
    # motor1_dir = OutputDevice(M1_DIR_PIN)

    # motor2_step = OutputDevice(M2_STEP_PIN)
    # motor2_dir = OutputDevice(M2_DIR_PIN)

    # motor3_step = OutputDevice(M3_STEP_PIN)
    # motor3_dir = OutputDevice(M3_DIR_PIN)

    # motor4_step = OutputDevice(M4_STEP_PIN)
    # motor4_dir = OutputDevice(M4_DIR_PIN)


    
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
        self.motor_dir.value = self.direction
        self.motor_step.on()
        sleep(const.STEP_DELAY)
        self.motor_step.off()
        sleep(const.STEP_DELAY)