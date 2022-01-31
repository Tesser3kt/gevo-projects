""" Contains the Constants class. """


class Constants:
    """ Class for storing game constants. """

    def __init__(self, defaults: dict):
        self.defaults = defaults
        self.width_units = self.defaults['game']['width_units']
        self.height_units = self.defaults['game']['height_units']
        self.pixels_per_unit = self.defaults['game']['pixels_per_unit']
        self.outer_wall = [
            [1] * self.width_units,
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] * 6 + [0] * (self.width_units - 12) + [1] * 6,
            [0] * 5 + [1] + [0] * (self.width_units - 12) + [1] + [0] * 5,
            [0] * 5 + [1] + [0] * (self.width_units - 12) + [1] + [0] * 5,
            [0] * 5 + [1] + [0] * (self.width_units - 12) + [1] + [0] * 5,
            [0] * 5 + [1] + [0] * (self.width_units - 12) + [1] + [0] * 5,
            [1] * 6 + [0] * (self.width_units - 12) + [1] * 6,
            [0] * self.width_units,
            [1] * 6 + [0] * (self.width_units - 12) + [1] * 6,
            [0] * 5 + [1] + [0] * (self.width_units - 12) + [1] + [0] * 5,
            [0] * 5 + [1] + [0] * (self.width_units - 12) + [1] + [0] * 5,
            [0] * 5 + [1] + [0] * (self.width_units - 12) + [1] + [0] * 5,
            [0] * 5 + [1] + [0] * (self.width_units - 12) + [1] + [0] * 5,
            [1] * 6 + [0] * (self.width_units - 12) + [1] * 6,
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] + [0] * (self.width_units - 2) + [1],
            [1] * self.width_units
        ]
        self.no_coins = [(row, col) for row in range(9, 22) for
                         col in range(self.width_units)
                         if col not in [6, self.width_units - 7]] +\
            [(22, 12), (22, 15)]
        self.inner_wall = [
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * 2 + [1] * 4 + [0] + [1] * 5 + [0] + [1] *
            2 + [0] + [1] * 5 + [0] + [1] * 4 + [0] * 2,
            [0] * 2 + [1] * 4 + [0] + [1] * 5 + [0] + [1] *
            2 + [0] + [1] * 5 + [0] + [1] * 4 + [0] * 2,
            [0] * 2 + [1] * 4 + [0] + [1] * 5 + [0] + [1] *
            2 + [0] + [1] * 5 + [0] + [1] * 4 + [0] * 2,
            [0] * self.width_units,
            [0] * 2 + [1] * 4 + [0] + [1] * 2 + [0] +
            [1] * 8 + [0] + [1] * 2 + [0] + [1] * 4 + [0] * 2,
            [0] * 2 + [1] * 4 + [0] + [1] * 2 + [0] +
            [1] * 8 + [0] + [1] * 2 + [0] + [1] * 4 + [0] * 2,
            [0] * 7 + [1] * 2 + [0] * 4 + [1] *
            2 + [0] * 4 + [1] * 2 + [0] * 7,
            [0] * 7 + [1] * 5 + [0] + [1] * 2 + [0] + [1] * 5 + [0] * 7,
            [0] * 7 + [1] * 5 + [0] + [1] * 2 + [0] + [1] * 5 + [0] * 7,
            [0] * 7 + [1] * 2 + [0] * 10 + [1] * 2 + [0] * 7,
            [0] * 7 + [1] * 2 + [0] * 10 + [1] * 2 + [0] * 7,
            [0] * 7 + [1] * 2 + [0] * 10 + [1] * 2 + [0] * 7,
            [0] * self.width_units,
            [0] * 7 + [1] * 2 + [0] * 10 + [1] * 2 + [0] * 7,
            [0] * 7 + [1] * 2 + [0] * 10 + [1] * 2 + [0] * 7,
            [0] * 7 + [1] * 2 + [0] * 10 + [1] * 2 + [0] * 7,
            [0] * 7 + [1] * 2 + [0] + [1] * 8 + [0] + [1] * 2 + [0] * 7,
            [0] * 7 + [1] * 2 + [0] + [1] * 8 + [0] + [1] * 2 + [0] * 7,
            [0] * ((self.width_units - 2) // 2) + [1] *
            2 + [0] * ((self.width_units - 2) // 2),
            [0] * 7 + [1] * 5 + [0] + [1] * 2 + [0] + [1] * 5 + [0] * 7,
            [0] * 7 + [1] * 5 + [0] + [1] * 2 + [0] + [1] * 5 + [0] * 7,
            [0] * 4 + [1] * 2 + [0] * 16 + [1] * 2 + [0] * 4,
            [0] * 2 + [1] * 4 + [0] + [1] * 2 + [0] + [1] *
            8 + [0] + [1] * 2 + [0] + [1] * 4 + [0] * 2,
            [0] * 2 + [1] * 4 + [0] + [1] * 2 + [0] + [1] *
            8 + [0] + [1] * 2 + [0] + [1] * 4 + [0] * 2,
            [0] * 7 + [1] * 2 + [0] * 4 + [1] *
            2 + [0] * 4 + [1] * 2 + [0] * 7,
            [0] * 2 + [1] * 10 + [0] + [1] * 2 + [0] + [1] * 10 + [0] * 2,
            [0] * 2 + [1] * 10 + [0] + [1] * 2 + [0] + [1] * 10 + [0] * 2,
            [0] * self.width_units,
            [0] * self.width_units
        ]
        self.prison = [
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * ((self.width_units - 8) // 2) + [1] * 2 + [0] *
            4 + [1] * 2 + [0] * ((self.width_units - 8) // 2),
            [0] * ((self.width_units - 8) // 2) + [1] + [0] *
            6 + [1] + [0] * ((self.width_units - 8) // 2),
            [0] * ((self.width_units - 8) // 2) + [1] + [0] *
            6 + [1] + [0] * ((self.width_units - 8) // 2),
            [0] * ((self.width_units - 8) // 2) + [1] + [0] *
            6 + [1] + [0] * ((self.width_units - 8) // 2),
            [0] * ((self.width_units - 8) // 2) + [1] *
            8 + [0] * ((self.width_units - 8) // 2),
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units
        ]
        self.prison_inside = [
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * ((self.width_units - 4) // 2) + [1] *
            4 + [0] * ((self.width_units - 4) // 2),
            [0] * ((self.width_units - 4) // 2) + [1] *
            4 + [0] * ((self.width_units - 4) // 2),
            [0] * ((self.width_units - 4) // 2) + [1] *
            4 + [0] * ((self.width_units - 4) // 2),
            [0] * ((self.width_units - 4) // 2) + [1] *
            4 + [0] * ((self.width_units - 4) // 2),
            [0] * ((self.width_units - 4) // 2) + [1] *
            4 + [0] * ((self.width_units - 4) // 2),
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units,
            [0] * self.width_units
        ]
        self.prison_door = [
            (12, 12), (13, 12), (14, 12), (15, 12)
        ]
        self.energizers = [
            (1, 1),
            (1, self.width_units - 2),
            (self.height_units - 2, 1),
            (self.height_units - 2, self.width_units - 2)
        ]
        self.ghost_spawn = [
            (12, 14), (13, 14), (14, 14), (15, 14)
        ]
        self.pac_spawn = 13, 17
