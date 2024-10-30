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

import sys
import subprocess
import shutil
from pathlib import Path
import constants as const
import logging

from flask import Flask, render_template, request, redirect, url_for, jsonify
import Utilities
import classes.DeviceMovements as movement

#Arcrane methods

# import curses
# from gpiozero import OutputDevice
# from time import sleep

# # Pin setup for Motor 1
# M1_STEP_PIN = 17  # GPIO pin for the step signal
# M1_DIR_PIN = 27   # GPIO pin for the direction control

# # Pin setup for Motor 2
# M2_STEP_PIN = 22  # GPIO pin for the step signal
# M2_DIR_PIN = 23   # GPIO pin for the direction control

# # Pin setup for Motor 3
# M3_STEP_PIN = 5   # GPIO pin for the step signal
# M3_DIR_PIN = 6    # GPIO pin for the direction control

# # Pin setup for Motor 4
# M4_STEP_PIN = 12  # GPIO pin for the step signal
# M4_DIR_PIN = 13   # GPIO pin for the direction control

# # Set up the GPIO pins for each motor
# motor1_step = OutputDevice(M1_STEP_PIN)
# motor1_dir = OutputDevice(M1_DIR_PIN)

# motor2_step = OutputDevice(M2_STEP_PIN)
# motor2_dir = OutputDevice(M2_DIR_PIN)

# motor3_step = OutputDevice(M3_STEP_PIN)
# motor3_dir = OutputDevice(M3_DIR_PIN)

# motor4_step = OutputDevice(M4_STEP_PIN)
# motor4_dir = OutputDevice(M4_DIR_PIN)

# # Motor settings
# steps_per_revolution = 200  # Assuming 200 steps for 1 full revolution (adjust if needed)
# step_delay = 0.001  # Delay between steps (in seconds)

#End of Arcrane Methods
        
app = Flask(__name__)
utility = Utilities.Utilities()

# # Pin setup for Motor 1
# M1_STEP_PIN = 17  # GPIO pin for the step signal
# M1_DIR_PIN = 27   # GPIO pin for the direction control

# # Pin setup for Motor 2
# M2_STEP_PIN = 22  # GPIO pin for the step signal
# M2_DIR_PIN = 23   # GPIO pin for the direction control

# # Pin setup for Motor 3
# M3_STEP_PIN = 5   # GPIO pin for the step signal
# M3_DIR_PIN = 6    # GPIO pin for the direction control

# # Pin setup for Motor 4
# M4_STEP_PIN = 12  # GPIO pin for the step signal
# M4_DIR_PIN = 13   # GPIO pin for the direction control

# # Set up the GPIO pins for each motor
# motor1_step = OutputDevice(M1_STEP_PIN)
# motor1_dir = OutputDevice(M1_DIR_PIN)

# motor2_step = OutputDevice(M2_STEP_PIN)
# motor2_dir = OutputDevice(M2_DIR_PIN)

# motor3_step = OutputDevice(M3_STEP_PIN)
# motor3_dir = OutputDevice(M3_DIR_PIN)

# motor4_step = OutputDevice(M4_STEP_PIN)
# motor4_dir = OutputDevice(M4_DIR_PIN)


movement1 = movement.DeviceMovements(step=const.M1_STEP_PIN, drive=const.M1_DIR_PIN,direction_forward=True)
movement2 = movement.DeviceMovements(step=const.M2_STEP_PIN, drive=const.M2_DIR_PIN,direction_forward=True)
movement3 = movement.DeviceMovements(step=const.M3_STEP_PIN, drive=const.M3_DIR_PIN,direction_forward=True)
movement4 = movement.DeviceMovements(step=const.M4_STEP_PIN, drive=const.M4_DIR_PIN,direction_forward=True)

logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/configuration", methods=['GET', 'POST'])
def configuration():
    utility.config.read('config.ini')  
    if request.method == 'POST':
        # config['Settings']['rotation'] = request.form['rotation_speed']
        # with open('config.ini', 'w') as configfile:
        #     config.write(configfile)       
        data = {
            "STEPS_PER_REVOLUTION": request.form['STEPS_PER_REVOLUTION'],
            "DEGREES_PER_STEP": request.form['DEGREES_PER_STEP'],
            "STEPS_PER_90_DEGREES": request.form['STEPS_PER_90_DEGREES'],
            "STEP_DELAY": request.form['STEP_DELAY'],
            "M1_STEP_PIN": request.form['M1_STEP_PIN'],
            "M1_DIR_PIN": request.form['M1_DIR_PIN'],
            "M2_STEP_PIN": request.form['M2_STEP_PIN'],
            "M2_DIR_PIN": request.form['M2_DIR_PIN'],
            "M3_STEP_PIN": request.form['M3_STEP_PIN'],
            "M3_DIR_PIN": request.form['M3_DIR_PIN'],
            "M4_STEP_PIN": request.form['M4_STEP_PIN'],
            "M4_DIR_PIN": request.form['M4_DIR_PIN']
        }
        
        utility.save_configuration(data)
        
        return redirect(url_for('configuration'))
    return render_template("configuration.html",  config=utility.config['Settings'])


@app.route("/joystick")
def joystick():
    return render_template("joystick.html")

@app.route('/move_joystick/<direction>')
def move_joystick(direction):
    # Here you can handle the joystick input
    print(f"Joystick moved: {direction}")
    return jsonify({'status': 'success', 'direction': direction})

@app.route("/loadDefaults", methods=['POST'])
def loadDefaults():
    #data = {'rotation_speed': '1000'}
    data =  {'rotation_speed': '1000'}
    return redirect(url_for('configuration'))

@app.route('/run-script', methods=['POST'])
def run_script():
    # Your Python script logic here
    result = {"message": "Script executed successfully!"}
    return jsonify(result)

@app.route('/long_press', methods=['POST'])
def long_press():
    # Handle the long-press action here
    return jsonify(message="Long press action triggered!")

def initializeMotors():
    pass

if __name__ == '__main__':
    try:
        app.run(debug=True)
        #curses.wrapper(motorMovements)
    except KeyboardInterrupt:
        print("Exiting...")


