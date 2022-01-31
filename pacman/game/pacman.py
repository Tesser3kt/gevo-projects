""" Contains the Pacman game class. """

import logging
import os
from typing import Tuple

import pygame as pg
from pygame import K_UP, Surface
from pygame.sprite import RenderUpdates
from pygame.event import Event
from pygame.time import Clock

from aux import loader
from game.game import Game
from game.game_state import GameState
from game.constants import Constants
from game.movement_direction import MovementDirection
from game.texture_loader import TextureLoader
from game.spawner import Spawner


class Pacman(Game):
    """ The Pacman game class. """

    def __init__(self, state: GameState, base_dir: str):
        """ Initializes the Pacman game and loads defaults from
        defaults.json. """

        super().__init__(state, base_dir)
        self.assets_dir = os.path.join(self.base_dir, 'assets')
        self.defaults = loader.load_json_dict(
            os.path.join(base_dir, 'defaults.json'))
        self.paths = loader.load_json_dict(
            os.path.join(base_dir, 'paths.json'))
        self.constants = Constants(self.defaults)
        self.objects: dict[str, RenderUpdates] = {}
        self.textures: dict[str, dict[str, list[Surface]]] = None
        self.screen: Surface = None
        self.background: Surface = None
        self.spawner: Spawner = None
        self.clock: Clock = None
        self.level = 0

    def init_gfx(self) -> None:
        # init pygame
        pg.init()

        # init game window
        size = (self.defaults['window']['width'],
                self.defaults['window']['height'])
        self.screen = pg.display.set_mode(size, pg.SCALED)
        self.background = Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(tuple(self.defaults['game']['bg_color']))
        pg.display.flip()

    def __user_quit(self, event: Event) -> bool:
        return event.type == pg.QUIT or (event.type == pg.KEYDOWN and
                                         event.key == pg.K_ESCAPE)

    def __handle_arrow_key_press(self, keys: dict) -> None:
        """ Handles key press. """

        logging.debug('Handling key input...')
        if keys[pg.K_UP]:
            direction = MovementDirection.UP
            vector = (0, -self.defaults['game']['object_speed']['pac'])
            logging.debug('Key UP pressed.')
        elif keys[pg.K_RIGHT]:
            direction = MovementDirection.RIGHT
            vector = (self.defaults['game']['object_speed']['pac'], 0)
            logging.debug('Key RIGHT pressed.')
        elif keys[pg.K_DOWN]:
            direction = MovementDirection.DOWN
            vector = (0, self.defaults['game']['object_speed']['pac'])
            logging.debug('Key DOWN pressed.')
        elif keys[pg.K_LEFT]:
            direction = MovementDirection.LEFT
            vector = (-self.defaults['game']['object_speed']['pac'], 0)
            logging.debug('Key LEFT pressed.')

        logging.debug('Moving pac by %s', vector)
        pac = self.objects['pac'].sprites()[0]
        pac.move(vector, direction)
        self.objects['pac'].update()
        changed_rects = self.objects['pac'].draw(self.screen)
        pg.display.update(changed_rects)

        logging.debug('Key input handled.')

    def load_textures(self) -> None:
        """ Loads game object textures. """

        # graphics must be initalized for texture loading to work
        if not self.screen:
            logging.error(
                'Cannot load textures without initializing graphics.')
            raise SystemExit(
                'Cannot load textures without initializing graphics.')

        # init texture loader
        txtr_loader = TextureLoader(self.assets_dir, self.defaults, self.paths)
        self.textures = txtr_loader.load_all_textures()

    def spawn(self) -> None:
        """ Spawns all the objects in the game. """

        # textures must be loaded before spawning objects
        if not self.textures:
            logging.error(
                'Game textures must be loaded before spawning objects.')
            raise SystemExit(
                'Game textures must be loaded before spawning objects.')

        # init spawner
        self.spawner = Spawner(self.textures, self.defaults,
                               self.objects, self.constants)

        logging.debug('Spawning immobile objects...')
        self.spawner.spawn_immobile()
        logging.debug('Immobile objects spawned.')

        logging.debug('Spawning mobile objects...')
        self.spawner.spawn_mobile()
        logging.debug('Mobile objects spawned.')

    def draw(self) -> None:
        """ Draws all the objects in the game. """

        # objects cannot be drawn without spawning
        if not self.objects:
            logging.error('No objects to draw.')
            raise SystemExit('No objects to draw.')

        for sprite_group in self.objects.values():
            sprite_group.draw(self.screen)
        pg.display.update()

    def update(self) -> None:
        ...

    def run(self) -> None:
        # init game clock (FPS)
        self.clock = Clock()

        running = True
        while running:
            self.clock.tick(self.defaults['game']['max_fps'])
            # get arrow key events
            keys = pg.key.get_pressed()
            if any((keys[pg.K_UP], keys[pg.K_DOWN], keys[pg.K_RIGHT],
                   keys[pg.K_LEFT])):
                self.__handle_arrow_key_press(keys)

            # get other events
            for event in pg.event.get():
                if self.__user_quit(event):
                    logging.debug('Quit event from user. Exiting...')
                    running = False
