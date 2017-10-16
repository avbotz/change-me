""" Locations for goal objects and order of goals """
import numpy as np
import logging
from common.state import State

logger = logging.getLogger(__name__)

logger.critical("TODO Set up competition map.")
RED_BUOY = State(10, 0, -.1, 0, 0, 0)
PVC = State(3, 3, 8, 0, 0, 0)
UNCOVERED_BIN = State(3, 3, 2, 0, 0, 0)
OCTAGON = State(12, 3, 4, 0, 0, 0)
POWER = .5 #.3
SPEED = .22 # .2

# Order to accomplish tasks in
GOAL_ORDER = ["red_buoy", "pvc", "uncovered_bin", "octagon"]
