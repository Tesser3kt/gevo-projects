""" Auxilliary module for loading and converting various filetypes. """
import json
import logging


def load_json_file(path: str) -> dict:
    """ Loads the dictionary from the given file. """

    logging.info('Loading data from %s...', path)
    try:
        file = open(path, 'r', encoding='utf-8-sig')
        data = json.load(file)
        file.close()
    except IOError as error:
        logging.error('Error reading %s. Error: %s', path, error)
        raise SystemExit(f'Error reading {path}.')
    except json.JSONDecodeError as error:
        logging.error('Error parsing %s. Error: %s', path, error)
        raise SystemExit(f'Error parsing {path}.')
    finally:
        logging.info('Data loaded successfully.')

    return data
