""" Contains the Pacman game class. """

import logging
import os
from pygame.sprite import RenderUpdates

from aux import loader
from game.game import Game
from game.game_state import GameState


class Pacman(Game):
    """ The Pacman game class. """

    def __init__(self, state: GameState, base_dir: str):
        """ Initializes the Pacman game and loads defaults from
        defaults.json. """

        super().__init__(state, base_dir)
        self.defaults = loader.load_json_dict(
            os.path.join(base_dir, 'defaults.json'))
        self.paths = loader.load_json_dict(
            os.path.join(base_dir, 'paths.json'))
        self.objects = RenderUpdates()

    def spawn_objects(self) -> None:
        """ Spawns all the objects needed for the game. """

        # load wall textures
        wall_paths = self.paths['walls']
        wall_textures = {
            'outer': loader.load_textures(wall_paths, 'outer'),
            'inner': loader.load_textures(wall_paths, 'inner'),
            'prison': loader.load_textures(wall_paths, 'prison')
        }

    def update(self) -> None:
        ...

    def run(self) -> None:
        """ Runs the game and keeps it running until exit singal is
        received. """

        while True:
            pass
