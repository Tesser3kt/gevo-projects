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
    def update(self) -> None:
        """ Updates the game state. """
        ...
