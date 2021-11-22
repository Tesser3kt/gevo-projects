""" Contains the movement direction ENUM. """

from enum import Enum, auto


class MovementDirection(str, Enum):
    """ The movement direction ENUM. """
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
