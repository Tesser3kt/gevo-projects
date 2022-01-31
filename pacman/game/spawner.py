""" Contains the Spawner base class. """

import logging
from pygame import Surface, Rect
from pygame.sprite import RenderUpdates

from game.game_object import GameObject
from game.mobile_game_object import MobileGameObject
from game.constants import Constants


class Spawner:
    """ Spawner class. Takes care of spawning game objects. """

    def __init__(self, textures: dict[str, dict[str, list[Surface]]],
                 game_defaults: dict, game_objects: RenderUpdates,
                 game_constants: Constants):
        self.textures = textures
        self.objects = game_objects
        self.defaults = game_defaults
        self.constants = game_constants

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

    def __spawn_ghosts(self) -> RenderUpdates:
        """ Spawns ghost objects. """
        ghost_objects = RenderUpdates()

        try:
            for index, type in enumerate(self.defaults['game']['ghost_types']
                                         ['ghost_normal_types']):
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
            logging.error('Ghost spawn positions badly indexed.')
            raise SystemExit('Ghost spawn positions badly indexed.') from error
        except KeyError as key_error:
            logging.error('Ghost textures key error. Error %s', key_error)
            raise SystemExit('Ghost textures key error.') from key_error

        return ghost_objects

    def __spawn_pac(self) -> MobileGameObject:
        try:
            col, row = self.constants.pac_spawn
            pac_object = MobileGameObject(
                animation_dict=self.textures['pac']['pac'],
                rect=Rect(col * self.constants.pixels_per_unit,
                          row * self.constants.pixels_per_unit,
                          self.constants.pixels_per_unit,
                          self.constants.pixels_per_unit),
                type='pac',
                destructible=True)
        except IndexError as error:
            logging.error('Pac spawn badly indexed.')
            raise SystemExit('Pac spawn badly indexed.') from error
        except KeyError as key_error:
            logging.error('Pac textures key error.')
            raise SystemExit('Pac textures key error.') from key_error

        return pac_object

    def spawn_immobile(self) -> None:
        """ Spawns all the static objects in the game. """

        # create groups for walls, coins and door
        walls = RenderUpdates()
        coins = RenderUpdates()

        # cycle through wall and coin types defined in game defaults

        logging.debug('Spawning walls...')
        for type in self.defaults['object']['wall']:
            walls.add(self.__spawn_wall(type))
        logging.debug('Walls spawned.')

        logging.debug('Spawning coins...')
        for type in self.defaults['object']['coin']:
            coins.add(self.__spawn_coins(type))
        logging.debug('Coins spawned.')

        logging.debug('Spawning prison door...')
        prison_door = self.__spawn_prison_door()
        logging.debug('Prison door spawned.')

        # add walls, coins and prison door to objects
        self.objects['walls'] = walls
        self.objects['coins'] = coins
        self.objects['prison_door'] = prison_door

    def spawn_mobile(self) -> None:
        """ Spawns dynamic objects in the game - ghosts and pac. """

        logging.debug('Spawning ghosts...')
        ghost_objects = self.__spawn_ghosts()
        logging.debug('Ghosts spawned.')

        logging.debug('Spawning pac...')
        pac_object = self.__spawn_pac()
        logging.debug('Pac spawned.')

        # add pac and ghosts to game object list
        self.objects['ghosts'] = ghost_objects
        self.objects['pac'] = RenderUpdates(pac_object)
