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


import constants as const
import classes.DeviceMovements as movement
import time
import classes.MicroSwitch as switch
import signal as signal
import smbus
import time
import Utilities
import paho.mqtt.client as mqtt   

utility = Utilities.Utilities()

# MQTT broker details
BROKER = "resurgo2.local"  # Replace with the broker's IP address
TOPIC = "raspberry/signal"

# MQTT client setup
client = mqtt.Client()

client.connect(BROKER, port=1883, keepalive=60)
print("Connected to MQTT broker")
# Keep script running
client.loop_start()

class Arcrane:
    _instance = None
    is_portal: bool = False
   
    #class initializer
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(Arcrane, cls).__new__(cls)
    #         cls._instance.value = 0
    #     return cls._instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.arcrane = movement.DeviceMovements(
            id ='j1',
            movements = {
            'motors': [
                { # up / down movement
                'step': utility.get_configuration('m3_step_pin'), 
                'drive': utility.get_configuration('m3_dir_pin'), 
                'direction': True, 
                'reversable': utility.get_configuration('m3_reversible'), 
                'reverse_movement': utility.get_configuration('m3_reverse_movement'),
                'movement': utility.get_configuration('m3_movement')}, 
                {
                'step': utility.get_configuration('m1_step_pin'), 
                'drive': utility.get_configuration('m1_dir_pin'), 
                'direction': True, 
                'reversable': utility.get_configuration('m1_reversible'), 
                'reverse_movement': utility.get_configuration('m1_reverse_movement'),
                'movement': utility.get_configuration('m1_movement')}, 
                # {
                # 'step': utility.get_configuration('m4_step_pin'), 
                # 'drive': utility.get_configuration('m4_dir_pin'), 
                # 'direction': True, 
                # 'reversable': utility.get_configuration('m4_reversible'), 
                # 'reverse_movement': utility.get_configuration('m4_reverse_movement'),
                # 'movement': utility.get_configuration('m4_movement')}, 
                {
                'step': utility.get_configuration('m2_step_pin'), 
                'drive': utility.get_configuration('m2_dir_pin'), 
                'direction': True, 
                'reversable': utility.get_configuration('m2_reversible'), 
                'reverse_movement': utility.get_configuration('m2_reverse_movement'),
                'movement': utility.get_configuration('m2_movement')}
                ]},
            pins=[{'down': utility.get_configuration('j1_down_pin'), 
                    'right': utility.get_configuration('j1_right_pin'), 
                    'up': utility.get_configuration('j1_up_pin'), 
                    'left': utility.get_configuration('j1_left_pin'), 
                    'backward': utility.get_configuration('j2_backward_pin'), 
                   'sideR': utility.get_configuration('j2_sideR_pin'), 
                   'forward': utility.get_configuration('j2_forward_pin'), 
                   'sideL': utility.get_configuration('j2_sideL_pin'), 
                   'trigger': utility.get_configuration('j2_trigger_pin'), 
                   'fire': utility.get_configuration('j2_fire_pin'), 
                   'up_stop_pin': utility.get_configuration('crane_up_stop_pin'),
                   'down_stop_pin': utility.get_configuration('crane_down_stop_pin'),
                   'left_stop_pin': utility.get_configuration('crane_move_left_stop_pin'),
                   'right_stop_pin': utility.get_configuration('crane_move_right_stop_pin'),
                   }])
        print(f"self.joystick1 {self.arcrane.pins}")
    
    def setupMovementJoystick2(self):
        print("setupMovementJoystick2 and monitor movements")

    
    def setUpMovements(self):
        print("setUpMovements and monitor movements")
        self.arcrane.delegate.register_subscriber("movement", self.receive_message)
        self.arcrane.configureMovement()
        self.arcrane.monitorMovements() 
        #client.publish(TOPIC, "MAKE THE MOTOR MOVE")

    def receive_message(self, message):
        print(f"Delegate message received: {message}")
        client.publish(TOPIC, message)

    
    def initializeI2c():
        # Create an SMBus instance
        bus = smbus.SMBus(1)  # Use 1 for Raspberry Pi (newer models)

        SLAVE_ADDRESS = 0x04  # Replace with the actual address of the slave

        try:
            while True:
                # Send data
                data = [0x01, 0x02, 0x03]  # Example data
                bus.write_i2c_block_data(SLAVE_ADDRESS, 0, data)
                print("Sent:", data)
                time.sleep(1)  # Send every second
        except KeyboardInterrupt:
            pass

    def testSwitch():    
        mSwitch = switch.MicroSwitch(17)
        if mSwitch.didPressed == False:
            signal.pause()
        else:
            print("stop the motor")

    def cleanup(self):
       self.arcrane.cleanupDevices()     