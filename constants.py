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


#Constants Declaration
DEFAULT_ANGLE = 120
DEFAULT_ROTATION = 360
STEPS_PER_REVOLUTION = 200  # Assuming 200 steps for 1 full revolution (adjust if needed)
DEGREES_PER_STEP = DEFAULT_ROTATION / STEPS_PER_REVOLUTION
STEPS_PER_90_DEGREES = int(90 / DEGREES_PER_STEP)
STEP_DELAY = 0.001
SERVO_DELAY = 1
SERVO_POSITION = 1

J1_UP_PIN = 26
J1_DOWN_PIN =  18
J1_LEFT_PIN =  20
J1_RIGHT_PIN = 21

# Pin setup for Motor 1
M1_STEP_PIN = 17
M1_DIR_PIN = 27
M1_MOVEMENT = ''
M1_REVERSIBLE = False
M1_REVERSE_MOVEMENT = ''

# Pin setup for Motor 2
M2_STEP_PIN = 22
M2_DIR_PIN = 23
M2_MOVEMENT = ''
M2_REVERSIBLE = False
M2_REVERSE_MOVEMENT = ''

# Pin setup for Motor 3
M3_STEP_PIN = 5
M3_DIR_PIN = 6
M3_MOVEMENT = ''
M3_REVERSIBLE = False
M3_REVERSE_MOVEMENT = ''

# Pin setup for Motor 4
M4_STEP_PIN = 12
M4_DIR_PIN = 13
M4_MOVEMENT = ''
M4_REVERSIBLE = False
M4_REVERSE_MOVEMENT = ''