""" Sleep calculator module. Contains methods for calculating the machine
sleeping time between lessons. """

import logging
import os
from datetime import datetime, timedelta


def get_machine_sleep_times(config: dict, room_dir: str) -> list[int]:
    """ Calculates machine sleep times based on wakeup_time and lesson start
    times. """

    try:
        logging.debug('Getting time info from string %s...',
                      config['wakeup_time'])
        wakeup = datetime.strptime(config['wakeup_time'], '%H:%M')
    except Exception as error:
        logging.error(
            'Error converting string %s to datetime. Error: %s',
            config['wakeup_time'], error)
        raise SystemExit('Error converting to datetime object.')
    finally:
        logging.debug('Done converting string %s to datetime.',
                      config['wakeup_time'])

    if not os.path.exists(room_dir):
        logging.error('Directory %s does not exist.', room_dir)
        raise SystemExit(f'Directory {room_dir} does not exist.')
