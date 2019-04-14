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
#images_db = ["media/no_light.bmp", "media/welcome.bmp", "media/9seed.bmp", "media/macos-8.bmp",
 #           "media/organic_start.bmp", "media/2years.bmp", "media/3bankloan.bmp", "media/10start.bmp"]
images_db = list(filter(lambda x: x.endswith("bmp"), sorted(os.listdir("/media"))))
#images_intro = list(filter(lambda x: x.endswith("bmp"), sorted(os.listdir("/media/intro"))))
#images_organic = list(filter(lambda x: x.endswith("bmp"), sorted(os.listdir("/media/organic"))))
#images_corn = list(filter(lambda x: x.endswith("bmp"), sorted(os.listdir("/media/organic"))))
#images_corn = list(filter(lambda x: x.endswith("bmp"), sorted(os.listdir("/media/organic"))))
print(images_db)
#print(images_intro)
#print(images_organic)

#Global Fade Timer
fade_timer = 0.01

#Light Threshold
light_threshold = 15000

#---------------------------------------------------
# Audio Setup
#---------------------------------------------------

# Setup audio out pin
audio = audioio.AudioOut(board.A0)

# set up time signature
#whole_note = 1.5  # adjust this to change tempo of everything
# these notes are fractions of the whole note
#half_note = whole_note / 2
#quarter_note = whole_note / 4
#dotted_quarter_note = quarter_note * 1.5
#eighth_note = whole_note / 8

# List of notes and their tone in Hz
#A3 = 220
#Bb3 = 233
#B3 = 247
#C4 = 262
#Db4 = 277
#D4 = 294
#Eb4 = 311
#E4 = 330
#F4 = 349
#Gb4 = 370
#G4 = 392
#Ab4 = 415
#A4 = 440
#Bb4 = 466
#B4 = 493
#C5 = 523
#Db5 = 554
#D5 = 587
#Eb5 = 622
#E5 = 659
#F5 = 698
#Gb5 = 740
#G5 = 784

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
PURPLE = (0, 100, 255)
WHITE = (255, 255, 255)
SKYBLUE = (0, 20, 200)
BLACK = (0,0,0)

#----------------------------------------------------
#D13 LED and Light Sensor
#----------------------------------------------------
# Setup LED and Light Sensor pins
#LED_PIN = board.D13  # Pin number for the board's built in LED.
LIGHT_SENSE = analogio.AnalogIn(board.A1)   # Light sensor is connected to A1 on Hallowing

# Setup digital output for LED:
#led = digitalio.DigitalInOut(LED_PIN)
#led.direction = digitalio.Direction.OUTPUT

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
    """
    Load a WAV audio file into RAM.
    @param name: partial file name string, complete name will be built on
                 this, e.g. passing 'foo' will load file 'foo.wav'.
    @return WAV buffer that can be passed to play_wav() below.
    """
    return audioio.WaveFile(open(name + '.wav', 'rb'))

STARTUP_WAV = load_wav('media\macos-10-1') # Startup sound
#CASH = load_wav('media\cash')

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

# Function for beeping, usage: 'beep(3)' will beep 3x
'''
def play_tone(freq,vol,note_length):
    frequency_hz = freq  # Set this to the Hz of the tone you want to generate.
    length = 8000 // frequency_hz
    sine_wave = array.array("H", [0] * length)
    for i in range(length):
        sine_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * vol * (2 ** 15 - 1))
    sine_wave_sample = audioio.RawSample(sine_wave)
    audio.play(sine_wave_sample,loop=True)
    time.sleep(note_length)
    audio.stop()
'''

'''
def play_song(song_number,vol):

    if song_number == 2:
        # Home on the Range
        home_range_song = [
            [C4, quarter_note],
            [C4, quarter_note],
            [F4, quarter_note],
            [G4, quarter_note],
            [A4, half_note],
            [F4, eighth_note],
            [E4, eighth_note],
            [D4, quarter_note],
            [Bb4, quarter_note],
            [Bb4, quarter_note],
            [Bb4, half_note],
            [A4, eighth_note],
            [Bb4, eighth_note],
            [C5, half_note],
            [F4, eighth_note],
            [F4, eighth_note],
            [F4, quarter_note],
            [E4, quarter_note],
            [F4, quarter_note],
            [G4, whole_note],

        ]
        for i in home_range_song:
            play_tone(i[0],vol,i[1])
'''
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

# Function for writing text to the screen

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
            show_image(images_db[scene_right])  # waiting display
            wait_for_touch()
            loop1 = False
        if back_button.value:
            print("Left choice made")
            choice = "Left"
            fade_down(fade_timer)
            splash.pop()
            show_image(images_db[scene_left])  # waiting display
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
            print("There enough light!")
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
    show_image(images_db[30])  # waiting display
    choice = touch_choice(32,31)
    if choice == "Right":
        insurance = False
    else:
        insurance = True
    print("Insurance is ",insurance)
    fade_down(fade_timer)
    splash.pop()
    show_image(images_db[33])  # waiting display
    wait_for_touch()
    fade_down(fade_timer)
    splash.pop()
    grow_scene("corn_growing.bmp")

    for i in range(36,45 ,1):
        show_image(images_db[i])  # waiting display
        wait_for_touch()
        fade_down(fade_timer)
        splash.pop()

def organic_soybean_scene():
    for i in range(2,20,1):
        show_image(images_db[i])  # waiting display
        wait_for_touch()
        fade_down(fade_timer)
        splash.pop()

#------------------------------------------------------------------------------------
init()
#show_image(images_db[0])
#play_wav(STARTUP_WAV)
#fade_down(fade_timer)
#splash.pop()
NP.fill(BLUE)
NP.show()
show_image(images_db[1])  # waiting display
#play_tone(G4,1,whole_note)
NP.fill(GREEN)
NP.show()
#play_song(2,0.3)
time.sleep(1)
fade_down(fade_timer)
splash.pop()
NP.fill(SKYBLUE)
NP.show()
#scene_player(2,20)
show_image(images_db[20])  # waiting display
choice = touch_choice(22,21)
if choice == "Right":
    farm = "Traditional"
else:
    farm = "Organic"

print("The decision made is",farm)
fade_down(fade_timer)
splash.pop()
scene_player(23,28)
show_image(images_db[29])  # waiting display
choice = touch_choice(31,30)
if choice == "Right":
    crop = "Soybean"
else:
    crop = "Corn"
print("The decision made is",crop)

if crop == "Corn" and farm == "Organic":
    organic_corn_scene()

if crop == "Soybean" and farm == "Organic":
    organic_soybean_scene()