import logging
import os
from datetime import datetime as dt
from unidecode import unidecode as ud

from drawer.drawer import Drawer
from aux.loader import load_json_file


def main():
    """ Main function. """

    # init logger
    date = dt.now().strftime('%Y-%m-%d')
    logging.basicConfig(filename=f'logs/log-{date}.txt', encoding='utf-8',
                        format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.DEBUG)
    text = f'Logging started at {dt.now().strftime("%H:%M:%S")}.'
    logging.info(len(text) * '-')
    logging.info(text)
    logging.info(len(text) * '-')

    # load default config
    config = load_json_file('config.json')

    # load timetable for all classrooms
    timetable = load_json_file('timetable.json')

    # initialize gfx and load fonts
    drawer = Drawer('1', config['color']['bg'], config)
    drawer.init_canvas()
    for name, font in config['fonts'].items():
        drawer.load_font(name, f'fonts/{font["family"]}', font['size'])

    # draw timetable for every classroom
    for room_name, room_timetable in timetable.items():

        # create directory for saving classroom images if it doesn't exist
        logging.debug('Getting working directory for %s.', room_name)
        room_ud_name = ud(room_name).lower()
        basedir = os.getcwd()
        imgdir = os.path.join(basedir, room_ud_name)

        if not os.path.exists(imgdir):
            logging.debug(
                'Creating new directory for saving %s timetables.', room_name)
            os.mkdir(imgdir)

        # get current weekday, exit on weekends
        logging.debug('Getting current weekday...')
        weekday = dt.today().weekday()
        if weekday > 4:
            return

        # draw timetable for each hour in the current day and save to
        # the corresponding directory
        logging.debug('Printing grids for every lesson on day %s...', weekday)
        for hour in range(config['lessons']):
            logging.debug('Printing lesson %s...', hour)

            # clear canvas
            drawer.clear_canvas()

            # draw grid
            drawer.draw_grid(config['color']['grid'],
                             config['grid']['line_width'])

            # draw timetable to grid
            drawer.draw_timetable(weekday, hour, room_timetable)

            # draw title
            drawer.draw_title(weekday, hour, room_name, room_timetable)

            # save image
            image_name = f'timetable-{room_ud_name}-{weekday}-{hour}.bmp'
            drawer.save_image(os.path.join(imgdir, image_name), 'bmp')

            logging.debug('Lesson %s printed.', hour)

        logging.debug('Grids for day %s printed.', weekday)


if __name__ == '__main__':
    main()
