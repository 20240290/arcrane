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
import threading
import time
import atexit
import subprocess, shlex

#Crane Utitlity Instance
utility = Utilities.Utilities()

#Crane Data Instance
arcrane = Arcrane.Arcrane()

#MQTT Server


def gpio_task():
    arcrane.setUpMovements()


logging.basicConfig(level=logging.DEBUG)
# Shared event to signal threads to stop
stop_event = threading.Event()

app = Flask(__name__)

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
            "claw_rotation_pin": request.form['claw_rotation_pin'],
            "j1_up_pin": request.form['j1_up_pin'],
            "j1_down_pin": request.form['j1_down_pin'],
            "j1_left_pin": request.form['j1_left_pin'],
            "j1_right_pin": request.form['j1_right_pin'],
            "j2_forward_pin": request.form['j2_forward_pin'],
            "j2_backward_pin": request.form['j2_backward_pin'],
            "j2_sideL_pin": request.form['j2_sideL_pin'],
            "j2_sideR_pin": request.form['j2_sideR_pin'],
            "j2_trigger_pin": request.form['j2_trigger_pin'],
            "j2_fire_pin": request.form['j2_fire_pin'],
            "crane_up_stop_pin": request.form['crane_up_stop_pin'],
            "crane_down_stop_pin": request.form['crane_down_stop_pin'],
            "crane_move_left_stop_pin": request.form['crane_move_left_stop_pin'],
            "crane_move_right_stop_pin": request.form['crane_move_right_stop_pin'],
            "claw_step_delay": request.form['claw_step_delay']
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
    print(f"check if joystick is added: {arcrane.joystick1 != None}")
    if arcrane.joystick1 != None:
        arcrane.joystick1.monitorWebMovements(direction)

    return jsonify({'status': 'success', 'direction': direction})

def get_running_flask_processes(port):
    processes = []
    cmd = f"lsof -ti:{port}"
    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    if result.stdout:
        if "\n" in result.stdout:
            processes += result.stdout.split("\n")
            processes = [int(x) for x in processes if x != '']
        else:
            processes += [int(result.stdout)]
    return processes

def cleanup():
    atexit.register(cleanup)   


def run_flask():
    app.run(threaded=True)

def worker():
    while not stop_event.is_set():  # Threads check this event to decide when to stop
        print("Working...")
        time.sleep(1)
    print("Thread exiting gracefully...")
     

if __name__ == '__main__':
    try:
        #list of threads
        #threads = []

        # Start Flask in a separate thread
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.start()
        #threads.append(flask_thread)
        gpio_task()

    except KeyboardInterrupt:
        # Signal all threads to stop by setting the stop event
                # flask_thread.start()
        # threads.append(flask_thread)stop_event.set()pwd

        print("All threads have exited. Program is shutting down.")
        print("Exiting...")
    finally:
        # cleanup()
        print("clean up")
        #sys.exit(0)
