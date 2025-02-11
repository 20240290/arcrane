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
from gpiozero import OutputDevice
from gpiozero import Button
import time
from signal import pause
from adafruit_servokit import ServoKit

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MqttClient import MqttClient

# Initialize PCA9685 (16-channel PWM)
kit = ServoKit(channels=16)


claw = 0  # claw channel
claw_rotation = 1 # claw rotation channel


def move_motor(channel, target_angle, step=1, delay=0.01):
    current_angle = kit.servo[channel].angle or 0  # Get current angle or default to 0
    step = step if target_angle > current_angle else -step  # Adjust step direction
    
    for angle in range(int(current_angle), target_angle + step, step):
        kit.servo[channel].angle = angle
        time.sleep(delay)
    
    kit.servo[channel].angle = None  # Disable signal to prevent noise

def open_claw(channel, angle):
    """Opens the claw by setting the servo to the open angle."""
    move_motor(channel, angle)  # Adjust as needed

def close_claw(channel, object_width):
    """Closes the claw by setting the servo to the closed angle."""
    # move_motor(channel, angle)  # Adjust based on grip strength
    max_close_angle = 90  # Maximum closing angle
    min_close_angle = 120  # Minimum closing angle for smaller objects
    target_angle = max(min_close_angle, min(max_close_angle, object_width * 2))  # Scale width to angle
    move_motor(channel, target_angle)

def on_message_received(client, userdata, message):
    print(f"command: {message.payload.decode()} on topic: {message.topic}")
    command = message.payload.decode()
    if command == "open_claw":
        open_claw(claw, 35)
    elif command == "close_claw": 
        #close_claw(claw, 120)
        object_widths = [10, 20, 30] 
        for width in object_widths:
            close_claw(claw, width)
            time.sleep(1)
    elif command == "rotate_left":
        move_motor(claw_rotation, 0)
        time.sleep(1)
        move_motor(claw_rotation, 90)
        time.sleep(1)
        move_motor(claw_rotation, 180)
    elif command == "rotate_right":
        move_motor(claw_rotation, 90)
        time.sleep(1)
        move_motor(claw_rotation, 0)    


# Instantiate MqttClient with custom callback
client = MqttClient("localhost","raspberry/signal", isBackground=False, on_message=on_message_received)

def main():
    print ('Program is starting...')
    try:
        pass
    except KeyboardInterrupt:
       client.disconnect()
       print("Ending program")

if __name__ == "__main__":
    main()

