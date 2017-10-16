import sys
import subprocess
import argparse
import multiprocessing
import time
import atexit
import logging
import config.control
import config.modeling
import config.mission

parser = argparse.ArgumentParser()
parser.add_argument("-z", "--visualize", help="send particle information over ssh", action="store_true", default=False)
parser.add_argument("-p", "--plot", help="plot particle data", action="store_true", default=False)
parser.add_argument("-v", "--verbose", help="set logging level to DEBUG", action="store_true", default=False)
parser.add_argument("-t", "--test", help="use mock vision and control", action="store_true", default=False)

args = parser.parse_args()

if args.test:
    config.control.ATMEGA_PORT = None
    config.control.VISION_FILE = None

config.modeling.VISUALIZE = args.visualize
config.modeling.PLOT = args.plot

log_out = open("out.log", "a")
logging.basicConfig(stream=log_out if args.visualize else sys.stdout, 
                    level=logging.DEBUG if args.verbose else logging.INFO)
logger = logging.getLogger(__name__)


import control.query
import control.command
import control.connections

atexit.register(control.command.kill)

import mission
import common.state
import modeling.mcl

control.command.set_power(config.mission.POWER)
control.command.set_speed(config.mission.SPEED)

io_check = multiprocessing.Process(target=control.query.killed)
io_check.start()
io_check.join(5)
if io_check.is_alive():
    logger.error("Unable to communicate with atmega at {}!".format(config.control.ATMEGA_PORT))
#    raise IOError("Unable to communicate with atmega at {}!".format(config.control.ATMEGA_PORT))

while True:
    while control.query.killed():
        time.sleep(0.2)
    modeling.mcl.reset()
    for g in config.mission.GOAL_ORDER:
        logger.info("Beginning goal {}.".format(g))
        while not control.query.killed() and not mission.goals[g].complete():
            modeling.mcl.update()
