""" Contains the Game class. """

import pygame as pg

import constants as ct
from gfx import Graphics
from game_object import GameObject
from circle import Circle
from wall import Wall


class Game:
    """ Main game class. Controls the movement of game objects and handles user
    input. """

    def __init__(self):
        self.gfx: Graphics = None
        self.player: GameObject = None
        self.enemies: pg.sprite.Group = pg.sprite.Group()
        self.walls: pg.sprite.Group = pg.sprite.Group()
        self.level = 0

    def __spawn_mobile(self) -> None:
        """ Spawns mobile game objects: player and enemy. Private method - not
        to be called outside of the class. """

        # create player object with starting position based on current level
        self.player = Circle(
            texture=self.gfx.textures['player'],
            x=ct.LEVELS[self.level]['player_start'][0] * ct.UNIT_SIZE,
            y=ct.LEVELS[self.level]['player_start'][1] * ct.UNIT_SIZE
        )

        # create enemy objects with starting position based on current level
        for path in ct.LEVELS[self.level]['enemy_paths']:
            self.enemies.add(
                Circle(
                    texture=self.gfx.textures['enemy'],
                    x=path[0][0],
                    y=path[0][1]
                )
            )

    def __spawn_walls(self) -> None:
        """ Spawns walls. Private method - not to be called outside of the
        class. """

        # create wall objects based on current level
        for row in ct.LEVELS[self.level]['walls']:
            for col, field in enumerate(row):
                if field:
                    self.walls.add(
                        Wall(
                            texture=self.gfx.textures['wall'],
                            x=col,
                            y=row
                        )
                    )

    def ready(self) -> None:
        """ Initializes the game graphics and loads game object textures. """

        # init gfx
        self.gfx = Graphics()
        self.gfx.init_gfx()

        # load textures
        self.gfx.load_textures()

    def spawn_all(self) -> None:
        """ Spawns all the game objects. """

        self.__spawn_mobile()
        self.__spawn_walls()
