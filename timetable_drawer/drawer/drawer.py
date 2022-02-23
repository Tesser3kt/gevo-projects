""" Contains the drawer class. """

import logging
import os
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

from auxil.converter import convert_dt_to_hm


class Drawer:
    """ The drawer responsible for drawing grayscale bitmaps. """

    def __init__(self, mode: str, bg_color: str, config: dict, base_dir: str):
        self.base_dir = base_dir
        self.mode = mode
        self.window = config['window']
        self.bg_color = bg_color
        self.img = Image.new(mode=self.mode, size=(
            self.window['width'], self.window['height']),
            color=self.bg_color)
        self.supersampling = config['supersampling']
        self.draw: ImageDraw.ImageDraw = None
        self.fonts: dict[str, ImageFont.ImageFont] = {}
        self.grid_data = config['grid']
        self.cell_margin = config['cell']['margin']
        self.epsilon = config['epsilon']
        self.days = config['days']
        self.lessons = config['lessons']
        self.day_names = config['day_names']
        self.lesson_start = config['lesson_start']
        self.lesson_length = config['lesson_length']

    def init_canvas(self) -> None:
        """ Initializes gfx for drawing on loaded canvas. """

        logging.debug('Initializing ImageDraw...')
        try:
            self.draw = ImageDraw.Draw(self.img)
        except Exception as error:
            logging.error('Error initializing ImageDraw: %s', error)
            raise SystemExit('Error initializing ImageDraw')
        finally:
            logging.debug('Done initializing ImageDraw.')

    def clear_canvas(self) -> None:
        """ Clears the canvas by drawing white rectangle over it. """

        logging.debug('Clearing canvas...')
        self.img = Image.new(mode=self.mode, size=(
            self.window['width'], self.window['height']),
            color=self.bg_color)
        self.draw = ImageDraw.Draw(self.img)
        self.draw.rectangle(
            [0, 0, self.window['width'], self.window['height']],
            outline=None, fill='#FFF', width=0)
        logging.debug('Canvas cleared.')

    def draw_grid(self, color: str, line_width: float) -> None:
        """ Draws a grid with the given grid data. """

        h_step = self.grid_data['height'] / self.grid_data['rows']
        v_step = self.grid_data['width'] / self.grid_data['cols']

        # draw horizontal lines
        logging.debug('Drawing horizontal lines...')
        line_start = self.grid_data['y']
        while line_start <= (self.grid_data['y'] + self.grid_data['height']) *\
                            (1 + self.epsilon):
            self.draw.line([(self.grid_data['x'], line_start),
                            (self.grid_data['x'] + self.grid_data['width'],
                            line_start)],
                           fill=color, width=line_width)
            line_start += h_step
        logging.debug('Done drawing horizontal lines.')

        # draw vertical lines
        logging.debug('Drawing vertical lines...')
        line_start = self.grid_data['x']
        while line_start <= (self.grid_data['x'] + self.grid_data['width']) *\
                            (1 + self.epsilon):
            self.draw.line([(line_start, self.grid_data['y']),
                           (line_start, self.grid_data['y'] +
                           self.grid_data['height'])], fill=color,
                           width=line_width)
            line_start += v_step
        logging.debug('Done drawing vertical lines.')

    def load_font(self, font_name: str, font_path: str,
                  font_size: int) -> None:
        """ Loads font to self.fonts given its name and path. """

        logging.info('Loading font %s from %s', font_name, font_path)
        try:
            path = os.path.join(self.base_dir, 'fonts', font_path)
            self.fonts[font_name] = ImageFont.truetype(path, font_size)
        except Exception as error:
            logging.error('Error loading font %s from %s. Error: %s',
                          font_name, font_path, error)
            raise SystemExit('Error loading font %s from %s.',
                             font_name, font_path)
        finally:
            logging.info('Font %s from %s loaded.', font_name, font_path)

    def write_text(self, **kwargs: dict) -> None:
        """ Writes text on the given coordinates of font_size and color."""

        logging.info('Writing text %s to coordinate %s...', kwargs.get('text'),
                     (kwargs.get('x'), kwargs.get('y')))
        if not kwargs.get('font') in self.fonts:
            logging.error('No font named %s loaded.', kwargs.get('font'))
            return

        if kwargs['multiline']:
            logging.debug('Drawing multiline...')
            self.draw.multiline_text(
                (kwargs['x'], kwargs['y']), text=kwargs['text'],
                font=self.fonts[kwargs['font']], fill=kwargs['color'],
                align='center'
            )
        else:
            logging.debug('Drawing single-line text...')
            self.draw.text(
                (kwargs['x'], kwargs['y']), text=kwargs['text'],
                font=self.fonts[kwargs['font']], fill=kwargs['color']
            )
        logging.info('Done writing text.')

    def write_to_cell(self, row: int, col: int, position: tuple[float, float],
                      text: str, font: str, color: str) -> None:
        """ Writes the to given cell of a drawn grid in 'position'. """

        logging.info('Writing %s to cell %s...', text, (row, col))
        if row > self.grid_data['rows'] or col > self.grid_data['cols']:
            logging.error('Cell %s doesn\'t exist.', (row, col))
            return

        cell_width = self.grid_data['width'] / self.grid_data['cols']
        cell_height = self.grid_data['height'] / self.grid_data['rows']
        cell_x = self.grid_data['x'] + (col - 1) * cell_width
        cell_y = self.grid_data['y'] + (row - 1) * cell_height

        text_args = {
            'x': cell_x + position[0],
            'y': cell_y + position[1],
            'text': text,
            'font': font,
            'color': color,
            'multiline': False
        }
        self.write_text(**text_args)
        logging.info('Text %s written to cell %s.', text, (row, col))

    def _get_cell_dimensions(self) -> tuple[float, float]:
        """ Gets cell (width, height) for a given grid. """

        return (
            self.grid_data['width'] / self.grid_data['cols'],
            self.grid_data['height'] / self.grid_data['rows']
        )

    def _draw_hours_to_grid(self) -> None:
        """ Draws hours to the given grid. """

        logging.info('Drawing hours to grid...')
        cell_width, cell_height = self._get_cell_dimensions()

        for hour in range(self.lessons):
            logging.debug('Drawing hour %s...', hour)

            # calculating width and position of hour number
            text_width, text_height = self.fonts['big_bold'].getsize(str(hour))
            text_x = (cell_width - text_width) / 2
            text_y = cell_height / 2 - text_height - 6

            # writing hour number to cell
            self.write_to_cell(1, hour + 2, (text_x, text_y),
                               str(hour), 'normal', '#000')

            # calculating width and position of hour duration
            lesson_start = datetime.strptime(self.lesson_start[hour], '%H:%M')
            lesson_end = lesson_start + timedelta(minutes=self.lesson_length)
            text = convert_dt_to_hm(lesson_start) + ' - ' +\
                convert_dt_to_hm(lesson_end)
            text_width, text_height = self.fonts['small'].getsize(text)
            text_x = (cell_width - text_width) / 2
            text_y = cell_height / 2 + 6

            # writing hour duration to cell
            self.write_to_cell(1, hour + 2, (text_x, text_y),
                               text, 'small', '#000')
            logging.debug('Done drawing hour %s.', hour)

        logging.info('Done drawing hours.')

    def _draw_days_to_grid(self) -> None:
        """ Writes day names to grid. """

        logging.info('Writing day names to grid...')
        cell_width, cell_height = self._get_cell_dimensions()

        for day in range(self.days):
            logging.debug('Writing day %s to grid...', day)
            # calculating text size and position
            text_width, text_height = self.fonts['big'].getsize(
                self.day_names[day])
            text_x = (cell_width - text_width) / 2
            text_y = (cell_height - text_height) / 2

            # writing day to cell
            self.write_to_cell(day + 2, 1, (text_x, text_y),
                               self.day_names[day], 'big', '#000')
            logging.debug('Day %s written to grid.', day)

        logging.info('Done drawing day names.')

    def draw_title(self, day: int, hour: int, room_name: str,
                   timetable_data: dict) -> None:
        """ Draws the name of the teacher currently occupying the classroom
        above the grid. """

        logging.info('Writing teacher and room name above the timetable.')

        if not timetable_data[day][hour]:
            teacher_name = 'Volno'
        else:
            teacher_name = timetable_data[day][hour]['teacher_long']

        # calculating text width, height and position
        text_width, text_height = self.fonts['title'].getsize(
            f'{room_name} - {teacher_name}')
        text_x = (self.window['width'] - text_width) / 2
        text_y = (self.grid_data['y'] - text_height) / 2

        # writing teacher name above grid
        text_args = {
            'x': text_x,
            'y': text_y,
            'text': f'{room_name} - {teacher_name}',
            'font': 'title',
            'color': '#000',
            'multiline': False
        }
        self.write_text(**text_args)
        logging.info('Done drawing teacher name.')

    def draw_timetable(self, cur_day: int, cur_hour: int,
                       timetable_data: dict) -> None:
        """ Draw the timetable given by timetable_data into the grid
        given by grid_data. """

        logging.info('Writing timetable to grid...')
        self._draw_hours_to_grid()
        self._draw_days_to_grid()

        # calculating cell width and height
        cell_width, cell_height = self._get_cell_dimensions()

        for day_index, day in enumerate(timetable_data):
            for hour_index, hour in enumerate(day):

                # draw white on black rectangle if the (day, hour) should be
                # highlighted
                if day_index == cur_day and hour_index == cur_hour:
                    logging.debug(
                        'Drawing black rect on day %s and hour %s', cur_day,
                        cur_hour)
                    color = '#FFF'
                    self.draw.rectangle([
                        self.grid_data['x'] + cell_width * (hour_index + 1),
                        self.grid_data['y'] + cell_height * (day_index + 1),
                        self.grid_data['x'] + cell_width * (hour_index + 2),
                        self.grid_data['y'] + cell_height * (day_index + 2)
                    ], outline=None, fill='#000', width=0)
                else:
                    color = '#000'

                # skip if no lesson
                if not hour:
                    continue

                logging.debug('Drawing subject %s to cell %s...',
                              hour['subject'], (day_index + 2, hour_index + 2))

                # calculating text width for group
                text_width, text_height = self.fonts['big'].getsize(
                    hour['groups'][0])

                # calculating text position for group (cell center)
                text_x = (cell_width - text_width) / 2
                text_y = (cell_height - text_height) / 2

                self.write_to_cell(day_index + 2, hour_index + 2,
                                   (text_x, text_y), hour['groups'][0],
                                   'big', color)

                # calculating text width and position for class (top left)
                text_width, text_height = self.fonts['normal'].getsize(
                    hour['classes'][0])
                text_x = self.cell_margin['left']
                text_y = self.cell_margin['top']

                self.write_to_cell(day_index + 2, hour_index + 2,
                                   (text_x, text_y), hour['classes'][0],
                                   'normal', color)

                # calculating text width and position for teacher (top right)
                text_width, text_height = self.fonts['normal'].getsize(
                    hour['teacher_short'])
                text_x = cell_width - text_width - self.cell_margin['right']
                text_y = self.cell_margin['top']

                self.write_to_cell(day_index + 2, hour_index + 2,
                                   (text_x, text_y), hour['teacher_short'],
                                   'normal', color)
                logging.debug('Subject written to cell.')
        logging.info('Done writing timetable.')

    def save_image(self, filename: str, format: str) -> None:
        """ Saves image in the given format to filename. """

        logging.info('Saving image %s in format %s', filename, format)
        self.img = self.img.resize(
            (self.window['width'] // self.supersampling,
             self.window['height'] // self.supersampling),
            resample=Image.ANTIALIAS)
        self.img.save(filename, format)
        logging.info('Image saved in %s.', filename)
