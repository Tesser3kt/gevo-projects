import logging
import os
from game.game_state import GameState
from game.pacman import Pacman


def main():
    """ Main function. """

    BASE_DIR = os.getcwd()

    logging.basicConfig(filename='log', filemode='w+',
                        encoding='utf-8', level=logging.DEBUG)
    pacman = Pacman(GameState.INTRO, BASE_DIR)
    pacman.init_gfx()
    pacman.load_all_textures()
    pacman.spawn()
    pacman.draw()
    pacman.run()


if __name__ == '__main__':
    main()
