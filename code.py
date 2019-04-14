# C I 510 X Text Based Adventure
# Programming by Matthew Nelson
# Artwork and text by Scott K
# Text, ideas, and making sure this actually makes sense by Megan McCleary

# Some code sections are from Adafruit's Learning Modules
# https://learn.adafruit.com

#-------------------------------------------
# Imports
#-------------------------------------------

import board, neopixel, displayio

#import array
import math
import time
import random
import audioio
import pulseio
import touchio
import digitalio
import analogio
import os

#-------------------------------------------
# Graphics Setup
#-------------------------------------------
# Display brightness now controlled with DISPLAY
# In the beta versions fo CircuitPython

board.DISPLAY.auto_brightness = False
board.DISPLAY.brightness = 0
splash = displayio.Group()
board.DISPLAY.show(splash)

# Image Database
#Image database, all images can be referenced from this list
images_db = list(filter(lambda x: x.endswith("bmp"), sorted(os.listdir("/media"))))
print(images_db)

#Global Fade Timer
fade_timer = 0.01

#Light Threshold
light_threshold = 15000

#---------------------------------------------------
# Audio Setup
#---------------------------------------------------

# Setup audio out pin
audio = audioio.AudioOut(board.A0)

#----------------------------------------------------
# Touch sensors
#----------------------------------------------------
# Create the touch objects on the first and last teeth
back_button = touchio.TouchIn(board.TOUCH1)
forward_button = touchio.TouchIn(board.TOUCH4)

#----------------------------------------------------
# Neopixel
#----------------------------------------------------
# Setup NeoPixel
NP = neopixel.NeoPixel(board.NEOPIXEL,1,brightness=0.5)
# Pre-define colors for NeoPixel
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255,195,0)
PURPLE = (0, 100, 255)
WHITE = (255, 255, 255)
SKYBLUE = (0, 20, 200)
BLACK = (0,0,0)
#YELLOW = (255,165,0)

# Setup LED and Light Sensor pins
#LED_PIN = board.D13  # Pin number for the board's built in LED.
LIGHT_SENSE = analogio.AnalogIn(board.A1)   # Light sensor is connected to A1 on Hallowing

#------------------------------------------------------
# Functions
#-----------------------------------------------------

# Initilize function for first time power on
def init():
  NP.fill(SKYBLUE)
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

    return audioio.WaveFile(open(name + '.wav', 'rb'))

STARTUP_WAV = load_wav('media\macos-10-1') # Startup sound
#CASH = load_wav('media\cash')

def play_wav(wav):

    audio.play(wav)      # Begin WAV playback
    while audio.playing: # Keep idle here as long as it plays
        pass
    time.sleep(1)        # A small pause avoids repeated triggering

#-----------------------------------------------------------
# Graphic functions
#-----------------------------------------------------------

# Function to fade up the backlight
def fade_up(fade_time):
    for i in range(100):
        board.DISPLAY.brightness = 0.01 * i
        time.sleep(fade_time)

# Function to fade down the backlight
def fade_down(fade_time):
    for i in range(100, -1, -1):
            board.DISPLAY.brightness = 0.01 * i
            time.sleep(fade_time)  # default (0.005)

# Function for displaying images on HalloWing TFT screen
def show_image(filename):
    filename = "/media/" + filename
    print(filename)
    image_file = open(filename, "rb")
    odb = displayio.OnDiskBitmap(image_file)
    face = displayio.TileGrid(odb, pixel_shader=displayio.ColorConverter(), x=0,y=0)
    splash.append(face)
    # Wait for the image to load.
    board.DISPLAY.wait_for_frame()
    fade_up(fade_timer)

def wait_for_touch():
    loop1 = True
    while loop1:
        if forward_button.value:
            print("Button touched!")
            loop1 = False

