""" Contains the textrue loader class. """

import logging
from pygame import Surface

from aux import loader


class TextureLoader:
    """ Takes care of loading game object textures. """

    def __init__(self, assets_dir: str, defaults: dict, paths: dict):
        self.assets_dir = assets_dir
        self.game_defaults = defaults
        self.txtr_paths = paths

    def __load_object_textures(self, obj: str, types: list[str])\
            -> dict[str, dict[str, list[Surface]]]:
        """ Loads and stores the wall textures. """

        logging.debug('Loading %s textures...', obj)
        try:
            object_paths = self.txtr_paths[obj]
            object_textures = {}
            image_size = (self.game_defaults['game']['pixels_per_unit'],
                          self.game_defaults['game']['pixels_per_unit'])
            for type in types:
                # mobile objects have dictionaries with animations for every
                # movement direction
                if isinstance(object_paths[type], dict):
                    object_textures[type] = loader.load_textures(
                        self.assets_dir, object_paths, type, image_size)
                else:  # immobile objects only have one frame
                    object_textures = loader.load_textures(
                        self.assets_dir, self.txtr_paths, obj, image_size)
                    break
        except KeyError as error:
            logging.error('Object %s textures not found.', obj)
            raise SystemExit(f'Object {obj} textures not found.') from error

        logging.debug('%s textures loaded.', obj.capitalize())
        return object_textures

    def load_all_textures(self) -> dict[str, dict[str, list[Surface]]]:
        """ Loads textures for all the objects in the game. """

        textures: dict[str, dict[str, list[Surface]]] = {}
        logging.debug('Loading all textures...')
        for obj, types in self.game_defaults['object'].items():
            textures[obj] = self.__load_object_textures(obj, types)

        logging.debug('All textures loaded.')
        return textures
