"""
Wrapper so that various things can be imported from
just 'modeling' rather than 'modeling.abc'
"""
from common.state import State

""" Represents the current position of the sub """
current_state = State(0, 0, 0, 0, 0, 0)
current_confidence = 0
