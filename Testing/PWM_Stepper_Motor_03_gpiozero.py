from gpiozero import OutputDevice
from time import sleep

# Define GPIO pinspip 
ENA_PIN = 17  # GPIO pin connected to the ENA (enable) pin on TB6600
DIR_PIN = 27  # GPIO pin connected to the DIR (direction) pin on TB6600
PUL_PIN = 22  # GPIO pin connected to the PUL (pulse) pin on TB6600

# Initialize OutputDevice for ENA, DIR, and PUL
enable = OutputDevice(ENA_PIN, active_high=False)  # Assuming ENA is active low
direction = OutputDevice(DIR_PIN, active_high=True)  # DIR is typically active high
pulse = OutputDevice(PUL_PIN, active_high=True)      # PUL is typically active high

def rotate_motor(steps, direction_value=1, pulse_delay=0.01):
    """
    Rotate the stepper motor.

    :param steps: Number of steps to rotate the motor.
    :param direction_value: Direction of rotation (1 for one direction, 0 for the other).
    :param pulse_delay: Delay between pulses (in seconds).
    """
    direction.value = direction_value  # Set the direction
    enable.on()  # Enable the driver
    for _ in range(steps):
        pulse.on()  # Send a pulse
        sleep(pulse_delay)
        pulse.off()  # End the pulse
        sleep(pulse_delay)
    enable.off()  # Disable the driver after moving

# Example usage
try:
    while True:
        print("Rotating motor clockwise")
        rotate_motor(200, direction_value=1, pulse_delay=0.05)  # Rotate 200 steps clockwise
        sleep(1)
        print("Rotating motor counter-clockwise")
        rotate_motor(200, direction_value=0, pulse_delay=0.05)  # Rotate 200 steps counter-clockwise
        sleep(1)
except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    # Cleanup GPIO state
    enable.off()
    direction.off()
    pulse.off()
