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
 
 #class contains all calculations of the motors
import constants as const
from configparser import ConfigParser
import json
import time

#utility class
class Utilities:
    """
    This class is used to save and load the configuration settings.

    Args:
        None

    Returns:
        None 
    """
    _instance = None
    config = ConfigParser()
    
    #class initializer
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
            cls._instance = super(Utilities, cls).__new__(cls)
            # Initialize any attributes you want here
            cls._instance.value = 0
        return cls._instance
    
    #save configuration files
    def save_configuration(self, params: dict):
        """
        Save configuration settings.

        Args:
            params (dict) : Parameters in dictionary to save the settings.

        Returns:
            dict : Updated settings. 
        """
        self.config.read('config.ini')  
        self.config['Settings']['steps_per_revolution'] = params['steps_per_revolution']
        self.config['Settings']['degrees_per_step'] = params['degrees_per_step']
        self.config['Settings']['steps_per_90_degrees'] = params['steps_per_90_degrees']
        self.config['Settings']['step_delay'] = params['step_delay']
        self.config['Settings']['m1_step_pin'] = params['m1_step_pin']
        self.config['Settings']['m1_dir_pin'] = params['m1_dir_pin']
        self.config['Settings']['m1_movement'] = params['m1_movement']
        self.config['Settings']['m1_reversible'] = 'True' if params.get('m1_reversible') == True else  ''
        self.config['Settings']['m1_reverse_movement'] = params['m1_reverse_movement']
        self.config['Settings']['m2_step_pin'] = params['m2_step_pin']
        self.config['Settings']['m2_dir_pin'] = params['m2_dir_pin']
        self.config['Settings']['m2_movement'] = params['m2_movement']
        self.config['Settings']['m2_reversible'] = 'True' if params.get('m2_reversible') == True else  ''
        self.config['Settings']['m2_reverse_movement'] = params['m2_reverse_movement']
        self.config['Settings']['m3_step_pin'] = params['m3_step_pin']
        self.config['Settings']['m3_dir_pin'] = params['m3_dir_pin']
        self.config['Settings']['m3_movement'] = params['m3_movement']
        self.config['Settings']['m3_reversible'] = 'True' if params.get('m3_reversible') == True else  ''
        self.config['Settings']['m3_reverse_movement'] = params['m3_reverse_movement']
        self.config['Settings']['m4_step_pin'] = params['m4_step_pin']
        self.config['Settings']['m4_dir_pin'] = params['m4_dir_pin']
        self.config['Settings']['m4_movement'] = params['m4_movement']
        self.config['Settings']['m4_reversible'] = 'True' if params.get('m4_reversible') == True else  ''
        self.config['Settings']['m4_reverse_movement'] = params['m4_reverse_movement']
        self.config['Settings']['left_stop_pin'] = params['left_stop_pin']
        self.config['Settings']['right_stop_pin'] = params['right_stop_pin']
        self.config['Settings']['claw_pickup_pin'] = params['claw_pickup_pin']
        self.config['Settings']['claw_rotation_pin'] = params['claw_rotation_pin']
        self.config['Settings']['j1_up_pin'] = params['j1_up_pin'],
        self.config['Settings']['j1_down_pin'] = params['j1_down_pin']
        self.config['Settings']['j1_left_pin'] = params['j1_left_pin']
        self.config['Settings']['j1_right_pin'] = params['j1_right_pin']
        self.config['Settings']['j2_forward_pin'] = params['j2_forward_pin']
        self.config['Settings']['j2_backward_pin'] = params['j2_backward_pin']
        self.config['Settings']['j2_sideL_pin'] = params['j2_sideL_pin']
        self.config['Settings']['j2_sideR_pin'] = params['j2_sideR_pin']
        self.config['Settings']['j2_trigger_pin'] = params['j2_trigger_pin']
        self.config['Settings']['j2_fire_pin'] = params['j2_fire_pin']
        self.config['Settings']['crane_move_left_stop_pin'] = params['crane_move_left_stop_pin']
        self.config['Settings']['crane_move_right_stop_pin'] = params['crane_move_right_stop_pin']
        self.config['Settings']['crane_up_stop_pin'] = params['crane_up_stop_pin']
        self.config['Settings']['crane_down_stop_pin'] = params['crane_down_stop_pin']
        self.config['Settings']['claw_step_delay'] = params['claw_step_delay']

        #write to configuration file
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile) 
        return self.config['Settings']  
    
    #get configuration settings
    def get_configuration(self, param):
        """
        Get the specific configuration setting.

        Args:
            params (str) : Setting name.

        Returns:
            str : value. 
        """
        self.config.read('config.ini')
        val = self.config["Settings"][param]
        print(f"param config: {param}")
        print(f"get config: {val}")
        return self.config["Settings"][param]
