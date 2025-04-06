import smbus
import time
def initializeI2c():
    # Create an SMBus instance
    bus = smbus.SMBus(1)  # Use 1 for Raspberry Pi (newer models)

    SLAVE_ADDRESS = 0x04  # Replace with the actual address of the slave

    try:
        while True:
            # Send data
            data = [0x01, 0x02, 0x03]  # Example data
            bus.write_i2c_block_data(SLAVE_ADDRESS, 0, data)
            print("Sent:", data)
            time.sleep(1)  # Send every second
    except KeyboardInterrupt:
        pass
