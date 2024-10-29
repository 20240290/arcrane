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

# Motor settings
# steps_per_revolution = 200  # Assuming 200 steps for 1 full revolution (adjust if needed)
# degrees_per_step = 360 / steps_per_revolution
# steps_per_90_degrees = int(90 / degrees_per_step)
# step_delay = 0.001  # Delay between steps (in seconds)

class Utilities:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Utilities, cls).__new__(cls)
        return cls._instance
    
    