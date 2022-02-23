""" Contains the Graphics class. """

import pygame as pg

import constants as ct
from game_object import GameObject


class Graphics:
    """ Game graphics class. Takes care of initializing pygame graphics,
    loading object texture and drawing objects on screen. """

    def __init__(self):
        self.canvas: pg.Surface = None
        self.background: pg.Surface = None
        self.textures: dict[str, pg.Surface] = {}

    def init_gfx(self) -> None:
        """ Initializes game graphics, creates the canvas and background
        surface. """

        # init pygame
        pg.init()

        # create game window and canvas
        self.canvas = pg.display.set_mode(ct.WINDOW_SIZE, pg.SCALED)

        # set window title
        pg.display.set_caption(ct.WINDOW_TITLE)

        # create bg surface
        self.background = pg.Surface(self.canvas.get_size())
        self.background.fill(ct.BG_COLOR)
        self.background = self.background.convert()

        # blit bg to canvas
        self.canvas.blit(self.background, (0, 0))

    def load_textures(self) -> None:
        """ Loads textures of all game object types - player, wall and
        enemy. """

        # load texture for each object name
        for obj in 'player', 'enemy', 'wall':

            # load the object image
            image = pg.image.load(f'{obj}.png')

            # scale it to unit size
            image = pg.transform.scale(image, (ct.UNIT_SIZE, ct.UNIT_SIZE))

            # convert it for faster blitting
            image = image.convert()

            # save to textures
            self.textures[obj] = image

    def draw_group(self, grp: pg.sprite.Group) -> None:
        """ Draws the given group of sprites onto the canvas. """

        grp.draw(self.canvas)

    def draw_bg_over_group(self, grp: pg.sprite.Group) -> None:
        """ Draws the background surface over the part of canvas determined
        by position of sprites in the group. """

        grp.clear(self.canvas, self.background)

    def clear_canvas(self) -> None:
        """ Draws the background surface over the entire canvas. """

        self.canvas.blit(self.background, (0, 0))

    def update_canvas(self, rects_to_update: list[pg.Rect] = None) -> None:
        """ Updates the parts of canvas specified by rects_to_update. """

        if rects_to_update:
            pg.display.update(rects_to_update)
        else:
            pg.display.update()
