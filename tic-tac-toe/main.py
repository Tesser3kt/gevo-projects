import turtle as tt

GRID_SIZE = 600
FIELD_SIZE = GRID_SIZE // 3
RADIUS = (3 * FIELD_SIZE) // 8
BOUND = GRID_SIZE // 2

pen = tt.Turtle()
screen = tt.Screen()


def draw_square(side_length):
    # Draw a square of side length 'side'.
    for _ in range(4):
        pen.forward(side_length)
        pen.left(90)


def draw_circle(x, y, radius):
    # Draw a circle of radius 'radius' at (x, y).
    pen.penup()
    pen.goto(x, y - radius)
    pen.pendown()
    pen.circle(radius)


def draw_cross(x, y, radius):
    # Draw a cross centered at (x, y) of radius 'radius'.
    pen.penup()
    pen.goto(x - radius, y - radius)
    pen.pendown()
    pen.goto(x + radius, y + radius)
    pen.penup()
    pen.goto(x - radius, y + radius)
    pen.pendown()
    pen.goto(x + radius, y - radius)


def draw_grid(x, y, side_length):
    third = side_length // 3
    pen.pu()
    pen.goto(x, y)

    for i in range(4):
        pen.pd()
        pen.goto(x + i * third, y + side_length)
        pen.pu()
        pen.goto(x + (i + 1) * third, y)

    pen.pu()
    pen.goto(x, y)
    for i in range(4):
        pen.pd()
        pen.goto(x + side_length, y + i * third)
        pen.pu()
        pen.goto(x, y + (i + 1) * third)


def handle_click(x, y):
    global player, board
    if abs(x) <= BOUND and abs(y) <= BOUND:
        row = (-int(y) + BOUND) // FIELD_SIZE
        col = (int(x) + BOUND) // FIELD_SIZE

        if board[row][col] != 0:
            return

        board[row][col] = player

        center = (
            -BOUND + col * FIELD_SIZE + FIELD_SIZE // 2,
            BOUND - row * FIELD_SIZE - FIELD_SIZE // 2
        )

        if player == 1:
            draw_cross(center[0], center[1], RADIUS)
        else:
            draw_circle(center[0], center[1], RADIUS)

        if game_over():
            if player == 1:
                print('Cross has won.')
            else:
                print('Circle has won.')
            tt.bye()

        player = -player


def game_over():
    global board

    # check rows
    for row in board:
        if abs(sum(row)) == 3:
            return True

    # check columns
    for i in range(3):
        if abs(board[0][i] + board[1][i] + board[2][i]) == 3:
            return True

    # check diags
    if abs(board[0][0] + board[1][1] + board[2][2]) == 3:
        return True

    if abs(board[0][2] + board[1][1] + board[2][0]) == 3:
        return True

    return False


board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
player = 1
screen.onclick(handle_click)
pen.speed(10)
pen.hideturtle()

draw_grid(-BOUND, -BOUND, GRID_SIZE)

tt.mainloop()
