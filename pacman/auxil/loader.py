""" Contains functions for loading game assets. """

import os
import json
import logging
from pygame import image, transform, Surface
from pygame import error as game_error


def load_json_dict(path: str) -> dict:
    """ Reads the JSON-formatted dict stored in 'path'. """

    logging.info('Reading from %s...', path)
    try:
        with open(path, 'r', encoding='utf-8') as json_file:
            json_string = json_file.read()
            logging.debug('Converting %s to JSON...', path)
            json_dict = json.loads(json_string)
    except IOError as error:
        logging.error('Error reading from %s. Error: %s', path, error)
        raise SystemExit(f'Error reading from {path}.') from error
    except json.JSONDecodeError as error:
        logging.error(
            'Error parsing JSON from %s. Error: %s', path, error)
        raise SystemExit(f'Error parsing JSON from {path}.') from error

    logging.info('Done reading %s.', path)
    return json_dict


def load_textures(assets_dir: str, assets_paths: dict, key: str,
                  image_size: tuple[int, int])\
        -> dict[str, list[Surface]]:
    """ Loads object textures given its key in assets/paths.json. """

    object_textures = {}

    logging.info('Loading object %s textures...', key)

    for folder, folder_path in assets_paths[key].items():
        logging.debug('Loading %s textures...', folder)
        folder_path = os.path.join(assets_dir, *folder_path.split('/'))
        animation_list = []
        try:
            logging.debug('Scanning folder %s...', folder_path)
            # get folder files
            files = os.listdir(folder_path)

            # order them by name
            files = sorted(files)

            # load images
            for file in files:
                file_path = os.path.join(folder_path, file)
                logging.debug('Loading %s as texture...', file_path)
                surface = image.load(file_path)
                surface = transform.scale(surface, image_size)
                logging.debug('Converting surface...')
                frame = surface.convert()
                animation_list.append(frame)
        except game_error as error:
            logging.error('Error loading %s textures. Error: %s', key, error)
            raise SystemExit(f'Error loading {key} textures.') from error

        logging.debug('Done loading %s textures.', folder)
        object_textures[folder] = animation_list.copy()
        animation_list = []

    logging.info('Object %s textures loaded.', key)
    return object_textures
