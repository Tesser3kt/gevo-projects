""" Constants module. Contains static game data used throughout the app. """

WINDOW_SIZE = 640, 640
UNIT_SIZE = 16
MAX_FPS = 60
BG_COLOR = 255, 255, 255
GOAL_COLOR = 100, 200, 100
WINDOW_TITLE = 'Hardest Game Ever'
LEVELS = [
    {
        'player_start': (19, 1),
        'player_goals': [(14, 38, 1, 10)],
        'enemy_paths': [
            [(1, 9), (38, 9), (1, 9)],
            [(1, 14), (24, 14), (1, 14)],
            [(25, 14), (38, 14), (25, 14)]
        ],
        'walls': [[1] * 40] + [[1] + [0] * 38 + [1]] * 38 + [[1] * 40]
    },
    {
        'player_start': (1, 1),
        'player_goals': [(35, 38, 1, 4), (38, 37, 2, 1)],
        'enemy_paths': [
            [(5, 20), (10, 1), (20, 1), (10, 1), (5, 20)],
        ],
        'walls': [[1] * 40] + [[1] + [0] * 38 + [1]] * 32 +
        [[1] * 8 + [0] * 24 + [1] * 8] + [[1] + [0] * 38 + [1]] *
        2 + [[1] * 8 + [0] * 24 + [1] * 8] + [[1] + [0] * 38 + [1]] *
        2 + [[1] * 40]
    }
]
PLAYER_SPEED = [
    0.2,
    0.3
]
ENEMY_SPEED = [
    [0.2, 0.1, 0.3],
    [0.3]
]
