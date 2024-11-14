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

from gpiozero import Servo
from time import sleep
import constants as const

class PWMServoMotor():
        #add a tag to the motor
    def __init__(self, pin: int):
        """
        Default Class initializer with that accepts the Servo device pin.

        Parameters:
        -----------
        None

        Return:
        -------
        None
        """
        
        self.motor_servo = Servo(pin)
    
    def rotate_motor(self, pos: int):
        """
        Rotate the specified motor by position.

        Parameters:
        -----------
        pos: int
            - Position of the servo.

        Return:
        -------
        None
        """
        """"""
        # if pos == 1:
        #     self.motor_servo.min()
        # elif pos == 2:
        #     self.motor_servo.mid()
        # elif pos == 3:
        #     self.motor_servo.max()    
        # sleep(const.SERVO_DELAY)
        self.motor_servo.min()  # Move to min position (e.g., -90 degrees)
        sleep(1)
        self.motor_servo.mid()  # Move to middle position (e.g., 0 degrees)
        sleep(1)
        self.motor_servo.max()  # Move to max position (e.g., +90 degrees)
        sleep(1)
    

    