"""
Config settings for control package
We can have straight .py config because security isn't an issue
(except with Emil)
If both ports are `None` then the sim will be used instead 
"""
import sys

ATMEGA_PORT = "/dev/ttyUSB2"
VISION_FILE = sys.stdin # "./cpp/pipes/vision"
