""" Contains the abstract base class for game objects. """

from pygame import Rect
from pygame.sprite import Sprite, RenderUpdates
from pygame.image import Surface


class GameObject(Sprite):
    """ The game object abstract base class. """

    def __init__(self, animation: list[Surface], rect: Rect,
                 group: RenderUpdates):
        super().__init__()
        self.animation = animation
        self.animation_frame = 0
        self.rect = rect
        self.group = group
        self.image = self.animation[self.animation_frame]

    def spawn(self) -> None:
        """ Registers and spawns the game object. """
        self.group.add(self)

    def die(self) -> None:
        """ Deregisters and despawns the game object. """
        self.group.remove(self)

    def update(self) -> None:
        """ Updates the game object. """
        self.animation_frame = (self.animation_frame +
                                1) % len(self.animation)
        self.image = self.animation[self.animation_frame]
