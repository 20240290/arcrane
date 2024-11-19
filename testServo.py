# from classes.PWMServoMotor import PWMServoMotor
# import constants as const

# servo = PWMServoMotor(17)

# while True:
#     servo.rotate_motor(90)


# from gpiozero import Servo
# from time import sleep

# # Define the GPIO pin for the PWM signal (Pin 17 is just an example)
# servo = Servo(17)

# # Sweep the servo back and forth
# while True:
#     servo.min()  # Move the servo to the minimum position
#     sleep(1)     # Wait for 1 second
#     servo.max()  # Move the servo to the maximum position
#     sleep(1)  

from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import pigpio

# Connect to the local PiGPIO daemon
factory = PiGPIOFactory()

# Use a pin for PWM, GPIO17 for example
servo = Servo(17, pin_factory=factory)

while True:
    servo.min()  # Set to minimum position
    sleep(1)
    servo.mid()  # Set to center
    sleep(1)
    servo.max()  # Set to maximum position
    sleep(1)