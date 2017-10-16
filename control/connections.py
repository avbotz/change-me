"""
Wrapper for serial so we can do initialization once
Otherwise we would have 2 different serials in query and command
"""
from __future__ import division
import numpy as np
import modeling
import os
import logging
import config.control as conf
from common.angle import Angle
if conf.VISION_FILE == None:
    import mission.goal


logger = logging.getLogger(__name__)


class ATMega(object):
    """ pipes atmega stuff to a file so a human can mock it """
    # pipein = None
    # pipeout = None
    pipe = None

    def __init__(self, port=None):
        if port is not None:
            self.sim = False
            self.pipe = open(port, "rw+")
        else:
            self.sim = True
            self.next_line = ""
            self.state = modeling.State(*([0] * 6))
            self.desired_state = modeling.State(*([0] * 6))

    def write(self, msg):
        if self.sim:
            msg = msg.strip()
            if msg == "a":
                self.next_line = "1\n"
            elif msg == "c":
                diff_state = self.desired_state - self.state
                norm = diff_state.x ** 2 + diff_state.y ** 2
                self.state.x += diff_state.x * 10 / norm
                self.state.y += diff_state.y * 10 / norm
                self.state.yaw = self.desired_state.yaw
                self.next_line = str(self.state) + "\n"
            elif msg[0] == "n":
                x, y = [float(i) for i in msg.split(" ")[1:]]
                self.state.x = x
                self.state.y = y
            elif msg[0] == "s":
                self.desired_state = modeling.State(*[float(i) for i in msg.split(" ")[2:]])
        else:
                try:
                    self.pipe.write(msg)
                    self.pipe.flush()
                except IOError:
                    logger.critical("Could not write to atmega, continuing.")

    def readline(self):
        if self.sim:
            nl = self.next_line
            self.next_line = ""
            if nl == "":
                logger.critical("Sim sending blank string.")
            return nl
        else:
            try:
                st = self.pipe.readline()
                escapes = ''.join([chr(char) for char in range(1, 32)])
                t = st.translate(None, escapes)
            except IOError:
                logger.critical("Could not read from atmega, continuing.")
            return t;


class Vision(object):
    """ pipes atmega stuff to a file so a human can mock it """
    pipe = None

    def __init__(self, port=None):
        if port != None:
            self.sim = False
            self.pipe = port
        else:
            self.sim = True
            self.end = False


    def readline(self):
        if self.sim:
            if self.end:
                self.end = not self.end
                return "\n"
            else:
                self.end = not self.end
                diff_state = mission.goal.goals["red_buoy"].desired_state - modeling.current_state
                angle = Angle(np.arctan2(diff_state.y, diff_state.x), Angle.UNIT).convert().range(-.5, .5)
                angle -= Angle(modeling.current_state.yaw, Angle.SUB)
                elevation = 0
                confidence = 1
                logger.debug(" Simulated Angle {} rotations Elevation {}".format(angle.value * 2 * np.pi, elevation))
                return "red_buoy {} -100 {} -100 1\n".format(angle.value * 2 * np.pi, elevation)
        else:
            return self.pipe.readline()


atmega = None

try:
    atmega = ATMega(conf.ATMEGA_PORT)
except IOError:
    logger.error("Unable to open ATMega.")
    raise

vision = None

try:
    vision = Vision(conf.VISION_FILE)
except IOError:
    logger.error("Unable to open Vision.")
    raise
