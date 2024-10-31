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
import curses
from gpiozero import OutputDevice
from time import sleep

        
app = Flask(__name__)
utility = Utilities.Utilities()

logging.basicConfig(level=logging.DEBUG)

# utility.clearGPIOPin(const.M1_STEP_PIN)
# utility.clearGPIOPin(const.M2_STEP_PIN)
# utility.clearGPIOPin(const.M3_STEP_PIN)
# utility.clearGPIOPin(const.M4_STEP_PIN)

# movement1 = movement.DeviceMovements(step=const.M1_STEP_PIN, drive=const.M1_DIR_PIN,direction_forward=True)
# movement2 = movement.DeviceMovements(step=const.M2_STEP_PIN, drive=const.M2_DIR_PIN,direction_forward=True)
# movement3 = movement.DeviceMovements(step=const.M3_STEP_PIN, drive=const.M3_DIR_PIN,direction_forward=True)
# movement4 = movement.DeviceMovements(step=const.M4_STEP_PIN, drive=const.M4_DIR_PIN,direction_forward=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/configuration", methods=['GET', 'POST'])
def configuration():
    utility.config.read('config.ini')  
    if request.method == 'POST':     
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
    movement1 = movement.DeviceMovements(step=const.M1_STEP_PIN, drive=const.M1_DIR_PIN,direction_forward=True)
    movement2 = movement.DeviceMovements(step=const.M2_STEP_PIN, drive=const.M2_DIR_PIN,direction_forward=True)
    movement3 = movement.DeviceMovements(step=const.M3_STEP_PIN, drive=const.M3_DIR_PIN,direction_forward=True)
    movement4 = movement.DeviceMovements(step=const.M4_STEP_PIN, drive=const.M4_DIR_PIN,direction_forward=True)
    if direction == 'up':
        movement1.motor.rotate_motor()
    elif direction == 'up-left':
        movement2.motor.rotate_motor()    
    elif direction == 'down-left':
        movement3.motor.rotate_motor()
    elif direction == 'down-right':
        movement4.motor.rotate_motor()

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

@app.route('/long_press/<direction>', methods=['POST'])
def long_press(direction):
    # Handle the long-press action here
    #return jsonify(message="Long press action triggered!")
    print(f"Joystick moved: {direction}")
    movement1 = movement.DeviceMovements(step=const.M1_STEP_PIN, drive=const.M1_DIR_PIN,direction_forward=True)
    if direction == 'up':
        movement1.motor.rotate_motor()
    # elif direction == 'down':
    #     movement2.motor.rotate_motor()    
    # elif direction == 'left':
    #     movement3.motor.rotate_motor()
    # elif direction == 'right':
    #     movement4.motor.rotate_motor()

    return jsonify({'status': 'success', 'direction': direction})

def initializeMotors():
    pass
    # movement1.setDeviceOutput()
    # movement2.setDeviceOutput()
    # movement3.setDeviceOutput()
    # movement4.setDeviceOutput()

if __name__ == '__main__':
    try:
        app.run(debug=True)
        #curses.wrapper(initializeMotors)
    except KeyboardInterrupt:
        print("Exiting...")


