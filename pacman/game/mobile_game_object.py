""" Contains the mobile game objects abstract class. """

from typing import Tuple
from pygame import Rect, Surface
from pygame.sprite import RenderUpdates, collide_rect, spritecollideany


from game.game_object import GameObject
from game.movement_direction import MovementDirection


class MobileGameObject(GameObject):
    """ The mobile game object abstract base class. """

    def __init__(self, animation_dict: dict[str, list[Surface]], rect: Rect,
                 type: str, destructible: bool):
        super().__init__(animation_dict['up'], rect, type, destructible)
        self.animation_dict = animation_dict
        self.direction = MovementDirection.UP
        self.vector = (0, 0)
        self.moving = False

    def move(self, vector: Tuple[int, int] = None,
             direction: MovementDirection = None):
        """ Moves the mobile game object by 'vector' in direction
        'direction'. """

        if vector and direction:
            self.direction = direction
            self.vector = vector
        self.animation = self.animation_dict[self.direction]
        self.rect = self.rect.move(*self.vector)
