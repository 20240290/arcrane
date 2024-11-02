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

class GenericDevice:
    def __init__(self):
        # Initialize the device without a pin
        self.pin = None
        self.state = False

    def begin(self):
        # Initialize the device here
        if self.pin is None:
            print("Device is not configured with a pin.")
        else:
            print(f"Output device initialized on pin {self.pin}.")

    def configure_pin(self, pin):
        # Set the pin for the output device
        self.pin = pin
        print(f"Pin configured to {self.pin}.")

    def turn_on(self):
        if self.pin is None:
            print("Error: Device pin not configured.")
            return
        # Logic to turn the device on
        self.state = True
        print(f"Device on pin {self.pin} turned ON.")

    def turn_off(self):
        if self.pin is None:
            print("Error: Device pin not configured.")
            return
        # Logic to turn the device off
        self.state = False
        print(f"Device on pin {self.pin} turned OFF.")

    def set_state(self, state):
        if state:
            self.turn_on()
        else:
            self.turn_off()

    def get_state(self):
        return self.state
