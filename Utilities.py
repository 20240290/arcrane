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
import lgpio
import time

#utility class
class Utilities:
    _instance = None
    config = ConfigParser()
    
    #class initializer
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Utilities, cls).__new__(cls)
            # Initialize any attributes you want here
            cls._instance.value = 0
        return cls._instance
    
    #save configuration files
    def save_configuration(self, params):
        self.config.read('config.ini')  
        self.config['Settings']['STEPS_PER_REVOLUTION'] = params['STEPS_PER_REVOLUTION']
        self.config['Settings']['DEGREES_PER_STEP'] = params['DEGREES_PER_STEP']
        self.config['Settings']['STEPS_PER_90_DEGREES'] = params['STEPS_PER_90_DEGREES']
        self.config['Settings']['STEP_DELAY'] = params['STEP_DELAY']
        self.config['Settings']['M1_STEP_PIN'] = params['M1_STEP_PIN']
        self.config['Settings']['M1_DIR_PIN'] = params['M1_DIR_PIN']
        self.config['Settings']['M2_STEP_PIN'] = params['M2_STEP_PIN']
        self.config['Settings']['M2_DIR_PIN'] = params['M2_DIR_PIN']
        self.config['Settings']['M3_STEP_PIN'] = params['M3_STEP_PIN']
        self.config['Settings']['M3_DIR_PIN'] = params['M3_DIR_PIN']
        self.config['Settings']['M4_STEP_PIN'] = params['M4_STEP_PIN']
        self.config['Settings']['M4_DIR_PIN'] = params['M4_DIR_PIN']

        #write to configuration file
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile) 
        return self.config['Settings']  
    
    def get_configuration(self, param):
        self.config.read('config.ini')
        val = self.config["Settings"][param]
        print(f"param config: {param}")
        print(f"get config: {val}")
        return self.config["Settings"][param]


    def loadDefaultConfiguration(self):
        self.config.read('config.ini')
        with open('config.ini', 'r') as file:
            self.config = json.load({"SETTINGS": {
               "STEPS_PER_REVOLUTION": const.STEPS_PER_REVOLUTION,
               "DEGREES_PER_STEP":  const.DEGREES_PER_STEP,
                "STEPS_PER_90_DEGREES": const.STEPS_PER_90_DEGREES,
                "STEP_DELAY": const.STEP_DELAY,
                "M1_STEP_PIN": const.M1_STEP_PIN,
                "M1_DIR_PIN": const.M1_DIR_PIN,
                "M2_STEP_PIN": const.M2_STEP_PIN,
                "M2_DIR_PIN": const.M2_DIR_PIN,
                "M3_STEP_PIN": const.M3_STEP_PIN,
                "M3_DIR_PIN": const.M3_DIR_PIN,
                "M4_STEP_PIN": const.M4_STEP_PIN,
                "M4_DIR_PIN": const.M4_DIR_PIN
            }})

            return self.config

    def clearGPIOPin(self,pin):
        try:
            chip = lgpio.gpiochip_open(0)
            # Claim the pin as an output
            lgpio.gpio_claim_output(chip, pin)

            # Set the pin high
            lgpio.gpio_write(chip, pin, 1)  # Set high
            # Set the pin low
            lgpio.gpio_write(chip, pin, 0)  # Set low

        finally:
            lgpio.gpiochip_close(chip) 