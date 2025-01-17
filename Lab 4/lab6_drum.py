import time
import board
import busio

import adafruit_mpr121
import os

import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

import time


import digitalio
import board

from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789




import os
import paho.mqtt.client as mqtt
import uuid

import board
import busio
import adafruit_apds9960.apds9960
import time
import paho.mqtt.client as mqtt
import uuid
import signal

import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

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

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
spi = board.SPI()
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)


height = disp.width  
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

padding = -2
top = padding
bottom = height - padding
x = 0

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

draw.rectangle((0, 0, width, height), outline=0, fill=0)


# while True:
#     position = -encoder.position
#     if position != last_position:
#         last_position = position
#         print("Position: {}".format(position))

#     if position == 1:
#         ma_img = Image.open("drum_title.jpg")
#         ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
#         disp.image(ma_img, rotation)
    
#     if position == 2:
#         ma_img = Image.open("chinese_drum.jpg")
#         ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
#         disp.image(ma_img, rotation)
    
#     if position == 3:
#         ma_img = Image.open("memes.jpg")
#         ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
#         disp.image(ma_img, rotation)

    # if not button.value and not button_held:
    #     button_held = True
    #     print("Button pressed")

    # if button.value and button_held:
    #     button_held = False
    #     print("Button released")
position = 1

topic = 'IDD/JOJO/drum'

def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
    my_rgb = msg.payload.decode('UTF-8')
    res = int(my_rgb)
    os.system(f'mpg321 drum{position}{res}.mp3 &')

	# print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
	# you can filter by topics
	# if msg.topic == 'IDD/some/other/topic': do thing


# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

# this is blocking. to see other ways of dealing with the loop
#  https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#network-loop
client.loop_forever()