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

from gpiozero import Button
from time import sleep

class CustomButton(Button):
    def __init__(self, pin, tag=None, id=None, **kwargs):
        super().__init__(pin, **kwargs)
        self.tag = tag
        self.id = id

    def __str__(self):
        return f"Button {self.tag} on Pin {self.pin} with ID {self.id}"
