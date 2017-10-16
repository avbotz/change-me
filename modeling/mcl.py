"""
Monte Carlo Localization system
Includes simple Particle class and update steps
"""
from __future__ import division
import random
import numpy as np
import sys
import logging
from common.state import State
from common.angle import Angle
import modeling
import modeling.sim
import mission
import config.modeling
import config.mission
import control.query

PYTHON_VERSION = 2 if sys.version_info[0] < 3 else 3
log = logging.getLogger(__name__)


class Particles(object):
    """ Singleton for holding particle arrays """
    array = np.empty((3, config.modeling.NUM_PARTICLES), dtype='f')
    x = array[0]
    y = array[1]
    probability = array[2]
    yaw = 0.0
    depth = 0.0

def weighted_avg(x,y,prob) :
    x_ = sum(x*prob)/sum(prob)
    y_ = sum(y*prob)/sum(prob)
    return x_, y_, 1

def highest_density(x, y, prob):
    """ 
    Finds the highest density region in a scatter plot  
    used to identfy the current location from the sub
    """
    # Setup sliding windows
    x_min = np.min(x)
    y_min = np.min(y)
    x_max = np.max(x)
    y_max = np.max(y)

    """
    First, run an initial sliding classifier. Then, sweep through the grid, cutting down on sample size 
    by half each time. Start with horizontal iterations, then vertical.
    """

    # TODO: Implement dp solution for overlapping regions
    # TODO: Have a smarter way to narrow down on point instead of hard-coding

    # Get starting bounds for initial sliding classifier
    start_arr_x = np.linspace(x_min, x_max * (config.modeling.NUM_SPLIT_INITIAL - 1) /
                              config.modeling.NUM_SPLIT_INITIAL, config.modeling.NUM_SPLIT_INITIAL)
    start_arr_y = np.linspace(y_min, y_max * (config.modeling.NUM_SPLIT_INITIAL - 1) /
                              config.modeling.NUM_SPLIT_INITIAL, config.modeling.NUM_SPLIT_INITIAL)

    # Iterate through starts
    dist_x = (x_max - x_min) / config.modeling.NUM_SPLIT_INITIAL
    dist_y = (y_max - y_min) / config.modeling.NUM_SPLIT_INITIAL
    max_sum = -np.Inf
    for start_x in start_arr_x:
        for start_y in start_arr_y:

            # Get grid from mask
            mask = (x > start_x) & (x < start_x + dist_x) & (y > start_y) & (y < start_y + dist_y)
            grid = prob[mask]

            # Get sum from grid and change bounds if greater
            grid_sum = np.sum(grid)
            if grid_sum > max_sum:
                max_sum = grid_sum
                x_min = start_x
                x_max = x_min + dist_x
                y_min = start_y
                y_max = y_min + dist_y

    # Run through horizontally, cut down by half each time
    for i in range(0, config.modeling.NUM_ITER):

        # Get the starting bounds
        start_arr = np.linspace(x_min, x_min + (x_max - x_min) / 2, config.modeling.NUM_SPLIT)
        dist = (x_max - x_min) / 2
        totals = list()

        # Go through starts, find sum of probabilities in projected area
        for start in start_arr:
            mask = (x > start) & (x < start + dist) & (y > y_min) & (y < y_max)
            grid = prob[mask]
            totals.append(np.sum(grid))

        # Set new min and max bounds for x
        idx = np.argmax(totals)
        x_min = start_arr[idx]
        x_max = x_min + dist

    # Run through vertically, cut down by half each time
    for i in range(0, config.modeling.NUM_ITER):

        # Get the starting bounds
        start_arr = np.linspace(y_min, y_min + (y_max - y_min) / 2, config.modeling.NUM_SPLIT)
        dist = (y_max - y_min) / 2
        totals = list()

        # Go through starts, find sum of probabilities in projected area
        for start in start_arr:
            mask = (y > start) & (y < start + dist) & (x > x_min) & (x < x_max)
            grid = prob[mask]
            totals.append(np.sum(grid))

        # Set new min and max bounds for x
        idx = np.argmax(totals)
        y_min = start_arr[idx]
        y_max = y_min + dist

# Get confidence for density
    fin_mask = (x > x_min) & (x < x_max) & (y > y_min) & (y < y_max)
    fin_grid = prob[mask]
    fin_size = fin_grid.shape[0]
    fin_sum = np.sum(fin_grid)
    confidence = fin_sum / fin_size

    # Calculate x and y
    x_avg = (x_max + x_min) / 2
    y_avg = (y_max + y_min) / 2
    return x_avg, y_avg, confidence


