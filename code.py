# C I 510 X Text Based Adventure GamePad
# Matthew Nelson, Scott K, Megan McCleary

import board, neopixel, displayio, terminalio
from adafruit_display_text import label

import array
import math
import time
import audioio
import pulseio
import touchio
import digitalio
import analogio
import os

# Create the touch objects on the first and last teeth
back_button = touchio.TouchIn(board.TOUCH1)
forward_button = touchio.TouchIn(board.TOUCH4)

# Pre-define colors for NeoPixel
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (0, 100, 255)
WHITE = (255, 255, 255)

# Setup LED and Light Sensor pins
LED_PIN = board.D13  # Pin number for the board's built in LED.
LIGHT_SENSE = analogio.AnalogIn(board.A1)   # Light sensor is connected to A1 on Hallowing

# Setup digital output for LED:
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

# Setup NeoPixel
NP = neopixel.NeoPixel(board.NEOPIXEL,1,brightness=0.5)

#-------------------------------------------------
# Graphics Display Setup
#-------------------------------------------------

#backlight = pulseio.PWMOut(board.TFT_BACKLIGHT)
max_brightness = 2 ** 15
splash = displayio.Group()
board.DISPLAY.show(splash)
#Image database, all images can be referenced from this list
images = ["media/corn.bmp", "media/iigs.bmp", "media/oregon.bmp",
          "media/macos-9.bmp", "media/organic_start.bmp"]

#---------------------------------------------------
# Audio Setup
#---------------------------------------------------

# tone player setup for status beeps
tone_volume = 0.1  # Increase this to increase the volume of the tone.
frequency_hz = 880  # Set this to the Hz of the tone you want to generate.
length = 8000 // frequency_hz
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))

sine_wave_sample = audioio.RawSample(sine_wave)
# Setup audio out pin
audio = audioio.AudioOut(board.A0)


#------------------------------------------------------
# Functions
#-----------------------------------------------------

# Initilize function for first time power on
def init():
  NP.fill(RED)
  NP.show()
  print("Booting up Hallowing...")
  time.sleep(1)
  print("Testing Light Sensor...")
  print("Current light value is:",LIGHT_SENSE.value)
  time.sleep(1)
  board.DISPLAY.auto_brightness = False
  board.DISPLAY.brightness = 0.33
  board.DISPLAY.show(splash)
  return splash

#--------------------------------------------------
# Audio Functions
#--------------------------------------------------

def load_wav(name):
    """
    Load a WAV audio file into RAM.
    @param name: partial file name string, complete name will be built on
                 this, e.g. passing 'foo' will load file 'foo.wav'.
    @return WAV buffer that can be passed to play_wav() below.
    """
    return audioio.WaveFile(open(name + '.wav', 'rb'))

def play_wav(wav):
    """
    Play a WAV file previously loaded with load_wav(). This function
    "blocks," i.e. does not return until the sound is finished playing.
    @param wav: WAV buffer previously returned by load_wav() function.
    """
    audio.play(wav)      # Begin WAV playback
    while audio.playing: # Keep idle here as long as it plays
        pass
    time.sleep(1)        # A small pause avoids repeated triggering

STARTUP_WAV = load_wav('media\macos-10-1') # Startup sound
# Function for beeping, usage: 'beep(3)' will beep 3x
def beep(count):
    for _ in range(count):
        audio.play(sine_wave_sample, loop=True)
        time.sleep(0.1)
        audio.stop()
        time.sleep(0.05)

#-----------------------------------------------------------
# Graphic functions
#-----------------------------------------------------------

# Function for writing text to the screen
def draw_text(txt,x_pos,y_pos,txt_scale):
  ta = label.Label(terminalio.FONT, text=txt)
  ta.scale=txt_scale
  ta.x=x_pos
  ta.y=y_pos
  board.DISPLAY.show(ta)
  board.DISPLAY.wait_for_frame()
  return ta

# Function for displaying images on HalloWing TFT screen
def show_image(filename):
    image_file = open(filename, "rb")
    odb = displayio.OnDiskBitmap(image_file)
    face = displayio.TileGrid(odb, pixel_shader=displayio.ColorConverter(), x=0,y=0)
    #backlight.duty_cycle = 0
    splash.append(face)
    # Wait for the image to load.
    board.DISPLAY.wait_for_frame()
    #backlight.duty_cycle = max_brightness

#------------------------------------------------------------------------------------

init()
show_image(images[3])
play_wav(STARTUP_WAV)
board.DISPLAY.show(splash)
time.sleep(1)
show_image(images[4])  # waiting display
time.sleep(1)
draw_text("Organic\n Trail",10,30,2)
time.sleep(1)
# This will blank out the display otherwise it will repeat the previous image loaded
splash = displayio.Group()
board.DISPLAY.show(splash)
draw_text("Welcome to \n Organic Trail! \n To continue, \n press the right \n pad.",10,50,1)
loop1 = True
while loop1:
    if forward_button.value:
        print("Button touched!")
        loop1 = False

board.DISPLAY.show(splash)
draw_text("How are you going \n to grow? \n Left pad - Traditional \n Right Pad - Organic",2,50,1)
loop1 = True
while loop1:
    if back_button.value:
        print("Traditional Picked")
        farm = "Traditional"
        loop1 = False
        NP.fill(PURPLE)
        NP.show()
    if forward_button.value:
        print("Organic Picked")
        farm = "Organic"
        loop1 = False
        NP.fill(BLUE)
        NP.show()

board.DISPLAY.show(splash)
farm_text = "You picked "+farm
draw_text(farm_text,10,30,1)
board.DISPLAY.show(splash)
draw_text("What are you going \n to grow? \n Left pad - Corn \n Right Pad - Soybean",5,50,1)
loop1 = True
while loop1:
    if back_button.value:
        print("Corn picked")
        plant = "Corn"
        loop1 = False
        show_image(images[0])
    if forward_button.value:
        print("Soybean picked")
        plant = "Soybean"
        loop1 = False
time.sleep(1)
board.DISPLAY.show(splash)
time.sleep(1)
plant_text = "You picked "+plant
draw_text(plant_text,10,30,1)
time.sleep(10)