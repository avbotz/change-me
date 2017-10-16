""" Commands that instruct the atmega """
from __future__ import division
import math
import logging
import config.mission
from control.connections import atmega
from common.angle import Angle
import modeling
import numpy as np

logger = logging.getLogger(__name__)


def set_state(state):
    """ Sends desired state to control """
    logger.info("Set desired state to {}".format(state))
    if modeling.current_confidence > 0.5:
        atmega.write("n {} {}\n".format(modeling.current_state.x, modeling.current_state.y))
        set_speed(.1)
        set_power(.3)
    else:
        set_speed(config.mission.SPEED)
        set_speed(config.mission.POWER)
    atmega.write("s {}\n".format(state))
    return state


def stop():
    """ Set the desired state to the current state """
    return set_state(modeling.current_state)


def move(state):
    """
    Move to a state from the current one
    It is different from set_state because it also sets the correct angle to travel at
    """
    # We need to get the angle diff but also not modify state
    diff = state - modeling.current_state
    # FIXME might have x and y reversed
    yaw = Angle(np.arctan2(diff.x, diff.y), Angle.UNIT).convert().range(-.5, .5)

    logger.debug("Diff X {} Y Diff {} Yaw {}".format(diff.x, diff.y, yaw))

    # if abs((yaw - Angle(modeling.current_state.yaw, Angle.SUB)).value) <= .2:
    #     return set_state(modeling.State(modeling.current_state.x, modeling.current_state.y, state.depth, yaw.value, 0, 0))
    # else:
    return set_state(modeling.State(state.x, state.y, state.depth, yaw.value, 0, 0))


def move_relative(state):
    """
    Move to a state relative to the current one
    It is different from set_state because it also sets the correct angle to travel at
    """
    # We need to get the angle diff but also not modify state
    yaw = math.atan2(state.y, state.x) / (2 * math.pi)
    state = modeling.current_state + state
    return set_state(modeling.State(state.x, state.y, state.depth, yaw, 0, 0))


def move_forward(distance=2):
    """ Moves the sub forwards of its current position at its current yaw """
    x = distance * (np.cos(modeling.current_state.yaw * 2 * math.pi) ** 2)
    y = distance * (np.sin(modeling.current_state.yaw * 2 * math.pi) ** 2)
    move_relative(modeling.State(x, y, 0, 0, 0, 0))



def drop():
    """ Activates dropper """
    return atmega.write("r 3\n")


def set_power(val):
    """ Sets the motor power """
    return atmega.write("p {}\n".format(val))


def kill():
    """ Sets the motor power to 0 """
    return atmega.write("p 0\n")
    return atmega.write("o 0\n")


def set_speed(val):
    """ sets speed of sub, I don't know if we use this """
    return atmega.write("o {}\n".format(val))


def set_level(leveldir, offset):
    """
    Set level, idk if we use this
    Returns the final level and offset
    """
    atmega.write("l {} {}\n".format(leveldir, offset))
    offset = atmega.readline().strip().split(" ")
    if offset[0] != "ll":
        logger.error("Expected 'll' as response to 'l' command, got {}".format(offset[0]))
    return int(offset[0]), float(offset[1])


def set_config(index, val):
    """ Set a desired config value on the arduino """
    return atmega.write("e {} {}\n".format(index, val))


def activate_relay(index):
    """ Activates the relay at the specified index """
    return atmega.write("r {}\n".format(index))


def untilt():
    """ Sets pitch and roll to 0 to level out the sub """
    return atmega.write("u\n")
