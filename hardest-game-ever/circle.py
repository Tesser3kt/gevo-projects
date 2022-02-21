""" Contains the Circle class. """

import pygame as pg
from typing import Tuple


import constants as ct
from game_object import GameObject


class Circle(GameObject):
    """ Class of the moving objects in the game - player and enemy. """

    def __init__(self, texture: pg.Surface, x: int = 0, y: int = 0,
                 width: int = ct.UNIT_SIZE, height: int = ct.UNIT_SIZE):
        GameObject.__init__(self, texture, x, y, width, height)

    def move(self, *vector: Tuple[int, int]) -> None:
        """ Moves the game obejct by the given vector. """

        self.rect = self.rect.move(*vector)
