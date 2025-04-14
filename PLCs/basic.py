from flask import Flask, request, jsonify
from gpiozero import Button
from rpi_ws281x import PixelStrip, Color
import threading
import time
import json
from enum import Enum

class ScreenColor(Enum):
    FIELD_SAFE = Color(0, 255, 0)  # Green
    FIELD_ACTIVE_RED = Color(255, 0, 0)  # Red
    FIELD_ACTIVE_BLUE = Color(0, 0, 255)  # Blue
    ESTOP_ACTIVE = Color(255, 165, 0)  # Orange
    ASTOP_ACTIVE = Color(255, 0, 255)  # Magenta
    ALL_OFF = Color(0, 0, 0)  # Off


with open('settings.json') as f:
    settings = json.load(f)

ESTOP_1_PIN = settings['estop_pin'][0]
ESTOP_2_PIN = settings['estop_pin'][1]
ESTOP_3_PIN = settings['estop_pin'][2]

ASTOP_1_PIN = settings['astop_pin'][0]
ASTOP_2_PIN = settings['astop_pin'][1]
ASTOP_3_PIN = settings['astop_pin'][2]

LED_1_PIN = settings['led_pin'][0]
LED_2_PIN = settings['led_pin'][1]
LED_3_PIN = settings['led_pin'][2]

LED_COUNT = 256
LED_BRIGHTNESS = 255

app = Flask(__name__)

estop_1 = Button(ESTOP_1_PIN, pull_down=True)
estop_2 = Button(ESTOP_2_PIN, pull_down=True)
estop_3 = Button(ESTOP_3_PIN, pull_down=True)
astop_1 = Button(ASTOP_1_PIN, pull_down=True)
astop_2 = Button(ASTOP_2_PIN, pull_down=True)
astop_3 = Button(ASTOP_3_PIN, pull_down=True)

status = {
    "estop" : [False, False, False],
    "astop" : [False, False, False],
    "field_active" : False,
    "field_safe" : False,
    "field_color" : ScreenColor.ALL_OFF,
    "color" : "RED"
}

screens = [
    PixelStrip(LED_COUNT, LED_1_PIN, brightness=LED_BRIGHTNESS),
    PixelStrip(LED_COUNT, LED_2_PIN, brightness=LED_BRIGHTNESS),
    PixelStrip(LED_COUNT, LED_3_PIN, brightness=LED_BRIGHTNESS)
]

for screen in screens:
    screen.begin()

def update_buttons():
    while True:
        status ["estop"][0] = estop_1.is_pressed
        status ["estop"][1] = estop_2.is_pressed
        status ["estop"][2] = estop_3.is_pressed

        status ["astop"][0] = astop_1.is_pressed
        status ["astop"][1] = astop_2.is_pressed
        status ["astop"][2] = astop_3.is_pressed
        
        time.sleep(0.05)