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

import sys
import threading
from gpiozero import Servo
from gpiozero import OutputDevice
import time
import paho.mqtt.client as mqtt
from Classes.ClawStepper import ClawStepper

# MQTT Broker configuration
BROKER = "localhost"  # Replace with your broker address
PORT = 1883
TOPIC = "raspberry/signal"  # Replace with your topic

motor_action = ""
#Claw rotation motor

motorPins = (18, 23, 24, 25)  # define pins connected to four phase ABCD of stepper motor
motors = list(map(lambda pin: OutputDevice(pin), motorPins))

clawMotorPins = (17, 27, 22, 10)  # define pins connected to four phase ABCD of stepper motor
clawMotors = list(map(lambda pin: OutputDevice(pin), clawMotorPins))

CCWStep = (0x01, 0x02, 0x04, 0x08)  # define power supply order for rotating anticlockwise
CWStep = (0x08, 0x04, 0x02, 0x01)   # define power supply order for rotating clockwise

maxStep = 20
def moveOnePeriod(direction, ms, motor): 
    if motor == "claw_movement":
        for j in range(0, 4, 1):  # cycle for power supply order
            for i in range(0, 4, 1):  # assign to each pin
                if direction == 1:  # power supply order clockwise
                    motors[i].on() if (CCWStep[j] == 1 << i) else motors[i].off()
                else:  # power supply order anticlockwise
                    motors[i].on() if CWStep[j] == 1 << i else motors[i].off()
            if ms < 3:  # the delay cannot be less than 3ms, otherwise it will exceed the motor's speed limit
                ms = 3
        time.sleep(ms * 0.001)
    else:
        for j in range(0, 4, 1):  # cycle for power supply order
            for i in range(0, 4, 1):  # assign to each pin
                if direction == 1:  # power supply order clockwise
                    motors[i].on() if (CCWStep[j] == 1 << i) else clawMotors[i].off()
                else:  # power supply order anticlockwise
                    motors[i].on() if CWStep[j] == 1 << i else clawMotors[i].off()
            if ms < 3:  # the delay cannot be less than 3ms, otherwise it will exceed the motor's speed limit
                ms = 3
        time.sleep(ms * 0.001)
        

def moveSteps(direction, ms, steps, motor):
    for _ in range(steps):
        moveOnePeriod(direction, ms, motor) 

def motorStop(motor):
    if motor == "claw_movement":
        for motor in motors:
            motor.off()
    else:
        for motor in clawMotors:
            motor.off()


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
            moveSteps(0, 1, 256, motor_action)  # Rotate clockwise for 128 steps
            time.sleep(0.1)
        elif movement == "TURN_CLAW_RIGHT":
            print("Rotating counter clockwise")
            moveSteps(1, 1, 256, motor_action)  # Rotate anticlockwise for 128 steps
            time.sleep(0.25)
        elif movement == "TRIGGER":
            print("trigger action")
            moveSteps(1, 5, 10, motor_action)  # Rotate anticlockwise 2
            time.sleep(0.25)
        elif movement == "FIRE":
            print("fire action")
            moveSteps(0, 5, 10, motor_action)  # Rotate faster clockwise 1
            time.sleep(0.25)
        elif movement == "STOP_MOTORS":
            #motorStop() 
            pass
        else:
            #motorStop() 
            pass
        

# Callback for connections
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

# Callback for received messages
def on_message(client, userdata, msg):

    print(f"Received: {msg.payload.decode()} on topic {msg.topic}")
    # command = msg.payload.decode()
    # moveMotor(command)
    moveSteps(0, 1, 256, "claw_movement")  # Rotate faster clockwise
    #time.sleep(0.1)

def process_message(msg):
    print(f"Received: {msg.payload.decode()} on topic {msg.topic}")
    #loop(msg.payload.decode())
def angle_to_servo(value):
    # Maps angle to the range that the servo can handle
    return (value / 90) - 1    

def startClient():
    client = mqtt.Client()
    client.enable_logger()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, 60)
        client.loop()  # Start network loop

    except KeyboardInterrupt:
        print("Disconnected from MQTT Broker.")
        client.disconnect()     

# MQTT client setup
client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)

def main():
    print ('Program is starting...')
    try:
        #messaging_thread = threading.Thread(target=startClient)
        #messaging_thread.start()
        #startClient()
        # moveMotor("TURN_CLAW_RIGHT")
         client.loop_forever()
    except KeyboardInterrupt:
        
       print("Ending program")


if __name__ == "__main__":
    main()

