from gpiozero import Button
from signal import pause
from gpiozero.pins.native import NativeFactory
from adafruit_servokit import ServoKit
import time

# Optionally, set the pin factory to native
Button.pin_factory = NativeFactory()

button = Button(17) # define Button pin according to BCM Numbering

# Initialize PCA9685 (16-channel PWM)
kit = ServoKit(channels=16)

claw = 0  # claw channel
claw_rotation = 1 # claw rotation channel

def gradual_move_servo(channel, target_angle, step=1, delay=0.01):
    """Gradually moves a servo to the target angle."""
    current_angle = kit.servo[channel].angle or 0  # Get current angle or default to 0
    step = step if target_angle > current_angle else -step  # Adjust step direction
    
    for angle in range(int(current_angle), target_angle + step, step):
        kit.servo[channel].angle = angle
        time.sleep(delay)

def loop():
    while True:
        if button.is_pressed: # if button is pressed
            print("Button is pressed") # print information on terminal
            gradual_move_servo(claw, 35)
            time.sleep(1)
        else : # if button is relessed
            print("Button is released")
            gradual_move_servo(claw, 120)
            time.sleep(1)

if __name__ == '__main__': # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        print("Ending program")
    