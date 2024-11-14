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
from time import sleep
import classes.MicroSwitch as switch
from signal import pause
import smbus
import time

def initialize():
     setUpMovements()

def setUpMovements():
    joystick1 = movement.DeviceMovements(step=const.M2_STEP_PIN, 
                                         drive=const.M2_DIR_PIN, 
                                         movements = {
                                             'pins': {'down': 18, 'right': 21, 'up': 26, 'left': 20}, 
                                             'motors': [{
                                                 'step': const.M4_STEP_PIN, 
                                                 'drive': const.M4_DIR_PIN, 
                                                 'direction': True, 
                                                 'movement': 'up'}, {
                                                 'step': const.M3_STEP_PIN, 
                                                 'drive': const.M3_DIR_PIN, 
                                                 'direction': True, 
                                                 'movement': 'right'}, ]},
                                         pins=[{'down': 18, 'right': 21, 'up': 26, 'left': 20}], direction_forward=True)
    joystick1.configureMovement()
    joystick1.monitorMovements()

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
        pause()
    else:
        print("stop the motor")