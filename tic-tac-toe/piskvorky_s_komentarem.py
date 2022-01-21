import turtle as tt

""" Upravené konstanty pro NxN piškvorky. """
FIELD_COUNT = 20
GRID_SIZE = 800
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
    """ Upravená funkce nakreslení mříže. Tady prostě stačilo zavést proměnnou
    field_count a nahradit jí všechny trojky, aby funkce uměla kreslit NxN
    mříž. """
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

            """ Když skončila hra, zruším efekt kliknutí na políčko. Slovo
            'None' v Pythonu značí prostě 'nic', takže jen říkám želvičce, že
            při kliknutí na obrazovku má dělat 'nic'. """
            screen.onclick(None)

            """ Pokud hra skončila, funkci tu ukončím. Jinak by se totiž mohlo
            stát, že bych vypsal jak výhru, tak remízu, pokud by někdo vyhrál a
            zároveň by bylo plné pole. """
            return

        """ To samé, co výše. Prostě se kouknu jestli nastala remíza. Jestli
        ano, vezmu hráči možnost klikat. """
        if tie():
            print('Tie.')
            screen.onclick(None)

        player = -player


def tie():
    """ Tady projíždím každý řádek v herním poli a v něm každé políčko. Pokud
    najdu 0, znamená to, že je ještě někde volné místo a remíza nenastala,
    takže vracím 'lež'. Naopak, pokud projdu celé pole a 0 nenajdu, je celé
    plné křížků a koleček, takže vracím 'pravda'. """
    for row in board:
        for field in row:
            if field == 0:
                return False

    return True


def game_over():
    """ Nefunguje pro piškvorky NxN. Budeme předělávat. """
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


def clear_board():
    """ Pomocí funkce clear() vyčistí obrazovku, pak znovu povolí klikání tím,
    že funkci onclick z želví knihovny předá naši handle_click, znovu nakreslí
    herní pole, vyčistí seznam políček a nastaví hráče na křížek. """
    global board, player
    pen.clear()
    screen.onclick(handle_click)
    draw_grid(-BOUND, -BOUND, GRID_SIZE, FIELD_COUNT)
    board = [[0] * FIELD_COUNT] * FIELD_COUNT
    player = 1


""" Vytvoří herní pole s proměnným počtem políček. Tenhle zápis prostě říká
Python, aby vzal seznam [0] a FIELD_COUNT-krát ho zkopíroval, vytvořiv prostě
seznam s FIELD_COUNT nulami. Pak má vzít tenhle seznam a zase ho
FIELD_COUNT-krát zkopírovat. Jinak řečeno, vytvoří seznam FIELD_COUNT seznamů,
každý s FIELD_COUNT nulami. """
board = [[0] * FIELD_COUNT] * FIELD_COUNT
player = 1
screen.onclick(handle_click)

""" Kliknutím mezerníku restartujeme hru přes funkci clear(). O kliknutí na
klávesu se stará řelví funkce onkey(). Aby ale želva vnímala klávesnici, je
ještě potřeba před startem zavolat funkci listen(), o 3 řádky níž. """
screen.onkey(clear_board, 'space')
pen.speed(0)
pen.hideturtle()
tt.listen()

draw_grid(-BOUND, -BOUND, GRID_SIZE, FIELD_COUNT)

tt.mainloop()
