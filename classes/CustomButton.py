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
 limitations under
 """
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to sys.path
sys.path.append(script_dir)

from gpiozero import Button
from time import sleep

class CustomButton(Button):
    """
    Custom gpiozero button class with additional parameter.
    
    Args:
        None    
    
    Returns:
        None
    """
    
    def __init__(self, pin, tag=None, id=None, **kwargs):  
        """
        Custom gpiozero button initializer.
        
        Args:
        tag (str) : Button tag
        id (str) : Button identifier    
        
        Returns:
            None
        """  
        super().__init__(pin, **kwargs)
        self.tag = tag
        self.id = id

    def __str__(self):
        """
        Print addional parameters values.
        
        Args:
            None

        Returns:
            None
        """
        return f"Button {self.tag} on Pin {self.pin} with ID {self.id}"
