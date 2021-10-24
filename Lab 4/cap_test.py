import time
import board
import busio

import adafruit_mpr121
import os

import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

# For use with the STEMMA connector on QT Py RP2040
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
# seesaw = seesaw.Seesaw(i2c, 0x36)

seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None

# while True:

#     # negate the position to make clockwise rotation positive
#     position = -encoder.position

#     if position != last_position:
#         last_position = position
#         print("Position: {}".format(position))

#     if not button.value and not button_held:
#         button_held = True
#         print("Button pressed")

#     if button.value and button_held:
#         button_held = False
#         print("Button released")

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

while True:
    # position = -encoder.position
    # if position != last_position:
    #     last_position = position
    #     print("Position: {}".format(position))

    # if not button.value and not button_held:
    #     button_held = True
    #     print("Button pressed")

    # if button.value and button_held:
    #     button_held = False
    #     print("Button released")


    for i in range(9):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
            os.system('mpg321 position{i}.mp3 &')
    time.sleep(0.25)  # Small delay to keep from spamming output messages.
