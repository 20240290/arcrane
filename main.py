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

@app.route("/loadDefaults", methods=['POST'])
def loadDefaults():
    data = {'rotation_speed': '1000'}
    return jsonify(data)

@app.route('/run-script', methods=['POST'])
def run_script():
    # Your Python script logic here
    result = {"message": "Script executed successfully!"}
    return jsonify(result)
    

if __name__ == '__main__':
    app.run(debug=True)


