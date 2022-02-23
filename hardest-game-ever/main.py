""" Main module. Run this file. """

from game import Game

# init game gfx
game = Game()
game.ready()

# create game objects
game.spawn_all()

# run the game
game.run()