def touch_choice(scene_right,scene_left):
    loop1 = True
    while loop1:
        if forward_button.value:
            print("Right choice made")
            choice = "Right"
            fade_down(fade_timer)
            splash.pop()
            show_image(scene_right)  # waiting display
            wait_for_touch()
            loop1 = False
        if back_button.value:
            print("Left choice made")
            choice = "Left"
            fade_down(fade_timer)
            splash.pop()
            show_image(scene_left)  # waiting display
            wait_for_touch()
            loop1 = False
    return choice

def grow_scene(scene):
    loop1 = True
    i = 0
    while loop1:
        if LIGHT_SENSE.value < light_threshold :
            NP.fill(RED)
            NP.show()
            show_image("no_light.bmp")
            time.sleep(1)
            fade_down(fade_timer)
            splash.pop()
            print("Current light value is:",LIGHT_SENSE.value)
            print("There is not enough light")
            time.sleep(1)
        else:
            NP.fill(SKYBLUE)
            NP.show()
            show_image(scene)
            time.sleep(1)
            fade_down(fade_timer)
            splash.pop()
            print("Current light value is:",LIGHT_SENSE.value)
            print("There is enough light!")
            i += 1
            time.sleep(1)
        if i == 5:
            loop1 = False

def scene_player(start,end):
    for i in range(start,end,1):
        show_image(images_db[i])  # waiting display
        wait_for_touch()
        fade_down(fade_timer)
        splash.pop()

def organic_corn_scene():
    fade_down(fade_timer)
    splash.pop()
    show_image(images_db[28])  # waiting display
    choice = touch_choice("2c.bmp","2b.bmp")
    if choice == "Right":
        insurance = False
    else:
        insurance = True
    print("Insurance is",insurance)
    fade_down(fade_timer)
    splash.pop()
    scene_player(31,34)
    grow_scene("corn_growing.bmp")
    scene_player(34,38)
    NP.fill(RED)
    NP.show()
    scene_player(38,40)
    if insurance == True:
        show_image(images_db[40])  # waiting display
        wait_for_touch()
    else:
        show_image(images_db[41])  # waiting display
        wait_for_touch()
    NP.fill(ORANGE)
    NP.show()
    scene_player(42,49)

def organic_soybean_scene():
    fade_down(fade_timer)
    splash.pop()
    show_image(images_db[49])  # waiting display
    choice = touch_choice("3c.bmp","3b.bmp")
    if choice == "Right":
        insurance = False
    else:
        insurance = True
    print("Insurance is",insurance)
    fade_down(fade_timer)
    splash.pop()
    scene_player(52,55)
    grow_scene("soybean_growing.bmp")
    scene_player(55,59)
    NP.fill(RED)
    NP.show()
    scene_player(59,61)
    if insurance == True:
        show_image(images_db[61])  # waiting display
        wait_for_touch()
    else:
        show_image(images_db[62])  # waiting display
        wait_for_touch()
    NP.fill(ORANGE)
    NP.show()
    scene_player(63,70)

#------------------------------------------------------------------------------------
init()
show_image(images_db[0])
play_wav(STARTUP_WAV)
fade_down(fade_timer)
splash.pop()
NP.fill(BLUE)
NP.show()
show_image(images_db[1])  # waiting display
NP.fill(GREEN)
NP.show()
time.sleep(2)
fade_down(fade_timer)
splash.pop()
NP.fill(SKYBLUE)
NP.show()
scene_player(2,20)
show_image(images_db[20])  # waiting display
choice = touch_choice("traditional.bmp","organic.bmp")
if choice == "Right":
    farm = "Traditional"
else:
    farm = "Organic"

print("The decision made is",farm)
fade_down(fade_timer)
splash.pop()
scene_player(21,27)
show_image(images_db[27])  # waiting display
choice = touch_choice("soybean_picked.bmp","corn_picked.bmp")
if choice == "Right":
    crop = "Soybean"
else:
    crop = "Corn"
print("The decision made is",crop)

if crop == "Corn":
    organic_corn_scene()

if crop == "Soybean":
    organic_soybean_scene()

fade_down(fade_timer)
splash.pop()
show_image("thanks.bmp")