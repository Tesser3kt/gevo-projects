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

    def move(self, vector: Tuple[int, int], direction: MovementDirection):
        """ Moves the mobile game object by 'vector' in direction
        'direction'. """

        self.animation = self.animation_dict[direction]
        self.rect.move(*vector)

    def collides_with(self, other: GameObject) -> bool:
        """ Checks if the object is colliding with another object. """

        return collide_rect(self, other)

    def collides_with_any_of(self, group: RenderUpdates) -> bool:
        """ Checks if the object is colliding with any of the objects in
        the group. """

        return spritecollideany(self, group) is not None
