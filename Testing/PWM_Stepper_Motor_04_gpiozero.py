import curses
from gpiozero import OutputDevice
from time import sleep

# Pin setup (adjust GPIO pins according to your wiring)
STEP_PIN = 17  # GPIO pin for the step signal
DIR_PIN = 27   # GPIO pin for the direction control

# Set up the GPIO pins
step = OutputDevice(STEP_PIN)
direction = OutputDevice(DIR_PIN)

# Motor settings
steps_per_revolution = 800  # Assuming 200 steps for 1 full revolution (adjust if needed)
degrees_per_step = 360 / steps_per_revolution
steps_per_90_degrees = int(90 / degrees_per_step)
step_delay = 0.001  # Delay between steps (in seconds)

def rotate(steps, direction_forward=True):
    # Set direction
    direction.value = direction_forward
    # Perform the steps
    for _ in range(steps):
        step.on()
        sleep(step_delay)
        step.off()
        sleep(step_delay)

def main(stdscr):
    stdscr.nodelay(True)  # Make getch() non-blocking
    stdscr.clear()
    stdscr.addstr("Press Left Arrow for -90° and Right Arrow for +90°\n")
    stdscr.addstr("Press 'q' to quit.\n")
    
    last_key = None  # Store the last key press to debounce
    debounce_delay = 0.5  # Delay between key presses in seconds
    row_count = 4  # Track how many rows of text are on the screen

    while True:
        key = stdscr.getch()

        # Clear the screen every 10 lines to prevent overflow
        if row_count >= 10:
            stdscr.clear()
            stdscr.addstr("Press Left Arrow for -90° and Right Arrow for +90°\n")
            stdscr.addstr("Press 'q' to quit.\n")
            row_count = 4  # Reset the row counter

        if key == curses.KEY_LEFT and last_key != curses.KEY_LEFT:  # Left arrow key pressed
            stdscr.addstr("Rotating -90 degrees (counterclockwise)\n")
            rotate(steps_per_90_degrees, direction_forward=False)
            last_key = curses.KEY_LEFT
            row_count += 1  # Increment row count
            sleep(debounce_delay)  # Add debounce delay

        elif key == curses.KEY_RIGHT and last_key != curses.KEY_RIGHT:  # Right arrow key pressed
            stdscr.addstr("Rotating +90 degrees (clockwise)\n")
            rotate(steps_per_90_degrees, direction_forward=True)
            last_key = curses.KEY_RIGHT
            row_count += 1  # Increment row count
            sleep(debounce_delay)  # Add debounce delay

        elif key == ord('q'):  # Press 'q' to exit
            break

        else:
            last_key = None  # Reset last_key if no key is pressed

        stdscr.refresh()
        sleep(0.1)  # Small delay to prevent high CPU usage

# Main execution
if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Exiting...")
