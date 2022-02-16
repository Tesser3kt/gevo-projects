""" Contains the Pacman game class. """

import logging
import os
from typing import List, Sequence, Tuple

import pygame as pg
from pygame import Surface, Rect
from pygame.sprite import RenderUpdates, groupcollide, spritecollideany
from pygame.event import Event
from pygame.time import Clock

from aux import loader
from game.game import Game
from game.game_state import GameState
from game.constants import Constants
from game.mobile_game_object import MobileGameObject
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
        """ Handles arrow key press. """

        logging.debug('Handling arrow key input...')
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

        self.__move_object('pac', vector, direction=direction)
        logging.debug('Arrow key input handled.')

    def __handle_key_press(self, keys: Sequence[bool]) -> None:
        """ Handles key-pressed events. """

        logging.debug('Handling key press...')
        if any((keys[pg.K_UP], keys[pg.K_DOWN], keys[pg.K_RIGHT],
                keys[pg.K_LEFT])):
            logging.debug('Arrow key pressed.')
            self.__handle_arrow_key_press(keys)

        logging.debug('Key press handled.')

    def __object_collides_with_solid(self, object: MobileGameObject) -> bool:
        """ Simple test if a given object collides with walls or door. """

        return spritecollideany(object, self.objects['walls']) or\
            spritecollideany(object, self.objects['prison_door'])

    def __move_object(self, object_type: str, vector: Tuple[int, int],
                      direction: MovementDirection) -> None:
        logging.debug('Moving object %s by %s...', object_type, vector)

        # get MobileGameObject based on object_type
        if object_type == 'pac':
            try:
                object = self.objects['pac'].sprites()[0]
            except IndexError:
                logging.error('Pac not initialized. Cannot move.')
        else:
            object = [obj for obj in self.objects['ghosts']
                      if object_type == obj.type]
            if len(object) != 1:
                logging.error(
                    'Error moving %s. No such object initialized. ',
                    object_type)
                return
            object = object[0]

        if object.moving:
            return

            # calculated position change
        vector = (vector[0] * self.defaults['game']['pixels_per_unit'],
                  vector[1] * self.defaults['game']['pixels_per_unit'])

        # move object by specified vector
        obj_prev_direction = object.direction
        object.move(vector, direction=direction)

        # if object collides with solid, move it back
        if self.__object_collides_with_solid(object):
            vector = (-vector[0], -vector[1])
            object.move(vector, direction=obj_prev_direction)

        logging.debug('Object %s moved by %s.', object_type, vector)

    def __update_moving_objects(self) -> List[Rect]:
        """ Updates moving objects after their position has changed."""

        logging.debug(
            'Updating moving objects position and drawing changes...')

        changed_rects = []
        game_unit_size = self.defaults['game']['pixels_per_unit']
        for moving_object_grp in ['pac', 'ghosts']:
            # keep moving until whole game units are reached
            for object in self.objects[moving_object_grp].sprites():
                if object.moving:
                    if object.rect.x % game_unit_size or\
                            object.rect.y % game_unit_size:
                        object.move()
                    else:
                        object.moving = False

                        # draw changes
            self.objects[moving_object_grp].clear(self.screen, self.background)
            self.objects[moving_object_grp].update()
            changed_rects += self.objects[moving_object_grp].draw(self.screen)

        logging.debug('Finished updating moving objects.')
        return changed_rects

    def load_textures(self) -> None:
        """ Loads game object textures. """

        # graphics must be initialized for texture loading to work
        if not self.screen:
            logging.error(
                'Cannot load textures without initializing graphics.')
            raise SystemExit(
                'Cannot load textures without initializing graphics.')

        # init texture loader
        txtr_loader = TextureLoader(self.assets_dir, self.defaults, self.paths)
        self.textures = txtr_loader.load_all_textures()

    def spawn_default(self) -> None:
        """ Spawns all the initial objects in the game. """

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
        # objects cannot be drawn without spawning
        if not self.objects:
            logging.error('No objects to draw.')
            raise SystemExit('No objects to draw.')

        for sprite_group in self.objects.values():
            sprite_group.draw(self.screen)
        pg.display.update()

    def update(self) -> None:
        changed_rects = self.__update_moving_objects()
        pg.display.update(changed_rects)

        # TODO allow movement only on whole units

    def run(self) -> None:
        # init game clock (FPS)
        self.clock = Clock()

        running = True
        while running:
            # start game clock
            self.clock.tick(self.defaults['game']['max_fps'])

            # handle key events
            self.__handle_key_press(pg.key.get_pressed())

            # get other events
            for event in pg.event.get():
                if self.__user_quit(event):
                    logging.debug('Quit event from user. Exiting...')
                    running = False

            self.update()
