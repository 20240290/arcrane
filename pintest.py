from gpiozero import Device
# from gpiozero.pins.native import NativeFactory

# # Set gpiozero to use the native GPIO factory
# Device.pin_factory = NativeFactory()

# available_pins = []
# unavailable_pins = []

# for gpio in range(28):  # Raspberry Pi has GPIOs 0-27 for general-purpose use
#     try:
#         pin = Device.pin_factory.pin(gpio)
#         pin.function = "input"  # Try to set pin as input
#         available_pins.append(gpio)
#         pin.close()  # Release the pin after testing
#     except Exception as e:
#         unavailable_pins.append(gpio)

# print("Available GPIO pins:", available_pins)
# print("Unavailable GPIO pins:", unavailable_pins)


from gpiozero import Device, DigitalInputDevice

available_pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]
print("Available GPIO pins and their states:")

for pin in available_pins:
    try:
        gpio = DigitalInputDevice(pin)
        print(f"Pin {pin}: {'HIGH' if gpio.is_active else 'LOW'}")
    except Exception as e:
        print(f"Pin {pin}: ERROR ({e})")