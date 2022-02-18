import pygame as pg

""" Graphics module. """


class Graphics:
    """ Graphics class. """

    def __init__(self):
        self.window_size = 640
        self.unit_size = 16
        self.bg_color = 255, 255, 255
        self.window_title = 'PacWoman'
        self.canvas: pg.Surface = None
        self.background: pg.Surface = None

    def init_gfx(self) -> None:
        """ Initialize the graphics. """

        pg.init()
        pg.display.set_caption(self.window_title)
        self.canvas = pg.display.set_mode((self.window_size,
                                           self.window_size), pg.SCALED)
        self.background = pg.Surface(self.canvas.get_size())
        self.background.fill(self.bg_color)
        self.background = self.background.convert()
        self.canvas.blit(self.background, (100, 100))
        pg.display.update()


gfx = Graphics()
gfx.init_gfx()

while True:
    ...
