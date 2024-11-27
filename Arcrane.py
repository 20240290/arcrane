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
   
utility = Utilities.Utilities()

class Arcrane:
    _instance = None
    is_portal: bool = False
    joystick1: movement.DeviceMovements
    joystick12: movement.DeviceMovements

    #class initializer
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Arcrane, cls).__new__(cls)
            cls._instance.value = 0
        return cls._instance
    
    def initialize(self):
        self.joystick1 = movement.DeviceMovements(movements = {
            'motors': [{
                'step': utility.get_configuration('m1_step_pin'), 
                'drive': utility.get_configuration('m1_dir_pin'), 
                'direction': True,
                'reversable': utility.get_configuration('m1_reversible'), 
                'reverse_movement': utility.get_configuration('m1_reverse_movement'),
                'movement': utility.get_configuration('m1_movement')},
                {
                'step': utility.get_configuration('m3_step_pin'), 
                'drive': utility.get_configuration('m3_dir_pin'), 
                'direction': True, 
                'reversable': utility.get_configuration('m3_reversible'), 
                'reverse_movement': utility.get_configuration('m3_reverse_movement'),
                'movement': utility.get_configuration('m3_movement')}, 
                {
                'step': utility.get_configuration('m4_step_pin'), 
                'drive': utility.get_configuration('m4_dir_pin'), 
                'direction': True, 
                'reversable': utility.get_configuration('m4_reversible'), 
                'reverse_movement': utility.get_configuration('m4_reverse_movement'),
                'movement': utility.get_configuration('m4_movement')}
                ]},
            pins=[{'down': utility.get_configuration('j1_down_pin'), 
                        'right': utility.get_configuration('j1_right_pin'), 
                    'up': utility.get_configuration('j1_up_pin'), 
                    'left': utility.get_configuration('j1_left_pin')}])
        print(f"self.joystick1 {self.joystick1}")

        self.joystick2 = movement.DeviceMovements(movements = {
            'motors': [{
                    'step': utility.get_configuration('m2_step_pin'), 
                    'drive': utility.get_configuration('m2_dir_pin'), 
                    'direction': True, 
                    'reversable': utility.get_configuration('m2_reversible'), 
                    'reverse_movement': utility.get_configuration('m2_reverse_movement'),
                    'movement': utility.get_configuration('m2_movement')}, 
                    ]},
            pins=[{'down': utility.get_configuration('j1_down_pin'), 
                        'right': utility.get_configuration('j1_right_pin'), 
                    'up': utility.get_configuration('j1_up_pin'), 
                    'left': utility.get_configuration('j1_left_pin')}])
        print(f"self.joystick1 {self.joystick1}")
    

    def setUpMovements(self):
        # joystick1 = movement.DeviceMovements(step=const.M2_STEP_PIN, 
        #                                      drive=const.M2_DIR_PIN, 
        #                                      movements = {
        #                                          'pins': {'down': 18, 'right': 21, 'up': 26, 'left': 20}, 
        #                                          'motors': [{
        #                                              'step': const.M4_STEP_PIN, 
        #                                              'drive': const.M4_DIR_PIN, 
        #                                              'direction': True, 
        #                                              'movement': 'up'}, {
        #                                              'step': const.M3_STEP_PIN, 
        #                                              'drive': const.M3_DIR_PIN, 
        #                                              'direction': True, 
        #                                              'movement': 'up'}, ]},
        #                                      pins=[{'down': 18, 'right': 21, 'up': 26, 'left': 20}], direction_forward=True)
        print("setUpMovements and monitor movements")
        self.joystick1.setUpMovements()
        self.joystick1.configureMovement()
        self.joystick1.monitorMovements()
        self.joystick1.monitorWebMovements()

    def setupWebMovement(self):    
        self.joystick1.configureMovement()
        self.joystick1.monitorMovements()
        
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
       self.joystick1.cleanupDevices()     