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
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to sys.path
sys.path.append(script_dir)

import classes.DeviceMovements as movement
#from classes.DeviceMovements import DeviceMovements
import classes.MicroSwitch as switch
import signal as signal
import Utilities
import MqttClient

class Arcrane:
    """
    A class that will initialize all the crane movements and devices.

    Args:
        None

    Returns:
        None 
    """

    _instance = None
    
    #utility module
    utility = Utilities.Utilities()

    #MQTT instance
    client = MqttClient.MqttClient("resurgo1.local","raspberry/signal", isBackground=True)
    

    def __new__(cls, *args, **kwargs):
        """
        Class initializer for new instance.

        Args:
            cls (Class) : pointer.
            args (dict) : class arguments.
            kwargs (dict) : additional parameters.

        Returns:
            instance : Class instance 
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initiliazed movements for the crane and its devices.

        Args:
            None

        Returns:
            None 
        """
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
    
    def setUpMovements(self):
        """
        Setup the motors and monitor the movements.

        Args:
            None

        Returns:
            None 
        """
        print("setUpMovements and monitor movements")
        
        #register callback handler
        self.arcrane.delegate.register_subscriber("movement", self.receive_message)
        
        #configure motors
        self.arcrane.configureMovement()
        
        #monitor joystick and motor movements
        self.arcrane.monitorMovements()

        #subscribe to mqtt client
        self.client.subscribe_to_topic() 


    def receive_message(self, message):
        """
        Method that receives the mesages from the callback handler.

        Args:
            message (str) : The action message.

        Returns:
            None 
        """
        print(f"Delegate message received: {message}")

        #publish to the mqtt subscriber
        #self.client.publish(self.TOPIC, message)
        self.client.publish_message(message)

    def cleanup(self):
        """
        Stop the motors movement.

        Args:
            None

        Returns:
            None 
        """
        #arcrane movement install to call clean up devices.
        self.arcrane.cleanupDevices()     