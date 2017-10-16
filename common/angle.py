import numpy as np


class Angle(object):
    """ 
    Holds a single value or np array of angles 
    Saves information about rotation, position, etc. 
    converts between various formats

    direction: direction of rotation
    value: numerical value
    scale: rotations/radians
    """

    SUB = 0
    UNIT = 1

    def __init__(self, value, type_):
        """ Creates an angle that knows its value, direction, and scale """
        if not isinstance(value, np.ndarray):
            value = np.array(value, dtype=np.float64)
        self.value = value
        self.type_ = type_


    def collapse_one_array(self):
        if self.value.shape == (1,):
            self.value.shape = self.value.reshape(())


    def convert_to(self, type_):
        """ Converts angle to specified type in place, returns self """
        if type_ == self.type_:
            return self
        if type_ == Angle.UNIT:
            self.type_ = Angle.UNIT
            self.value *= 2 * np.pi;
            while (self.value < 0).any():
                while (self.value < 0).any():
                    self.value[self.value < 0] += 2 * np.pi
            while (self.value[self.value < 0] > 2 * np.pi).any():
                self.value[self.value < 0] -= 2 * np.pi
            if (self.value <= (np.pi / 2)).any():
                self.value[self.value <= (np.pi / 2)] = (np.pi / 2) - self.value
            else :
                self.value[self.value > (np.pi / 2)] = 5 * (np.pi/ 2) - self.value
            return self
        else:
            self.type_ = Angle.SUB
            while (self.value < 0).any():
                self.value[self.value < 0] += 2 * np.pi
            while (self.value > 2 * np.pi):
                self.value[self.value > 2 * np.pi] -= 2 * np.pi
            if (self.value <= np.pi / 2).any():
                self.value[self.value <= np.pi / 2] = np.pi/2 - self.value
            if (self.value > np.pi / 2).any() and \
               (self.value <= (3 * np.pi / 2)).any():
                self.value[(self.value > np.pi / 2) & (self.value <= 3 * np.pi / 2)] = self.value - np.pi/2
                self.value[(self.value > np.pi / 2) & (self.value <= 3 * np.pi / 2)] = -self.value
            if (self.value > 3 * np.pi/2).any:
                self.value[self.value > np.pi / 2] = self.value - 3 * np.pi
                self.value = np.pi - self.value;
            self.value /= 2 * np.pi
            return self


    def convert(self):
        """ Convenience function for convert """
        return self.convert_to(Angle.UNIT if self.type_ == Angle.SUB else Angle.SUB)


    def range(self, low, high):
        """ puts all angle values within given range in place """
        lt = self.value < low
        gt = self.value > high
        while lt.any():
            self.value[lt] += 2 * np.pi if self.type_ == Angle.UNIT else 1
            lt = self.value < low
        while gt.any():
            try:
                self.value[gt] -= 2 * np.pi if self.type_ == Angle.UNIT else 1
            except:
                self.value -= (2 * np.pi) if self.type_ == Angle.UNIT else 1
            gt = self.value > high
        self.collapse_one_array()
        return self



    def __add__(self, other):
        if self.type_ != other.type_:
            raise ValueError("Attempted to add 2 angles of different types.")
        return Angle(self.value + other.value, self.type_)


    def __sub__(self, other):
        if self.type_ != other.type_:
            raise ValueError("Attempted to add 2 angles of different types.")
        return Angle(self.value - other.value, self.type_)


    def __str__(self):
        return "{} angle {}".format("sub" if self.type_ == Angle.SUB else "unit", self.value)
