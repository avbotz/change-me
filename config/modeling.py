""" Config options for mcl and sim in modeling """
import sys
import os

""" MCL """
NUM_PARTICLES = 10000
GRID_SIZE = (50, 50)
START_GRID = (.1, .1)
GRID_DENSITY_SIZE = 1
MARGIN_X = GRID_SIZE[0] * 0.2
MARGIN_Y = GRID_SIZE[1] * 0.2

# Number of particles started in the beginning of the grid
# depth and lateral motion aren't the same but should be linearly correlated
DEPTH_LATERAL_SCALE = 1

NUM_START_PARTICLES = 500
RANDOM_RESAMPLE = 1000

# Density algorithm constants
NUM_SPLIT_INITIAL = 30
NUM_SPLIT = 6
NUM_TILES = 10
NUM_ITER = 10

""" Sim """
SUB_LENGTH = 3
PLOT = False
# Does not send if None
VISUALIZE = False
