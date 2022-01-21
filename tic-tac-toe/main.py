import turtle as tt

FIELD_COUNT = 30
GRID_SIZE = 900
FIELD_SIZE = GRID_SIZE // FIELD_COUNT
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


def draw_grid(x, y, side_length, field_count):
    field_size = side_length // field_count
    pen.pu()
    pen.goto(x, y)

    for i in range(field_count + 1):
        pen.pd()
        pen.goto(x + i * field_size, y + side_length)
        pen.pu()
        pen.goto(x + (i + 1) * field_size, y)

    pen.pu()
    pen.goto(x, y)
    for i in range(field_count + 1):
        pen.pd()
        pen.goto(x + side_length, y + i * field_size)
        pen.pu()
        pen.goto(x, y + (i + 1) * field_size)


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

            screen.onclick(None)
            return

        if tie():
            print('Tie.')
            screen.onclick(None)

        player = -player


def tie():
    global board
    for row in board:
        for field in row:
            if field == 0:
                return False

    return True


def game_over():
    global board

    # check rows
    for row in board:
        for i in range(FIELD_COUNT - 4):
            if abs(sum(row[i + j] for j in range(5))) == 5:
                return True

    # check columns
    for col in range(FIELD_COUNT):
        for i in range(FIELD_COUNT - 4):
            if abs(sum(board[i + j][col] for j in range(5))) == 5:
                return True

    # check diags
    for row in range(FIELD_COUNT - 4):
        # left -> right
        for col in range(FIELD_COUNT - 4):
            if abs(sum(board[row + i][col + i] for i in range(5))) == 5:
                return True

        # right -> left
        for col in range(4, FIELD_COUNT):
            if abs(sum(board[row + i][col - i] for i in range(5))) == 5:
                return True

    return False


def clear_board():
    global board, player
    pen.clear()
    screen.onclick(handle_click)
    draw_grid(-BOUND, -BOUND, GRID_SIZE, FIELD_COUNT)
    board = [[0 for _ in range(FIELD_COUNT)] for _ in range(FIELD_COUNT)]
    player = 1


board = [[0 for _ in range(FIELD_COUNT)] for _ in range(FIELD_COUNT)]
player = 1
screen.onclick(handle_click)
screen.onkey(clear_board, 'space')
pen.speed(0)
pen.hideturtle()
tt.listen()

draw_grid(-BOUND, -BOUND, GRID_SIZE, FIELD_COUNT)

tt.mainloop()
