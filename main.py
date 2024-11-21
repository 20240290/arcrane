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
import classes.DeviceMovements as movement
import Arcrane as Arcrane

from flask import Flask, render_template, request, redirect, url_for, jsonify
import Utilities
import multiprocessing

utility = Utilities.Utilities()
arcrane = Arcrane.Arcrane()
arcrane.initialize()

def gpio_task():
    if arcrane.joystick1 != None:
        arcrane.setUpMovements()

    print(f"arcrane.joystick1 is none? {arcrane.joystick1 == None}")   

#Start the GPIO task in a separate process
# gpio_process = multiprocessing.Process(target=gpio_task)
# gpio_process.daemon = True
# gpio_process.start()


logging.basicConfig(level=logging.DEBUG)

# def configure_app(app):
#     print("configure_app called...")
#     initializeMovements()
#     #initializeI2c()

#app = Flask(__name__)
# def create_app():
#     app = Flask(__name__)
#     #configure_app(app)
#     # Initialization tasks
#     print("App is being initialized...")
#     return app


# app = create_app()


def init_app():
    
    print(f"arcrane.joystick1 is none? {arcrane.joystick1 == None}")    
    print("Performing startup initialization tasks...") 
    # if arcrane.joystick1 != None:
    #     arcrane.setUpMovements()

    print(f"arcrane.joystick1 is none? {arcrane.joystick1 == None}")    

app = Flask(__name__)

init_app()  # Call the initialization function here

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/configuration", methods=['GET', 'POST'])
def configuration():
    utility.config.read('config.ini')  
    if request.method == 'POST':     
        print(f"reversible: {request.form.get('m4_reversible')}")
        data = {
            "steps_per_revolution": request.form['steps_per_revolution'],
            "degrees_per_step": request.form['degrees_per_step'],
            "steps_per_90_degrees": request.form['steps_per_90_degrees'],
            "step_delay": request.form['step_delay'],
            "m1_step_pin": request.form['m1_step_pin'],
            "m1_dir_pin": request.form['m1_dir_pin'],
            "m1_movement": request.form['m1_movement'],
            "m1_reversible": True if request.form.get('m1_reversible') != None else '',
            "m1_reverse_movement": request.form['m1_reverse_movement'],
            "m2_step_pin": request.form['m2_step_pin'],
            "m2_dir_pin": request.form['m2_dir_pin'],
            "m2_movement": request.form['m2_movement'],
            "m2_reversible": True if request.form.get('m2_reversible') != None else '',
            "m2_reverse_movement": request.form['m2_reverse_movement'],
            "m3_step_pin": request.form['m3_step_pin'],
            "m3_dir_pin": request.form['m3_dir_pin'],
            "m3_movement": request.form['m3_movement'],
            "m3_reversible": True if request.form.get('m3_reversible')  != None else '',
            "m3_reverse_movement": request.form['m3_reverse_movement'],
            "m4_step_pin": request.form['m4_step_pin'],
            "m4_dir_pin": request.form['m4_dir_pin'],
            "m4_movement": request.form['m4_movement'],
            "m4_reversible": True if request.form.get('m4_reversible') != None else '',
            "m4_reverse_movement": request.form['m4_reverse_movement'],
            "left_stop_pin": request.form['left_stop_pin'],
            "right_stop_pin": request.form['right_stop_pin'],
            "claw_pickup_pin": request.form['claw_pickup_pin'],
            "claw_rotation_pin": request.form['claw_rotation_pin']
        }
        
        utility.save_configuration(data)
        #call the module to configure the crane movements and devices.
        
        return redirect(url_for('configuration'))
    return render_template("configuration.html",  config=utility.config['Settings'])


@app.route("/joystick")
def joystick():
    #setup motors from arcrane module
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

@app.route('/long_press/<direction>/<device>', methods=['POST'])
def long_press(direction,device):
    # Handle the long-press action here
    print(f"Joystick moved: {direction} device: { device }")
    
    # if direction == 'up':
    #     movement1 = movement.DeviceMovements(step=const.M1_STEP_PIN, drive=const.M1_DIR_PIN, pins=[], direction_forward=True)
    #     movement1.motor.rotate_motor()
    # elif direction == 'down':
    #     movement2 = movement.DeviceMovements(step=const.M2_STEP_PIN, drive=const.M2_DIR_PIN, pins=[],direction_forward=True)
    #     movement2.motor.rotate_motor()    
    # elif direction == 'left':
    #     movement3 = movement.DeviceMovements(step=const.M3_STEP_PIN, drive=const.M3_DIR_PIN, pins=[],direction_forward=True)
    #     movement3.motor.rotate_motor()
    # elif direction == 'right':
    #     movement4 = movement.DeviceMovements(step=const.M4_STEP_PIN, drive=const.M4_DIR_PIN, pins=[],direction_forward=True)
    #     movement4.motor.rotate_motor()
    print(f"check if joystick is added: {Arcrane.joystick1 != None}")
    if Arcrane.joystick1 != None:
        Arcrane.joystick1.monitorWebMovements(direction)

    return jsonify({'status': 'success', 'direction': direction})

if __name__ == '__main__':
    try:
        app.run(port=5001, debug=True, use_reloader=True)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        print("clean up")
