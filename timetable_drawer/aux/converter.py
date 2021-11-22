""" Module hosting various auxilliary conversion methods."""

import logging
from datetime import datetime


def convert_dt_to_hm(dt: datetime) -> str:
    """ Converts given datetime object to string 'HOURS:MINUTES'. """

    logging.debug('Converting %s to hours:minutes...', dt)
    try:
        time_string = dt.strftime('%H:%M')
    except Exception as error:
        logging.error('Conversion of %s failed.', dt)
        raise SystemExit(f'Conversion of datetime failed. Error: {error}.')
    finally:
        logging.debug('Conversion successful.')

    return time_string
