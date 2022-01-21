""" Contains the abstract game class. """

from abc import ABC, abstractmethod
from pygame.sprite import RenderUpdates

from game.game_state import GameState


class Game(ABC):
    """ Defines the abstract game class. """

    def __init__(self, state: GameState, base_dir: str):
        self.state = state
        self.base_dir = base_dir
        self.objects: RenderUpdates = None
        self.defaults: dict = None

    @abstractmethod
    def init_gfx(self) -> None:
        """ Initializes the game graphics. """
        ...

    @abstractmethod
    def update(self) -> None:
        """ Updates the game state. """
        ...

    @abstractmethod
    def run(self) -> None:
        """ Runs the game and keeps it running until given exit signal. """
        ...
