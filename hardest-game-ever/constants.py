""" Constants module. Contains static game data used throughout the app. """

WINDOW_SIZE = 640, 640
UNIT_SIZE = 16
BG_COLOR = 255, 255, 255
WINDOW_TITLE = 'Hardest Game Ever'
LEVELS = [
    {
        'player_start': (19, 1),
        'enemy_paths': [
            [(1, 9), (38, 9)]
        ],
        'walls': [1] * 40 + [[1] + [0] * 38 + [1]] * 38 + [1] * 40
    }
]
