import logging
import os
from game.game_state import GameState
from game.pacman import Pacman


def main():
    """ Main function. """

    # get CWD
    BASE_DIR = os.getcwd()

    # delete previous log file
    if os.path.exists(os.path.join(BASE_DIR, 'log')):
        os.remove(os.path.join(BASE_DIR, 'log'))

    # init logger
    logging.basicConfig(filename='log', filemode='w+',
                        encoding='utf-8', level=logging.DEBUG)

    # init game objects
    pacman = Pacman(GameState.INTRO, BASE_DIR)
    pacman.init_gfx()
    pacman.load_textures()
    pacman.spawn()
    pacman.draw()

    # run game
    pacman.run()


if __name__ == '__main__':
    main()
