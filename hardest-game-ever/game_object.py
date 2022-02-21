""" Contains the GameObject class. """

from abc import ABC
import pygame as pg

import constants as ct


class GameObject(ABC, pg.sprite.Sprite):
    """ Abstract game object class. Inherits from PyGame Sprite - basis class
    for all drawable game objects. """

    def __init__(self, texture: pg.Surface, x: int = 0, y: int = 0,
                 height: int = ct.UNIT_SIZE, width: int = ct.UNIT_SIZE):

        # call the parent class' constructor
        pg.sprite.Sprite.__init__(self)

        # create object's rectangle with the given data
        self.rect = pg.Rect(x, y, width, height)

        # save object's texture
        self.image = texture