def reset():
    """ Generates a starting grid with a certain number at the starting position """
    Particles.x = np.concatenate(((np.random.random(config.modeling.NUM_PARTICLES - config.modeling.NUM_START_PARTICLES) *
                                   config.modeling.GRID_SIZE[0] - config.modeling.MARGIN_X),
                                  (np.random.random(config.modeling.NUM_START_PARTICLES) *
                                   config.modeling.START_GRID[0])))
    Particles.y = np.concatenate(((np.random.random(config.modeling.NUM_PARTICLES - config.modeling.NUM_START_PARTICLES) *
                                   config.modeling.GRID_SIZE[1] - config.modeling.MARGIN_Y),
                                 (np.random.random(config.modeling.NUM_START_PARTICLES) *
                                  config.modeling.START_GRID[1])))
    Particles.probability = np.zeros(Particles.x.shape, dtype=np.float32)
    np.random.shuffle(Particles.array.T)


def motor_update():
    """ Update each particle with the relative motor move """
    control_state = control.query.get_state()
    relative_position = control_state - modeling.current_state
    Particles.x += relative_position.x
    Particles.y += relative_position.y

    # The yaw from control is required to figure out vision stuff
    # The yaw from control is accurate enough to accept as ground truth
    # ditto for depth
    Particles.yaw = control_state.yaw
    Particles.depth = control_state.depth


def sensor_update():
    """ Updates each particle with the probability that it is true """
    control.query.update_observations()
    for name in mission.goal.goals:
        goal = mission.goal.goals[name]
        if len(goal.recent_observations) <= 0:
            continue
        current_obs = goal.recent_observations[0]
        goal_state = goal.desired_state

        # Adds the percent difference in angle * the confidence to the probability

        if current_obs["confidence"] == 0:
            # If confidence is 0 then no object was found in the image
            continue

        # vision angles are radians from front
        log.debug(Angle(5 * np.pi / 6,Angle.SUB).convert_to(Angle.UNIT).value)
        theta = (Angle(current_obs["z_rotation"] / (2*np.pi), Angle.SUB) + Angle(Particles.yaw , Angle.SUB))
        dot = np.sin(theta.value) * (goal_state.y - Particles.y) + np.cos(theta.value) * (goal_state.x - Particles.x)
        #np.sum(vector_1 * vector_2, 1)
        norm_1 = np.sqrt(np.cos(theta.value)**2+np.sin(theta.value)**2)
        norm_2 = np.sqrt((goal_state.y - Particles.y)**2+(goal_state.x - Particles.x)**2)
        angle = np.arccos(dot / (norm_1 * norm_2))
        angle = 1 - angle/np.pi
        Particles.probability += angle


def resample():
    """ Randomly choose particles proportional to their probability """
    Particles.probability[Particles.probability < .00001] = .00001
    Particles.probability /= sum(Particles.probability)

    random_indices = np.random.choice(Particles.array.shape[1], Particles.array.shape[1] - config.modeling.RANDOM_RESAMPLE, p=Particles.probability, replace=True)
    Particles.x = np.concatenate((np.random.random(config.modeling.RANDOM_RESAMPLE) *
                                 config.modeling.GRID_SIZE[0] - config.modeling.MARGIN_X,
                                  Particles.x[random_indices])) 
    Particles.y = np.concatenate((np.random.random(config.modeling.RANDOM_RESAMPLE) *
                                 config.modeling.GRID_SIZE[0] - config.modeling.MARGIN_Y,
                                 Particles.y[random_indices]))

def choose_current_state():
    Particles.probability[Particles.probability < .0001] = .0001
    stack = np.stack((Particles.x, Particles.y, Particles.probability), 0)
    np.save("data.csv", stack)
    x = np.average(Particles.x, weights=Particles.probability)
    y = np.average(Particles.y, weights=Particles.probability)
    modeling.current_state = State(x, y, Particles.depth, Particles.yaw, 0, 0)
    return
 

num = 0
def update():
    """ Runs all update functions to fully update mcl """
    global num
    if config.modeling.PLOT:
        # Draw the previous state
        modeling.sim.plot_current_state("green", modeling.current_state)
    motor_update()
    sensor_update()
    log.info(modeling.current_state)
    # Send or plot particles if being asked
    if config.modeling.PLOT:
        modeling.sim.show_plot(Particles)
    if config.modeling.VISUALIZE and num % 10 == 0:
        modeling.sim.send_particles(Particles)
    num += 1
    choose_current_state()
    resample()

# Initializes modeling for the first time just to make sure particles exist
reset()
