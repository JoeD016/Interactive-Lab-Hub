import digitalio
import board

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors

import time,datetime
import subprocess

from PIL import Image, ImageDraw, ImageFont
from time import strftime, sleep 
from pytz import timezone


# The display uses a communication protocol called SPI.
# SPI will not be covered in depth in this course. 
# you can read more https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # the rate  the screen talks to the pi
# Create the ST7789 display:
display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)


# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()



cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
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

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)

font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 6)
# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


est = timezone('EST')
est_now = datetime.now(est)
bij = timezone('Asia/Beijing')
bij_now = datetime.now(bij)


# Main loop:
while True:
    if not buttonA.value: # New York Time display
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        strDate = est_now.strftime('%A %m %b %Y')
        strTime = est_now.strftime('%H: %M: %S')
        strhour = est_now.strftime('%H')
        Hour = int(strhour)
        strmin = est_now.strftime('%M')
        Min = int(strmin)

        strsec = est_now.strftime('%S')
        Sec = int(strsec)



        number_of_coffee = Min/10
        draw.rectangle((0, 0, width, height), outline=0, fill=0)  
        draw.text((x,top),strDate, font = font, fill ="#ffffff")
        draw.text((x+24,top+32),strhour+"  O'Clock", font = font1, fill ="#FFFF00")
        draw.text((x+50,top+58),"and  "+str(int(number_of_coffee))+"  coffee",font=font1,fill = "#FFFF00")
        draw.text((x+78,top+86),strTime, font = font, fill = "#FFFF00")
        draw.text((x+5,top+78),"   *   *    *",font = font2, fill = "#ffffff")
        draw.text((x+5,top+84),"  *   *    *", font = font2, fill = "#ffffff")
        draw.text((x+5,top+90),"   *   *    *", font = font2, fill = "#ffffff")
        draw.text((x+5,top+96),"  *   *    *", font = font2, fill = "#ffffff")
        draw.text((x+5,top+102),"***************", font = font2, fill = "#ffffff")
        draw.text((x+5,top+108),"  ***********   * ", font = font2, fill = "#ffffff")
        draw.text((x+5,top+114),"   *********    *", font = font2, fill = "#ffffff")
        draw.text((x+5,top+120),"    ******* **** ", font = font2, fill = "#ffffff")
        draw.text((x+5,top+126),"     *****   ", font = font2, fill = "#ffffff")
    # Display image.
        disp.image(image, rotation)
        time.sleep(1)


        
        
    
    if not buttonB.value:  # just button B pressed    Beijing Time
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        strDate = bij_now.strftime('%A %m %b %Y')
        strMinSec = bij_now.strftime('%M: %S')
        strhour = bij_now.strftime('%H')
        Hour = int(strhour)
        # if Hour > 12:
        #     Hour -= 12
        # else:
        #     Hour += 12
        strmin = bij_now.strftime('%M')
        Min = int(strmin)

        strsec = bij_now.strftime('%S')
        Sec = int(strsec)
        strTime = str(Hour) + ": " + strMinSec



        number_of_coffee = Min/10

        

        draw.rectangle((0, 0, width, height), outline=0, fill=0)  
        draw.text((x,top),strDate, font = font, fill ="#ffffff")
        draw.text((x+24,top+32),str(Hour)+"  O'Clock", font = font1, fill ="#FFFF00")
        draw.text((x+50,top+58),"and  "+str(int(number_of_coffee))+"  coffee",font=font1,fill = "#FFFF00")
        draw.text((x+78,top+86),strTime, font = font, fill = "#FFFF00")
        draw.text((x+5,top+78),"   *   *    *",font = font2, fill = "#ffffff")
        draw.text((x+5,top+84),"  *   *    *", font = font2, fill = "#ffffff")
        draw.text((x+5,top+90),"   *   *    *", font = font2, fill = "#ffffff")
        draw.text((x+5,top+96),"  *   *    *", font = font2, fill = "#ffffff")
        draw.text((x+5,top+102),"***************", font = font2, fill = "#ffffff")
        draw.text((x+5,top+108),"  ***********   * ", font = font2, fill = "#ffffff")
        draw.text((x+5,top+114),"   *********    *", font = font2, fill = "#ffffff")
        draw.text((x+5,top+120),"    ******* **** ", font = font2, fill = "#ffffff")
        draw.text((x+5,top+126),"     *****   ", font = font2, fill = "#ffffff")
    # Display image.
        disp.image(image, rotation)
        time.sleep(1)




