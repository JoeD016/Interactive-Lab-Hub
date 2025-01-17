import time,datetime
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from time import strftime, sleep 
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
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

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    strDate = strftime('%A %m %b %Y')
    strTime = strftime('%H: %M: %S')
    strhour = strftime('%H')
    Hour = int(strhour)
    strmin = strftime('%M')
    Min = int(strmin)

    strsec = strftime('%S')
    Sec = int(strsec)



    number_of_coffee = Min/10


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
