from turtle import *

SIZE = 450
BOUND = SIZE // 2
FIELD_SIZE = SIZE // 3
SYMBOL_RADIUS = 3 * FIELD_SIZE // 8
DEFAULT_COLOR = (0, 0, 0)
PLAYER_COLOR = {
    -1: (255, 0, 0),
    1: (0, 0, 255)
}
TEXT_POSITION = -(BOUND + 100)
DRAWING_SPEED = 10


class Drawer:
    def __init__(self):
        self.pen = Turtle()
        self.pen.pu()
        self.pen.hideturtle()
        self.pen.speed(DRAWING_SPEED)

    def draw_line(self, x1, y1, x2, y2, color):
        """ Draws a line from (x1, y1) to (x2, y2) with the given color.
        """

        self.pen.goto(x1, y1)
        self.pen.color(color)
        self.pen.pd()
        self.pen.goto(x2, y2)
        self.pen.pu()

    def draw_circle(self, x, y, radius, color):
        """ Draws a circle at (x, y) with the given radius and color."""

        self.pen.goto(x, y - radius)
        self.pen.color(color)
        self.pen.pd()
        self.pen.circle(radius)
        self.pen.pu()

    def draw_cross(self, x, y, radius, color):
        """ Draws a cross at (x, y) with the given radius and color."""

        self.pen.color(color)

        # top left corner - bottom right corner
        self.pen.goto(x - radius, y - radius)
        self.pen.pd()
        self.pen.goto(x + radius, y + radius)
        self.pen.pu()

        # top right corner - bottom left corner
        self.pen.goto(x + radius, y - radius)
        self.pen.pd()
        self.pen.goto(x - radius, y + radius)
        self.pen.pu()

    def draw_board(self, x, y, color):
        """ Draws a board starting from top left corner with given
        height, width and color."""

        self.pen.color(color)
        self.pen.goto(x, y)
        self.pen.pd()

        # drawing the main square
        self.pen.goto(x, y + SIZE)
        self.pen.goto(x + SIZE, y + SIZE)
        self.pen.goto(x + SIZE, y)
        self.pen.goto(x, y)
        self.pen.pu()

        # drawing the horizontal bars
        self.pen.goto(x, y + FIELD_SIZE)
        self.pen.pd()
        self.pen.goto(x + SIZE, y + FIELD_SIZE)
        self.pen.pu()
        self.pen.goto(x, y + 2*FIELD_SIZE)
        self.pen.pd()
        self.pen.goto(x + SIZE, y + 2*FIELD_SIZE)
        self.pen.pu()

        # drawing the vertical bars
        self.pen.goto(x + FIELD_SIZE, y)
        self.pen.pd()
        self.pen.goto(x + FIELD_SIZE, y + SIZE)
        self.pen.pu()
        self.pen.goto(x + 2*FIELD_SIZE, y)
        self.pen.pd()
        self.pen.goto(x + 2*FIELD_SIZE, y + SIZE)
        self.pen.pu()

    def write_message(self, x, y, color, message):
        """ Writes a message on the given coordinates. """

        self.pen.color(color)
        self.pen.goto(x, y)
        self.pen.write(message, align='center', font=('Arial', 30, 'bold'))


class Game:
    def __init__(self, drawer, screen):
        self.player = 1
        self.drawer = drawer
        self.screen = screen
        self.board = []

    def start_game(self):
        # bind click to handle_click
        self.screen.onclick(self.handle_click)

        # initialize board
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.drawer.draw_board(-BOUND, -BOUND, DEFAULT_COLOR)

        # loop
        self.screen.mainloop()

    def handle_click(self, x, y):
        """ Handles mouse clicks. """

        valid_click = -BOUND <= x <= BOUND and -BOUND <= y <= BOUND
        if valid_click:
            row = int((x + BOUND) // FIELD_SIZE)
            col = int((y + BOUND) // FIELD_SIZE)
            self.handle_turn(row, col)

    def handle_turn(self, row, col):
        """ Plays on the (row, col) field. """

        if self.board[row][col] == 0:
            self.board[row][col] = self.player
            self.place_symbol(row, col)

            if self.is_over():
                self.end_game()
                return

            self.player = -self.player

    def place_symbol(self, row, col):
        """ Places player's symbol on the specified field. """

        field_center = (
            -BOUND + row * FIELD_SIZE + FIELD_SIZE // 2,
            -BOUND + col * FIELD_SIZE + FIELD_SIZE // 2
        )
        if self.player == 1:
            self.drawer.draw_cross(
                *field_center, SYMBOL_RADIUS, PLAYER_COLOR[self.player])
        else:
            self.drawer.draw_circle(
                *field_center, SYMBOL_RADIUS, PLAYER_COLOR[self.player])

    def is_over(self):
        """ Checks if any player has won the game. """

        # check rows and columns
        for i in range(3):
            row_sum = abs(sum(self.board[i]))
            col_sum = abs(sum(self.board[j][i] for j in range(3)))
            if row_sum == 3 or col_sum == 3:
                return True

        # check diagonals
        main_diag_sum = abs(sum(self.board[i][i] for i in range(3)))
        sec_diag_sum = abs(sum(self.board[i][2 - i] for i in range(3)))

        if main_diag_sum == 3 or sec_diag_sum == 3:
            return True

        return False

    def end_game(self):
        """ Writes the victor and ends drawing. """

        self.screen.onclick(None)
        if self.player == 1:
            message = 'Cross has won the game!'
        else:
            message = 'Circle has won the game!'

        self.drawer.write_message(
            0, TEXT_POSITION, PLAYER_COLOR[self.player], message)


def main():
    # initialize the window
    screen = Screen()
    screen.colormode(255)

    # initialize drawer and game
    drawer = Drawer()
    game = Game(drawer, screen)
    game.start_game()


if __name__ == '__main__':
    main()
