""" Contains the movement direction ENUM. """

from enum import Enum


class MovementDirection(str, Enum):
    """ The movement direction ENUM. """
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
