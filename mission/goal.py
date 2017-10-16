"""
Goal class that is used in mission and modeling and initializes
goals to accomplish
"""
import logging
import control.command
import modeling.mcl
import config.mission
logger = logging.getLogger(__name__)


class Goal(object):
    """
    A goal to be accomplished
    contains the goal's location as a desired state, and the action to do when at that location
    the location should be slightly in front of the actual object
    based on the action that must be performed
    e.g. to ram buoys we should be slightly in front of the buoys

    All positions are relative to gate and need only be rough
    Camera refers into 
    """
    # Number of recent observations to save
    NUM_OBSERVATIONS = 3

    def add_observation(self, observation):
        """ 
        Add an observation and pop the oldest one 
        linear time shouldn't matter because the size shouldn't be much greater than 10
        """
        self.recent_observations.insert(0, observation)
        if len(self.recent_observations) > Goal.NUM_OBSERVATIONS:
            self.recent_observations.pop()

    def __init__(self, desired_state, action, camera, name=""):
        """ Initialize a goal object with desired state, action to run, and name """
        self.name = name
        self.desired_state = desired_state
        self.action = action
        self.recent_observations = []

    def complete(self):
        """
        Moves to the location of the task then performs its action
        returns true when complete
        """
        # move does not actually care about roll/pitch/yaw
        # Also move is non-blocking so we can loop and call this while updating state
        self.desired_state = control.command.move(self.desired_state)
        if self.desired_state == modeling.current_state:
            logger.info("Completing goal {}.".format(self.name))
            self.action()
            return True
        return False


""" dict of pre-initialized goal objects to accomplish """
goals = {
    "red_buoy": Goal(config.mission.RED_BUOY, control.command.move_forward, True, "red_buoy"),
    "pvc": Goal(config.mission.PVC, control.command.move_forward, True, "pvc"),
    "uncovered_bin": Goal(config.mission.UNCOVERED_BIN, control.command.drop, False, "uncovered_bin"),
    # TODO action/goal set is different for hydrophones
    "octagon": Goal(config.mission.OCTAGON,
                    lambda: control.command.move_relative(
                        modeling.State(0, 0, -modeling.current_state.depth, 0, 0, 0)), False,
                    "octagon"),
}
