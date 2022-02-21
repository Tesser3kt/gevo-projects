""" Contains the Wall class. """

import pygame as pg

import constants as ct
from game_object import GameObject


class Wall(GameObject):
    """ Base class for immobile objects in the game - walls. """

    def __init__(self, texture: pg.Surface, x: int = 0, y: int = 0,
                 height: int = ct.UNIT_SIZE, width: int = ct.UNIT_SIZE):
        GameObject.__init__(self, texture, x, y, height, width)
