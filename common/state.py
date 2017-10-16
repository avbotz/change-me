""" State class to represent position of sub """
import numpy as np


class State(object):
    """
    Represents the precise position of the sub
    """

    ROT_EPSILON = (np.pi / 12)  # 15 degrees is close enough
    LIN_EPSILON = .3  # .3 distance units is close enough

    def __init__(self, x, y, depth, yaw, pitch, roll):
        """
        Initializes a state from provided values
        More possible initialization methods should be added
        """
        self.x = x
        self.y = y
        self.depth = depth
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def __str__(self):
        """
        Returns a format suitable for io to control
        for a human-readable format, try __repr__
        """
        return "s {} {} {} {} {} {}".format(self.x, self.y, self.depth,
                                            self.yaw, self.pitch, self.roll)

    def __sub__(self, other):
        """ subtracts two state element-wise """
        # if not isinstance(other, State):
        #    raise ArithmeticError("Cannot subtract State from a non-State object")
        return State(self.x - other.x, self.y - other.y, self.depth - other.depth,
                     self.yaw - other.yaw, self.pitch - other.pitch, self.roll - other.roll)

    def __add__(self, other):
        """ adds two states element-wise """
        # if not isinstance(other, State):
        #    raise ArithmeticError("Cannot add State to a non-State object.")
        return State(self.x + other.x, self.y + other.y, self.depth + other.depth,
                     self.yaw + other.yaw, self.pitch + other.pitch, self.roll + other.roll)

    def distance(self, other):
        """ Returns Euclidian distance to another State """
        diff = self - other
        return (diff.x ** 2 + diff.y ** 2 + diff.depth ** 2) ** .5

    def __eq__(self, other):
        """ determines if two states are 'close enough' to be equal """
        if not isinstance(other, State):
            return False
        return self.distance(other) < State.LIN_EPSILON and abs(self.yaw - other.yaw) < State.ROT_EPSILON

    def angle_to(self, other):
        """
        gives the angle in yaw and pitch
        between this state and another
        IS ONLY BASED on x, y, and depth *NOT* actual sub angle
        for sub angle use __sub__
        RETURNS IN RADIANS
        """
        diff = other - self
        z_rotation = np.arctan2(diff.y, diff.x)
        plane_distance = (diff.x ** 2 + diff.y ** 2) ** .5
        elevation = np.arctan2(diff.depth, plane_distance)
        return z_rotation, elevation

    def xyz(self):
        """ Returns the xyz of the state as a list """
        return [self.x, self.y, self.depth]

    def cross(self, other):
        """
        returns the cross product state of xyz for 2 states
        keeps the angle of the first state
        """
        return State(*np.cross(self.xyz, other.xyz), yaw=self.yaw, pitch=self.pitch, roll=self.roll)

    def __matmul__(self, other):
        """ See cross. matmul is the '@', or matrix mult op in py3 """
        return self.cross(other)

    def __abs__(self):
        """ Returns the norm of the vector """
        return self.distance(State(*([0] * 6)))
