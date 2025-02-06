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
import MqttClient
from signal import pause
from adafruit_servokit import ServoKit

#Claw action motor
def moveMotor(movement):
    print(f"LOOP movement {movement}")
    #flag motor by movement

    if movement == "TRIGGER" or movement == "FIRE":
        motor_action = "claw_grab"
    else:
        motor_action = "claw_movement" 

    #while True:
        #client.loop_start()
        if movement == "TURN_CLAW_LEFT":
            print("Rotating clockwise")
            #moveSteps(0, 1, 256, motor_action)  # Rotate clockwise for 128 steps
            time.sleep(0.1)
        elif movement == "TURN_CLAW_RIGHT":
            print("Rotating counter clockwise")
            #moveSteps(1, 1, 256, motor_action)  # Rotate anticlockwise for 128 steps
            time.sleep(0.25)
        elif movement == "TRIGGER":
            print("trigger action")
            #moveSteps(1, 5, 10, motor_action)  # Rotate anticlockwise 2
            time.sleep(0.25)
        elif movement == "FIRE":
            print("fire action")
            #moveSteps(0, 5, 10, motor_action)  # Rotate faster clockwise 1
            time.sleep(0.25)
        elif movement == "STOP_MOTORS":
            #motorStop() 
            pass
        else:
            #motorStop() 
            pass
        

# Callback for received messages
def on_message(msg):
    print(f"Received: {msg.payload.decode()} on topic {msg.topic}")
    # command = msg.payload.decode()
    # moveMotor(command)
    #moveSteps(0, 1, 256, "claw_movement")  # Rotate faster clockwise
    #time.sleep(0.1)

def process_message(msg):
    print(f"Received: {msg.payload.decode()} on topic {msg.topic}")
    #loop(msg.payload.decode())

def main():
    print ('Program is starting...')
    try:
        client = MqttClient.MqttClient("localhost","raspberry/signal")
        client.on_message = on_message
        client.subscribe_to_topic()

    except KeyboardInterrupt:
       client.disconnect()
       print("Ending program")


if __name__ == "__main__":
    main()

