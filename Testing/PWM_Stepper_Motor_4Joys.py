import curses
from gpiozero import OutputDevice
from time import sleep

# Pin setup for Motor 1
M1_STEP_PIN = 17  # GPIO pin for the step signal
M1_DIR_PIN = 27   # GPIO pin for the direction control

# Pin setup for Motor 2
M2_STEP_PIN = 22  # GPIO pin for the step signal
M2_DIR_PIN = 23   # GPIO pin for the direction control

# Pin setup for Motor 3
M3_STEP_PIN = 5   # GPIO pin for the step signal
M3_DIR_PIN = 6    # GPIO pin for the direction control

# Pin setup for Motor 4
M4_STEP_PIN = 12  # GPIO pin for the step signal
M4_DIR_PIN = 13   # GPIO pin for the direction control

# Set up the GPIO pins for each motor
motor1_step = OutputDevice(M1_STEP_PIN)
motor1_dir = OutputDevice(M1_DIR_PIN)

motor2_step = OutputDevice(M2_STEP_PIN)
motor2_dir = OutputDevice(M2_DIR_PIN)

motor3_step = OutputDevice(M3_STEP_PIN)
motor3_dir = OutputDevice(M3_DIR_PIN)

motor4_step = OutputDevice(M4_STEP_PIN)
motor4_dir = OutputDevice(M4_DIR_PIN)

# Motor settings
steps_per_revolution = 200  # Assuming 200 steps for 1 full revolution (adjust if needed)
step_delay = 0.001  # Delay between steps (in seconds)

def rotate_motor(step_pin, dir_pin, direction_forward=True):
    """Rotate the specified motor one step."""
    dir_pin.value = direction_forward
    step_pin.on()
    sleep(step_delay)
    step_pin.off()
    sleep(step_delay)

def main(stdscr):
    stdscr.nodelay(True)  # Make getch() non-blocking
    stdscr.clear()
    stdscr.addstr("Press 1/2/3/4 to control motor 1/2/3/4 respectively.\n")
    stdscr.addstr("Hold Left Arrow for continuous counterclockwise rotation and Right Arrow for clockwise.\n")
    stdscr.addstr("Press 'q' to quit.\n")

    current_motor = 1  # Default to motor 1
    row_count = 4  # Keep track of printed rows

    while True:
        key = stdscr.getch()

        # Clear the screen every 10 lines to prevent overflow
        if row_count >= 10:
            stdscr.clear()
            stdscr.addstr("Press 1/2/3/4 to control motor 1/2/3/4 respectively.\n")
            stdscr.addstr("Hold Left Arrow for continuous counterclockwise rotation and Right Arrow for clockwise.\n")
            stdscr.addstr("Press 'q' to quit.\n")
            row_count = 4  # Reset the row count

        # Switch between motors using 1, 2, 3, 4 keys
        if key == ord('1'):
            current_motor = 1
            stdscr.addstr("Motor 1 selected.\n")
            row_count += 1

        elif key == ord('2'):
            current_motor = 2
            stdscr.addstr("Motor 2 selected.\n")
            row_count += 1

        elif key == ord('3'):
            current_motor = 3
            stdscr.addstr("Motor 3 selected.\n")
            row_count += 1

        elif key == ord('4'):
            current_motor = 4
            stdscr.addstr("Motor 4 selected.\n")
            row_count += 1

        # Handle motor rotation based on key press (continuous as long as key is held)
        if key == curses.KEY_LEFT:
            stdscr.addstr(f"Rotating Motor {current_motor} counterclockwise (continuous)\n")
            row_count += 1
            if current_motor == 1:
                rotate_motor(motor1_step, motor1_dir, direction_forward=False)
            elif current_motor == 2:
                rotate_motor(motor2_step, motor2_dir, direction_forward=False)
            elif current_motor == 3:
                rotate_motor(motor3_step, motor3_dir, direction_forward=False)
            elif current_motor == 4:
                rotate_motor(motor4_step, motor4_dir, direction_forward=False)

        elif key == curses.KEY_RIGHT:
            stdscr.addstr(f"Rotating Motor {current_motor} clockwise (continuous)\n")
            row_count += 1
            if current_motor == 1:
                rotate_motor(motor1_step, motor1_dir, direction_forward=True)
            elif current_motor == 2:
                rotate_motor(motor2_step, motor2_dir, direction_forward=True)
            elif current_motor == 3:
                rotate_motor(motor3_step, motor3_dir, direction_forward=True)
            elif current_motor == 4:
                rotate_motor(motor4_step, motor4_dir, direction_forward=True)

        # Stop rotation when no key is pressed
        if key == -1:
            pass  # Do nothing, stop rotation

        # Quit the program
        if key == ord('q'):
            break

        # Sleep to prevent overloading CPU
        stdscr.refresh()
        sleep(0.01)

# Main execution
if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Exiting...")
