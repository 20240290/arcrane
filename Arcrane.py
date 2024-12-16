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
import classes.MicroSwitch as switch
import signal as signal
import Utilities
import paho.mqtt.client as mqtt   

class Arcrane:
    _instance = None
    
    #utility module
    utility = Utilities.Utilities()

    # MQTT broker details
    BROKER = "resurgo2.local"
    TOPIC = "raspberry/signal"

    # MQTT client setup
    client = mqtt.Client()

    client.connect(BROKER, port=1883, keepalive=60)
    print("Connected to MQTT broker")
    # Keep script running
    client.loop_start()

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
                'step': self.utility.get_configuration('m3_step_pin'), 
                'drive': self.utility.get_configuration('m3_dir_pin'), 
                'direction': True, 
                'reversable': self.utility.get_configuration('m3_reversible'), 
                'reverse_movement': self.utility.get_configuration('m3_reverse_movement'),
                'movement': self.utility.get_configuration('m3_movement')}, 
                {
                'step': self.utility.get_configuration('m1_step_pin'), 
                'drive': self.utility.get_configuration('m1_dir_pin'), 
                'direction': True, 
                'reversable': self.utility.get_configuration('m1_reversible'), 
                'reverse_movement': self.utility.get_configuration('m1_reverse_movement'),
                'movement': self.utility.get_configuration('m1_movement')}, 
                # {
                # 'step': utility.get_configuration('m4_step_pin'), 
                # 'drive': utility.get_configuration('m4_dir_pin'), 
                # 'direction': True, 
                # 'reversable': utility.get_configuration('m4_reversible'), 
                # 'reverse_movement': utility.get_configuration('m4_reverse_movement'),
                # 'movement': utility.get_configuration('m4_movement')}, 
                {
                'step': self.utility.get_configuration('m2_step_pin'), 
                'drive': self.utility.get_configuration('m2_dir_pin'), 
                'direction': True, 
                'reversable': self.utility.get_configuration('m2_reversible'), 
                'reverse_movement': self.utility.get_configuration('m2_reverse_movement'),
                'movement': self.utility.get_configuration('m2_movement')}
                ]},
            pins=[{'down': self.utility.get_configuration('j1_down_pin'), 
                    'right': self.utility.get_configuration('j1_right_pin'), 
                    'up': self.utility.get_configuration('j1_up_pin'), 
                    'left': self.utility.get_configuration('j1_left_pin'), 
                    'backward': self.utility.get_configuration('j2_backward_pin'), 
                   'sideR': self.utility.get_configuration('j2_sideR_pin'), 
                   'forward': self.utility.get_configuration('j2_forward_pin'), 
                   'sideL': self.utility.get_configuration('j2_sideL_pin'), 
                   'trigger': self.utility.get_configuration('j2_trigger_pin'), 
                   'fire': self.utility.get_configuration('j2_fire_pin'), 
                   'up_stop_pin': self.utility.get_configuration('crane_up_stop_pin'),
                   'down_stop_pin': self.utility.get_configuration('crane_down_stop_pin'),
                   'left_stop_pin': self.utility.get_configuration('crane_move_left_stop_pin'),
                   'right_stop_pin': self.utility.get_configuration('crane_move_right_stop_pin'),
                   }])
        print(f"self.joystick1 {self.arcrane.pins}")
    
    def setupMovementJoystick2(self):
        print("setupMovementJoystick2 and monitor movements")

    
    def setUpMovements(self):
        print("setUpMovements and monitor movements")
        self.arcrane.delegate.register_subscriber("movement", self.receive_message)
        self.arcrane.configureMovement()
        self.arcrane.monitorMovements() 


    def receive_message(self, message):
        print(f"Delegate message received: {message}")
        self.client.publish(self.TOPIC, message)

    def cleanup(self):
       self.arcrane.cleanupDevices()     