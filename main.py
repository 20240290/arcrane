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
import Arcrane
import Utilities
import threading
import time
import atexit
from flask import Flask, render_template, request, redirect, url_for, jsonify
import webbrowser


#Crane Utitlity Instance
utility: Utilities = Utilities()

#Crane Data Instance
arcrane: Arcrane = Arcrane()

#Arcrane Setup Movements
def craneSetup():
    """
    Setup crane movements.

    Args:
        None

    Returns:
        None
    """
    arcrane.setUpMovements()


logging.basicConfig(level=logging.DEBUG)
# Shared event to signal threads to stop
stop_event = threading.Event()

app = Flask(__name__)

#Dashboard route
@app.route("/")
def index():
    """
    Web portal home page

    Args:
        None

    Returns:
        web page : index.html
    """
    return render_template("index.html")

#Configuration route.
@app.route("/configuration", methods=['GET', 'POST'])
def configuration():
    """
    Configurations page.

    Args:
        None

    Returns:
        web page : configuration.html 
    """
    #read config.ini file
    utility.config.read('config.ini')  

    #check request method
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
        
        #save configurations in the config.ini
        utility.save_configuration(data)
      
        #call the module to configure the crane movements and devices.
        return redirect(url_for('configuration'))
    return render_template("configuration.html",  config=utility.config['Settings'])

#Joystick route.
@app.route("/joystick")
def joystick():
    """
    Configurations page.

    Args:
        None

    Returns:
        web page : configuration.html
    """
    #setup motors from arcrane module
    return render_template("joystick.html")

#Long press action route.
@app.route('/long_press/<direction>/<device>', methods=['POST'])
def long_press(direction,device):
    """
    Method to handle the long press gesture and correspond to the movement of the joystick.

    Args:
        direction (str) : The direction of the joystick
        device (str) : The joystick selected.
    
    Returns:
        str : status message
    """
    # Handle the long-press action here
    print(f"Joystick moved: {direction} device: { device }")
    if arcrane.arcrane != None:
        #convvert the receive movement depends on the device
        if device == "crane":
            arcrane.arcrane.monitorWebMovements(direction)
        else:
            movement = "forward"
            if direction == "up":
                movement = "forward"
            elif direction == "down":
                movement = "backward" 
            elif direction == "left":
                movement = "sideL"   
            elif direction == "right":
                movement = "sideR"
            elif direction == "fire":
                movement = "fire"
            elif direction == "trigger"  :
                movement = "trigger"                
            arcrane.arcrane.monitorWebMovements(movement)

        

    return jsonify({'status': 'success', 'direction': direction})

def cleanup():
    atexit.register(cleanup)   

def run_flask():
    """
    Initialize flask instance.

    Args:
        None

    Returns:
        None
    """
    app.run(threaded=True)

def worker():
    while not stop_event.is_set():  # Threads check this event to decide when to stop
        print("Working...")
        time.sleep(1)
    print("Thread exiting gracefully...")
    
# def check_dependencies():
#     """
#     Method to check if the necessary dependencies are installed and let the user know that it needs to be installed.

#     Args:
#         None

#     Returns:
#         Bool : Check if all dependencies are installed.
#     """
#     missing_dependencies = []

#     try:
#         import Flask
#         print("Flask library is installed")
#     except ImportError:
#        missing_dependencies.append('Flask')

#     try:
#         import paho.mqtt.client
#         print("paho.mqtt.client library is installed")

#     except ImportError:
#        missing_dependencies.append('mosquitto')
#        missing_dependencies.append('mosquitto-clients')
#        missing_dependencies.append('paho-mqtt')

#     if len(missing_dependencies) == 0:
#         return True
#     else:
#         for item in missing_dependencies:
#             install(item)
#         else:
#             return True    
    
# def install(package):
#     """
#     Install a specific package.

#     Args:
#         None

#     Returns:
#         None
#     """
#     try:
#         subprocess.check_call([sys.executable, "-m", "pip", "install", package])
#         print(f"Successfully installed {package}")
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to install {package}: {e}")

def enable_mosquitto_at_boot():
    try:
        # Check if Mosquitto is installed
        result = subprocess.run(["which", "mosquitto"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Mosquitto is not installed. Install it using 'sudo apt install mosquitto'.")
            return

        # Enable Mosquitto to start at boot
        subprocess.run(["sudo", "systemctl", "enable", "mosquitto"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "mosquitto"], check=True)
        print("Mosquitto has been enabled to start at boot and is now running.")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while enabling Mosquitto: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")             


def check_dependencies(dependencies):
    """Check if the required dependencies are installed."""
    missing = []
    for dependency in dependencies:
        try:
            subprocess.run([sys.executable, "-m", dependency, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            missing.append(dependency)
        except FileNotFoundError:
            missing.append(dependency)
    return missing

def install_dependencies(missing):
    """Attempt to install missing dependencies."""
    for dependency in missing:
        print(f"Installing {dependency}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dependency], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to install {dependency}. Please install it manually.")
            return False
    return True

def main():
    """Main function to run the app."""
    # Define required dependencies
    dependencies = ["gpiozero","flask", "mosquitto", "mosquitto-clients", "paho-mqtt"]
    
    print("Checking dependencies...")
    missing = check_dependencies(dependencies)

    if missing:
        print(f"The following dependencies are missing: {', '.join(missing)}")
        install = input("Would you like to attempt to install them now? (yes/no): ").strip().lower()
        if install in ['yes', 'y']:
            if not install_dependencies(missing):
                print("Dependency installation failed. Exiting.")
                sys.exit(1)
        else:
            print("Dependencies are missing. Exiting.")
            sys.exit(1)

    print("All dependencies are installed!")
    # Open a browser to a specific URL
    url = "http://localhost:5000"
    print(f"Launching browser to {url}...")
    threads = []

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    threads.append(flask_thread)
    craneSetup()
    webbrowser.open(url)


# if __name__ == '__main__':
#     try:
#         if check_dependencies():
#             #list of threads
#             threads = []

#             # Start Flask in a separate thread
#             flask_thread = threading.Thread(target=run_flask)
#             flask_thread.start()
#             threads.append(flask_thread)
#             craneSetup()

#     except KeyboardInterrupt:
#         # Signal all threads to stop by setting the stop event
#                 # flask_thread.start()
#         # threads.append(flask_thread)stop_event.set()pwd

#         print("All threads have exited. Program is shutting down.")
#         print("Exiting...")
#     finally:
#         # cleanup()
#         print("clean up")
#         #sys.exit(0)

if __name__ == "__main__":
    main()