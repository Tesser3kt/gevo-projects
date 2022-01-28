""" Contains the Pacman game class. """

import logging
import os
import pygame
from pygame import Surface, Rect
from pygame import image
from pygame.sprite import RenderUpdates

from aux import loader
from game.game import Game
from game.game_object import GameObject
from game.mobile_game_object import MobileGameObject
from game.game_state import GameState
from game.constants import Constants


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
        self.objects = RenderUpdates()
        self.textures: dict[str, dict[str, list[Surface]]] = None
        self.screen: Surface = None
        self.background: Surface = None

    def init_gfx(self) -> None:
        # init pygame
        pygame.init()

        # init game window
        size = (self.defaults['window']['width'],
                self.defaults['window']['height'])
        self.screen = pygame.display.set_mode(size, pygame.SCALED)
        self.background = Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(tuple(self.defaults['game']['bg_color']))
        pygame.display.flip()

    def __load_object_textures(self, obj: str, types: list[str])\
            -> dict[str, dict[str, list[Surface]]]:
        """ Loads and stores the wall textures. """

        logging.debug('Loading %s textures...', obj)
        try:
            object_paths = self.paths[obj]
            object_textures = {}
            image_size = (self.defaults['game']['pixels_per_unit'],
                          self.defaults['game']['pixels_per_unit'])
            for type in types:
                # mobile objects have dictionaries with animations for every
                # movement direction
                if isinstance(object_paths[type], dict):
                    object_textures[type] = loader.load_textures(
                        self.assets_dir, object_paths, type, image_size)
                else:  # immobile objects only have one frame
                    object_textures = loader.load_textures(
                        self.assets_dir, self.paths, obj, image_size)
                    break
        except KeyError as error:
            logging.error('Object %s textures not found.', obj)
            raise SystemExit(f'Object {obj} textures not found.') from error

        logging.debug('%s textures loaded.', obj.capitalize())
        return object_textures

    def load_all_textures(self) -> None:
        """ Loads textures for all the objects in the game. """

        # graphics must be initalized for texture loading to work
        if not self.screen:
            logging.error(
                'Cannot load textures without initializing graphics.')
            raise SystemExit(
                'Cannot load textures without initializing graphics.')

        self.textures = {}
        logging.debug('Loading all textures...')
        for obj, types in self.defaults['object'].items():
            self.textures[obj] = self.__load_object_textures(obj, types)

        logging.debug('All textures loaded.')

    def __get_wall_block_type(self, row: int, col: int,
                              wall_blocks: list) -> str:
        """ Determines the wall block type on position (row, col) in
        wall_blocks. Very ugly function. Needs refactoring. """

        logging.debug(
            'Determining wall block type on position (%s, %s)...', row, col)
        block_type = None
        if 0 < row < self.constants.height_units - 1:
            if 0 < col < self.constants.width_units - 1:
                if not (wall_blocks[row - 1][col] or
                        wall_blocks[row + 1][col] or
                        wall_blocks[row][col + 1]):
                    block_type = 'top'
                elif not (wall_blocks[row - 1][col] or
                          wall_blocks[row + 1][col] or
                          wall_blocks[row][col - 1]):
                    block_type = 'top'
                elif not wall_blocks[row - 1][col]:
                    if not wall_blocks[row][col - 1]:
                        block_type = 'top_left_corner'
                    elif not wall_blocks[row][col + 1]:
                        block_type = 'top_right_corner'
                    else:
                        block_type = 'top'
                elif not wall_blocks[row + 1][col]:
                    if not wall_blocks[row][col - 1]:
                        block_type = 'bottom_left_corner'
                    elif not wall_blocks[row][col + 1]:
                        block_type = 'bottom_right_corner'
                    else:
                        block_type = 'bottom'
                else:
                    if not wall_blocks[row][col - 1]:
                        block_type = 'left'
                    elif not wall_blocks[row][col + 1]:
                        block_type = 'right'
                    # joins and insides of walls are bounded from all sides,
                    # only determined by diagonals
                    else:
                        if not wall_blocks[row - 1][col - 1]:
                            block_type = 'bottom_right_join'
                        elif not wall_blocks[row - 1][col + 1]:
                            block_type = 'bottom_left_join'
                        elif not wall_blocks[row + 1][col - 1]:
                            block_type = 'top_right_join'
                        elif not wall_blocks[row + 1][col + 1]:
                            block_type = 'top_left_join'
                        else:
                            block_type = 'inside'

            # left outer walls
            elif col == 0:
                if not wall_blocks[row - 1][col] and\
                        not wall_blocks[row + 1][col]:
                    block_type = 'bottom'
                elif not wall_blocks[row - 1][col]:
                    block_type = 'top_left_corner'
                elif not wall_blocks[row + 1][col]:
                    block_type = 'bottom_left_corner'
                else:
                    block_type = 'left'
            else:  # right outer walls
                if not wall_blocks[row - 1][col] and\
                        not wall_blocks[row + 1][col]:
                    block_type = 'bottom'
                elif not wall_blocks[row - 1][col]:
                    block_type = 'top_right_corner'
                elif not wall_blocks[row + 1][col]:
                    block_type = 'bottom_right_corner'
                else:
                    block_type = 'right'

        # top outer walls
        elif row == 0:
            if col == 0:
                block_type = 'top_left_corner'
            elif col == self.constants.width_units - 1:
                block_type = 'top_right_corner'
            else:
                block_type = 'top'
        else:  # bottom outer walls
            if col == 0:
                block_type = 'bottom_left_corner'
            elif col == self.constants.width_units - 1:
                block_type = 'bottom_right_corner'
            else:
                block_type = 'bottom'

        logging.debug('Wall block type determined to be %s.', block_type)
        return block_type

    def __spawn_wall(self, type: str) -> RenderUpdates:
        """ Returns wall objects of type determined by 'type' parameter as
        a group. """

        wall_objects = RenderUpdates()
        # get correct block positions based on 'type'
        if type == 'outer':
            wall_blocks = self.constants.outer_wall
        elif type == 'inner':
            wall_blocks = self.constants.inner_wall
        else:  # type == 'prison'
            wall_blocks = self.constants.prison

        logging.debug('Spawning %s wall...', type)
        try:
            for i, row in enumerate(wall_blocks):
                for j, unit in enumerate(row):
                    # if unit == 1, spawn a block
                    if unit:
                        # determine block type
                        block_type = self.__get_wall_block_type(
                            i, j, wall_blocks)

                        # return game object
                        wall_objects.add(GameObject(
                            animation=self.textures['wall'][type][block_type],
                            rect=Rect(j * self.constants.pixels_per_unit,
                                      i * self.constants.pixels_per_unit,
                                      self.constants.pixels_per_unit,
                                      self.constants.pixels_per_unit),
                            type='wall_{type}_{block_type}',
                            destructible=False))

        except IndexError as error:
            logging.error('%s wall badly indexed. Error: %s',
                          type.capitalize(), error)
            raise SystemExit('%s badly indexed. Exiting...' %
                             type.capitalize()) from error

        logging.debug('Wall %s created.', type)
        return wall_objects

    def __spawn_coins(self, type: str) -> RenderUpdates:
        """ Returns coins of the predetermined type as a group. """

        logging.debug('Spawning coins of type %s', type)
        coin_objects = RenderUpdates()

        # get coin positions based on type
        coin_positions = []
        try:
            if type == 'normal':
                for row in range(self.defaults['game']['height_units']):
                    for col in range(self.defaults['game']['width_units']):
                        if not any((
                                self.constants.outer_wall[row][col],
                                self.constants.inner_wall[row][col],
                                self.constants.prison[row][col],
                                self.constants.prison_inside[row][col],
                                (row, col) in self.constants.prison_door,
                                (row, col) in self.constants.energizers,
                                (row, col) in self.constants.no_coins)):
                            coin_positions.append((row, col))
            else:  # type == 'energizer'
                coin_positions = self.constants.energizers
        except IndexError as error:
            logging.error('Walls or coins badly indexed. Error: %s', error)
            raise SystemExit('Walls or coins badly indexed.') from error

        for row, col in coin_positions:
            coin_objects.add(GameObject(
                animation=self.textures['coin'][type],
                rect=Rect(col * self.constants.pixels_per_unit,
                          row * self.constants.pixels_per_unit,
                          self.constants.pixels_per_unit,
                          self.constants.pixels_per_unit),
                type=f'coin_{type}',
                destructible=True))

        logging.debug('Coins of type %s successfully spawned.', type)
        return coin_objects

    def __spawn_prison_door(self) -> RenderUpdates:
        """ Spawns prison door. """

        logging.debug('Spawning prison door...')

        door_objects = RenderUpdates()
        try:
            for col, row in self.constants.prison_door:
                door_objects.add(GameObject(
                    animation=self.textures['wall']['prison']['door'],
                    rect=Rect(col * self.constants.pixels_per_unit,
                              row * self.constants.pixels_per_unit,
                              self.constants.pixels_per_unit,
                              self.constants.pixels_per_unit),
                    type='prison_door',
                    destructible=True))
        except IndexError as error:
            logging.error('Prison door badly indexed.')
            raise SystemExit('Prison door badly indexed.') from error

        logging.debug('Prison door successfully spawned.')

        return door_objects

    def __spawn_immobile(self) -> None:
        """ Spawns all the static objects in the game. """

        # create groups for walls, coins and door
        walls = RenderUpdates()
        coins = RenderUpdates()

        # cycle through wall and coin types defined in game defaults
        for type in self.defaults['object']['wall']:
            walls.add(self.__spawn_wall(type))

        for type in self.defaults['object']['coin']:
            coins.add(self.__spawn_coins(type))

        prison_door = self.__spawn_prison_door()

        # add walls, coins and prison door to objects
        self.objects.add(walls)
        self.objects.add(coins)
        self.objects.add(prison_door)

    def __spawn_mobile(self) -> None:
        """ Spawns dynamic objects in the game - ghosts and pac. """

        # spawn ghosts
        ghost_objects = RenderUpdates()

        try:
            for index, type in enumerate(self.defaults['game']['ghost_types']['ghost_normal_types']):
                col, row = self.constants.ghost_spawn[index]
                ghost_objects.add(MobileGameObject(
                    animation_dict=self.textures['ghost'][type],
                    rect=Rect(col * self.constants.pixels_per_unit,
                              row * self.constants.pixels_per_unit,
                              self.constants.pixels_per_unit,
                              self.constants.pixels_per_unit),
                    type=type,
                    destructible=False))
        except IndexError as error:
            logging.error('Ghost spawn position badly indexed.')
            raise SystemExit('Ghost spawn position badly indexed.') from error
        except KeyError as key_error:
            logging.error('Ghost textures key error. Error %s', key_error)
            raise SystemExit('Ghost textures key error.') from key_error

        # TODO

    def spawn(self) -> None:
        """ Spawns all the objects in the game. """

        # textures must be loaded before spawning objects
        if not self.textures:
            logging.error(
                'Game textures must be loaded before spawning objects.')
            raise SystemExit(
                'Game textures must be loaded before spawning objects.')

        logging.debug('Spawning immobile objects.')
        self.__spawn_immobile()
        # TODO

    def draw(self) -> None:
        """ Draws all the objects in the game. """

        # objects cannot be drawn without spawning
        if not self.objects.sprites():
            logging.error('No objects to draw.')
            raise SystemExit('No objects to draw.')

        self.objects.draw(self.screen)
        pygame.display.flip()

    def update(self) -> None:
        ...

    def run(self) -> None:
        while True:
            pass
