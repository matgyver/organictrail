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

import array
import math
import time
import random
import audioio
import pulseio
import touchio
import digitalio
import analogio
import os
import busio
import adafruit_lis3dh

#-------------------------------------------
# Setup for HW
#-------------------------------------------

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
images_db = ["media/no_light.bmp", "media/welcome.bmp", "media/oregon.bmp", "media/macos-8.bmp", "media/organic_start.bmp"]

#images_db = list(filter(lambda x: x.endswith("bmp"), os.listdir("/")))
print(images_db)

#Global Fade Timer
fade_timer = 0.05

#---------------------------------------------------
# Audio Setup
#---------------------------------------------------

# Setup audio out pin
audio = audioio.AudioOut(board.A0)

# set up time signature
whole_note = 1.5  # adjust this to change tempo of everything
# these notes are fractions of the whole note
half_note = whole_note / 2
quarter_note = whole_note / 4
dotted_quarter_note = quarter_note * 1.5
eighth_note = whole_note / 8

A3 = 220
Bb3 = 233
B3 = 247
C4 = 262
Db4 = 277
D4 = 294
Eb4 = 311
E4 = 330
F4 = 349
Gb4 = 370
G4 = 392
Ab4 = 415
A4 = 440
Bb4 = 466
B4 = 493
C5 = 523
Db5 = 554
D5 = 587
Eb5 = 622
E5 = 659
F5 = 698
Gb5 = 740
G5 = 784

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
LED_PIN = board.D13  # Pin number for the board's built in LED.
LIGHT_SENSE = analogio.AnalogIn(board.A1)   # Light sensor is connected to A1 on Hallowing

# Setup digital output for LED:
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

#----------------------------------------------------
# LIS3DH Sensor
#----------------------------------------------------
SENSITIVITY = 5   # reading in Z direction to trigger, adjustable

# Set up accelerometer on I2C bus, 4G range:
I2C = busio.I2C(board.SCL, board.SDA)

ACCEL = adafruit_lis3dh.LIS3DH_I2C(I2C, address=0x18)

ACCEL.range = adafruit_lis3dh.RANGE_4_G

#i = random.randint(0, (len(images)-1))  # initial image is randomly selected

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

def play_tone(freq,vol,note_length):
    tone_volume = vol  # Increase this to increase the volume of the tone.
    frequency_hz = freq  # Set this to the Hz of the tone you want to generate.
    length = 8000 // frequency_hz
    sine_wave = array.array("H", [0] * length)
    for i in range(length):
        sine_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))
    sine_wave_sample = audioio.RawSample(sine_wave)
    audio.play(sine_wave_sample,loop=True)
    time.sleep(note_length)
    audio.stop()

def beep(count):
    for _ in range(count):
        audio.play(sine_wave_sample, loop=True)
        time.sleep(0.1)
        audio.stop()
        time.sleep(0.05)

def play_song(song_number,vol):
    """
    if song_number == 1:
        # jingle bells
        jingle_bells_song = [
            [E4, vol, quarter_note],
            [E4, vol, quarter_note],
            [E4, vol, half_note],
            [E4, vol, quarter_note],
            [E4, vol, quarter_note],
            [E4, vol, half_note],
            [E4, vol, quarter_note],
            [G4, vol, quarter_note],
            [C4, vol, dotted_quarter_note],
            [D4, vol, eighth_note],
            [E4, vol, whole_note],
        ]
        for i in jingle_bells_song:
            play_tone(i[0],i[1],i[2])
    """
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
            time.sleep(0.005)  # default (0.005)

# Function for writing text to the screen
"""
def draw_text(txt,x_pos,y_pos,txt_scale):
  ta = label.Label(terminalio.FONT, text=txt)
  ta.scale=txt_scale
  ta.x=x_pos
  ta.y=y_pos
  board.DISPLAY.show(ta)
  board.DISPLAY.wait_for_frame()
  fade_up(0.005)
  return ta
"""
# Function for displaying images on HalloWing TFT screen
def show_image(filename):
    image_file = open(filename, "rb")
    odb = displayio.OnDiskBitmap(image_file)
    face = displayio.TileGrid(odb, pixel_shader=displayio.ColorConverter(), x=0,y=0)
    splash.append(face)
    # Wait for the image to load.
    board.DISPLAY.wait_for_frame()
    fade_up(fade_timer)

#------------------------------------------------------------------------------------
init()
show_image(images_db[3])
play_wav(STARTUP_WAV)
fade_down(fade_timer)
splash.pop()
show_image(images_db[4])  # waiting display
#play_tone(G4,1,whole_note)
play_song(2,0.3)
time.sleep(1)
fade_down(fade_timer)
splash.pop()
show_image(images_db[1])  # waiting display
loop1 = True
while loop1:
    if forward_button.value:
        print("Button touched!")
        loop1 = False
fade_down(0.05)
splash.pop()
show_image(images_db[0])
if LIGHT_SENSE.value < 10000 :
    print("Current light value is:",LIGHT_SENSE.value)
    print("There is not enough light")
else:
    print("Current light value is:",LIGHT_SENSE.value)
    print("There enough light!")

"""
while True:
    shaken = False
    with open(images[i], "rb") as f:
        print("Image load {}".format(images[i]))
        try:
            odb = displayio.OnDiskBitmap(f)
        except ValueError:
            print("Image unsupported {}".format(images[i]))
            del images[i]
            continue
        face = displayio.TileGrid(odb, pixel_shader=displayio.ColorConverter(),
                                x=0,y=0)
        splash.append(face)
        # Wait for the image to load.
        board.DISPLAY.wait_for_frame()

        # Fade up the backlight
        fade_up(0.05)
        # Wait forever
        while not shaken:
            try:
                ACCEL_Z = ACCEL.acceleration[2]  # Read Z axis acceleration
            except IOError:
                pass
            # print(ACCEL_Z)  # uncomment to see the accelerometer z reading
            if ACCEL_Z > SENSITIVITY:
                shaken = True

        # Fade down the backlight
        fade_down(0.05)

        splash.pop()

        i = random.randint(0, (len(images)-1))  # pick a new random image
        print("shaken")
        faceup = False
        i %= len(images) - 1
"""