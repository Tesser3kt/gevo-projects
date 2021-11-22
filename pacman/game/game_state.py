""" Contains the ENUM with game states. """

from enum import Enum, auto


class GameState(Enum):
    """ Defines the ENUM for game states. """
    INTRO = auto()
    RUNNING = auto()
    ENERGIZED = auto()
    PAUSED = auto()
    OVER = auto()
