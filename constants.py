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