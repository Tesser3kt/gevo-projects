""" Contains functions for loading game assets. """

import os
import json
import logging
from pygame import image
from pygame import error as game_error


def load_json_dict(path: str) -> dict:
    """ Reads the JSON-formatted dict stored in 'path'. """

    logging.info('Reading from %s...', path)
    json_dict = None
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
    finally:
        logging.info('Done reading %s', path)

    return json_dict


def load_textures(assets_paths: dict, key: str) -> dict[str,
                                                        list[image.Surface]]:
    """ Loads object textures given its key in assets/paths.json. """

    object_textures = {}

    logging.info('Loading object %s textures...', key)
    for folder, folder_path in assets_paths[key]:
        logging.debug('Loading %s textures...', folder)
        animation_list = []
        try:
            logging.debug('Scanning folder %s...', folder_path)
            for file in os.scandir(folder_path):
                logging.debug('Loading %s as texture...', file.name)
                surface = image.load(file.path)
                logging.debug('Converting surface...')
                frame = surface.convert()
                animation_list.append(frame)
        except game_error as error:
            logging.error('Error loading %s textures. Error: %s', key, error)
            raise SystemExit(f'Error loading {key} textures.') from error
        finally:
            logging.debug('Done loading %s textures.', folder)
            object_textures[folder] = animation_list.copy()
            animation_list = []
    logging.info('Object %s textures loaded.', key)

    return object_textures