from __future__ import division, print_function
import sys
import config.modeling as conf
if conf.PLOT:
    import matplotlib.pyplot as plt
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
from common.angle import Angle
import numpy as np
import modeling
import config.mission
import mission.goal

def plot_current_state(color="black", state=None):
    if state == None:
        state = modeling.current_state
    yaw_radians = Angle(state.yaw, Angle.SUB).convert().value
    x_off = conf.SUB_LENGTH * np.sin(yaw_radians)
    y_off = conf.SUB_LENGTH * np.cos(yaw_radians)
    print("Plotted current state {}".format(state))
    ax.plot([state.x - x_off , state.x + x_off ],
             [state.y - y_off , state.y + y_off ],
             linewidth=conf.SUB_LENGTH, c=color)
        

def plot_particles(particles):
    ax.scatter(np.concatenate((particles.x, [])),
                np.concatenate((particles.y, [])),
                c=particles.probability, alpha=.1)

def plot_red_buoy(color="red", state=config.mission.RED_BUOY):
    ax.scatter(state.x, state.y, c=color)


def plot_all(particles, buoy=config.mission.RED_BUOY, state=None):
    if state == None:
        state = modeling.current_state
    ax.clear()
    plot_particles(particles)
    plot_current_state(state=state)
    plot_red_buoy(state=buoy)


def show_plot(particles, buoy=config.mission.RED_BUOY, state=None):
    if state == None:
        state = modeling.current_state
    plot_all(particles, buoy, state)
    plt.show()
    plt.pause(.01)


def send_particles(particles, buoy=config.mission.RED_BUOY, state=None):
    if state == None:
        state = modeling.current_state
    sys.stdout.write("FOOFOO\n")
    sys.stdout.write("[")
    for f in np.array(particles.x, dtype=np.float32)[:-1]:
        sys.stdout.write("{0:0.4}, ".format(f))
    sys.stdout.write("{0:0.4}]\n".format(particles.x[-1]))

    sys.stdout.write("[")
    for f in np.array(particles.y, dtype=np.float32)[:-1]:
        sys.stdout.write("{0:0.4}, ".format(f))
    sys.stdout.write("{0:0.4}]\n".format(particles.y[-1]))

    sys.stdout.write("[")
    for f in np.array(particles.probability, dtype=np.float32)[:-1]:
        sys.stdout.write("{0:0.4}, ".format(f))
    sys.stdout.write("{0:0.4}]\n".format(particles.probability[-1]))

    sys.stdout.write(str(np.array((particles.yaw, particles.depth, state.x, state.y, buoy.x, buoy.y), dtype = np.float32).tolist()) + "\n")
    sys.stdout.write("RASPUTIN\n") # Russia's greatest love machine, don't question it
