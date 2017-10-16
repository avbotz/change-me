""" Queries information from the atmega """
from __future__ import division
import logging
import numpy as np
import mission.goal
from control.connections import atmega, vision
import config.control as conf
from common.state import State


logger = logging.getLogger(__name__) 

def killed():
    """ Get the status of the kill switch """
    atmega.write("a\n")
    k = atmega.readline().strip()
    try:
        k = int(k)
    except:
        logger.critical("Recieved {} instead of an 1 or 0 from atmega, continuing".format(k))
        return True
    return True if k == 0 else False


def get_state():
    """ Requests and returns the state from the atmega """
    atmega.write("c\n")
    # get the line, strip the newline char, split it
    arr = atmega.readline().strip().split(" ")
    if arr[0] != "s":
        logger.error("Expected reply starting with 's' from control when asked"
                     " for state, got {}".format(arr[0]))
        return State(*([0] * 6))
    # exclude the first 's' char
    arr = [float(i) for i in arr[1:]]
    return State(*arr)


def update_observations():
    """ Updates all goal observations """
    line = vision.readline()
    while line != "\n":
        ssv = line.strip().split(" ")
        obs = {}
        obs["z_rotation"] = float(ssv[1])
        obs["radius_distance"] = float(ssv[2])
        obs["elevation"] = float(ssv[3])
        obs["distance"] = float(ssv[4])
        obs["confidence"] = float(ssv[5]) 
        mission.goal.goals[ssv[0]].add_observation(obs)
        logger.info("Updated {} observation: {}".format(ssv[0], obs))
        line = vision.readline()
