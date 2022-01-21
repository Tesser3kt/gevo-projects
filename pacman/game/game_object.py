""" Contains the abstract base class for game objects. """

from pygame import Rect, Surface
from pygame.sprite import Sprite


class GameObject(Sprite):
    """ The game object base class. """

    def __init__(self, animation: list[Surface], rect: Rect,
                 type: str, destructible: bool):
        super().__init__()
        self.animation = animation
        self.animation_frame = 0
        self.rect = rect
        self.image = self.animation[self.animation_frame]
        self.type = type
        self.destructible = destructible

    def update(self) -> None:
        """ Updates the game object. """
        self.animation_frame = (self.animation_frame +
                                1) % len(self.animation)
        self.image = self.animation[self.animation_frame]
