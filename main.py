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
from configparser import ConfigParser

#Arcrane methods
# import curses
# from gpiozero import OutputDevice
# from time import sleep

# # Pin setup (adjust GPIO pins according to your wiring)
# STEP_PIN = 17  # GPIO pin for the step signal
# DIR_PIN = 27   # GPIO pin for the direction control

# # Set up the GPIO pins
# step = OutputDevice(STEP_PIN)
# direction = OutputDevice(DIR_PIN)

# # Motor settings
# steps_per_revolution = 200  # Assuming 200 steps for 1 full revolution (adjust if needed)
# degrees_per_step = 360 / steps_per_revolution
# steps_per_90_degrees = int(90 / degrees_per_step)
# step_delay = 0.001  # Delay between steps (in seconds)
        
app = Flask(__name__)
config = ConfigParser()
config.read('config.ini')   

logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/configuration", methods=['GET', 'POST'])
def configuration():
    if request.method == 'POST':
        config['Settings']['rotation'] = request.form['rotation_speed']
        with open('config.ini', 'w') as configfile:
            config.write(configfile)       
        return redirect(url_for('configuration'))
    return render_template("configuration.html",  config=config['Settings'])


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
    data = {'rotation_speed': '1000'}
    return jsonify(data)

@app.route('/run-script', methods=['POST'])
def run_script():
    # Your Python script logic here
    result = {"message": "Script executed successfully!"}
    return jsonify(result)

@app.route('/long_press', methods=['POST'])
def long_press():
    # Handle the long-press action here
    return jsonify(message="Long press action triggered!")
    
def rotate(steps, direction_forward=True):
    # Set direction
    direction.value = direction_forward
    # Perform the steps
    for _ in range(steps):
        step.on()
        sleep(step_delay)
        step.off()
        sleep(step_delay)

if __name__ == '__main__':
    app.run(debug=True)


