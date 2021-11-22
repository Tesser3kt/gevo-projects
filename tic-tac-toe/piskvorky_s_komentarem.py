""" Na začátku importujeme knihovnu 'turtle', která se stará o veškeré
kreslení. Nazveme si ji v programu 'tt', jen abychom nemuseli moc psát. """
import turtle as tt

""" Jakési 'nastavení' hry. Tohle je většinou uložené v nějakém souboru mimo
hlavní program, to ale zatím neřešíme. Jde o to, že když chci třeba změnit
velikost mříže (grid), tak stačí změnit tuhle proměnnou nahoře a nemusím
přepisovat čísla v celém programu. """
GRID_SIZE = 450
FIELD_SIZE = GRID_SIZE // 3
RADIUS = (3 * FIELD_SIZE) // 8
BOUND = GRID_SIZE // 2

""" Vytvoříme si pero, které vrací funkce Turtle() z želví knihovny a
obrazovku, kterou vrací Screen(). """
pen = tt.Turtle()
screen = tt.Screen()


def draw_square(side_length):
    """ Nakreslí čtverec o straně 'side_length'. Funguje to tak, že čtyřikrát
    (in range(4)) zopakuje úkon 'vzdálenost side_length dopředu, otoč se o 90
    stupnu doleva'."""
    for _ in range(4):
        pen.forward(side_length)
        pen.left(90)


def draw_circle(x, y, radius):
    """ Nakreslí čtverec o poloměru radius na pozici (x, y). Nejprve musíme
    nastavit úhel kreslení na 0, protože želva kreslí kružnici po směru, kam se
    dívá, potom jít do bodu (x, y - poloměr) a odtud nakreslit směrem nahoru
    kružnici. """
    pen.tiltangle(0)
    pen.penup()
    pen.goto(x, y - radius)
    pen.pendown()
    pen.circle(radius)


def draw_cross(x, y, radius):
    """ Nakreslí křížek, kde 'radius' je poloměr kružnice vepsané. Prostě jenom
    udělá čáru z levého dolního do pravého horního rohu a pak z levého horního
    do pravého dolního."""
    pen.penup()
    pen.goto(x - radius, y - radius)
    pen.pendown()
    pen.goto(x + radius, y + radius)
    pen.penup()
    pen.goto(x - radius, y + radius)
    pen.pendown()
    pen.goto(x + radius, y - radius)


def draw_grid(x, y, side_length):
    """ Nakreslí 3x3 mříž o délce nejdelší strany side_length, kde (x, y) je
    levý dolní roh. """
    third = side_length // 3
    pen.pu()
    pen.goto(x, y)

    """ Nakreslím vodorovné čáry tak, že se vždycky posunu na pozici
    x + i * (třetina strany), kde i je počet opakování tohohle úkonu, a posunu
    se o délku strany nahoru. Třeba pro dvě svislé čáry to vypadá tak, že
    nakreslím čáru z (x, y) do (x, y + výška mříže), posunu se do bodu
    (x + 1 * třetina strany, y) a nakreslím čáru do (x + 1 * třetina strany,
    y + výška mříže). """
    for i in range(4):
        pen.pd()
        pen.goto(x + i * third, y + side_length)
        pen.pu()
        pen.goto(x + (i + 1) * third, y)

    """ To samé pro vodorovné čáry. Funguje úplně stejně, jen zaměním x a y.
    """
    pen.pu()
    pen.goto(x, y)
    for i in range(4):
        pen.pd()
        pen.goto(x + side_length, y + i * third)
        pen.pu()
        pen.goto(x, y + (i + 1) * third)


def handle_click(x, y):
    """ Tahle funkce řeší, co se děje při kliknutí na pozici (x, y). Nejprve se
    podívám, jestli hráč vůbec klikl dovnitř herního pole. To dělá podmínka
    if abs(x) <= BOUND and abs(y) <= BOUND. Ta kontroluje, že absolutní hodnota
    x a y je menší než hranice, kterou jsem nahoře nastavil jako polovinu
    herního pole. Čili kontroluje, jestli x jsou v intervalu [-hranice,
    hranice]. """

    # Z hlavního programu (tedy mimo tuhle funkci) si musím půjčit proměnné
    # player a board, které uchovávají informaci o herním poli (kde jsou
    # křížky, kde kolečka a kde volno) a hráči právě na tahu.
    global player, board

    if abs(x) <= BOUND and abs(y) <= BOUND:
        """ Spočítám index řádku a sloupce (čísla od 0 - první do 2 - druhý)
        podle souřadnic kurzoru myši při kliknutí, které dostala funkce v
        proměnných x a y. Protože x a y jsou obecně destinná čísla, ale já
        potřebuju celá, zavolám funkci int(), která vezme celou část čísla.
        Můžete si nakreslit, že výpočet takhle funguje za předpokladu, že střed
        mříže je v bodě (0, 0). Třeba pro kliknutí na bod (210, 30) mi musí
        vyjít řádek = 1 a sloupec = 2, čili druhý řádek a třetí sloupec.
        Ověřte si to."""
        row = (-int(y) + BOUND) // FIELD_SIZE
        col = (int(x) + BOUND) // FIELD_SIZE

        """ Pokud na políčku není 0, je tam buď křížek nebo kolečko. V takovém
        případě funkci ukončím už teď slovíčkem 'return' a nic nekreslím ani
        nezapisuju. """
        if board[row][col] != 0:
            return

        """ Na místo (řádek, sloupec) v herním poli dosadím hodnotu hráče
        právě na tahu, tedy 1 pro křížek a -1 pro kolečko."""
        board[row][col] = player

        """ Teď nakreslím příslušný symbol do mříže. Nejprve si musím spočítat
        střed políčka, kam mám kreslit. První souřadnice je x, druhá y. Můžete
        si ověřit, že to funguje. """
        center = (
            -BOUND + col * FIELD_SIZE + FIELD_SIZE // 2,
            BOUND - row * FIELD_SIZE - FIELD_SIZE // 2
        )

        if player == 1:  # Když je hráč 1, kreslím křížek.
            draw_cross(center[0], center[1], RADIUS)
        else:
            # V opačném případě, tedy hráč je -1 (jiná možnost není), kreslím
            # kolečko.
            draw_circle(center[0], center[1], RADIUS)

        """ Pokud skončila hra, kouknu se, kdo byl právě na tahu. Ten je nutně
        vítězem. Podle čísla hráče už tedy jenom napíšu, kdo vyhrál a ukončím
        želvičku funkcí bye() z její knihovny. """
        if game_over():
            if player == 1:
                print('Cross has won.')
            else:
                print('Circle has won.')
            tt.bye()

        """ Prohodím hráče. To je ta výhoda mít hráče jako 1 a -1. Pro
        prohození stačí totiž jenom napsat hráč = -hráč."""
        player = -player


def game_over():
    """ Funkce, která mi poví, zda hra skončila nebo ne. Ještě jsem zapomněl
    (doděláme příště) na případ, kdy je celé pole zaplněné a nastala remíza.
    Postupně projdeme všechny možnosti (řádky, sloupce, diagonály) a koukneme
    se, jestli v nich nejsou tři stejné znaky. Pokud ano, vrátíme True (pravda,
    tedy hra skončila) nebo False (lež, tedy ještě neskončila). """
    global board

    """ Projedu řádky. Ty jsou nejjednodušší, protože v poli jsou tři seznamy
    (řádky) každý s třemi hodnotami (sloupce). Stačí se totiž podívat, jestli
    není součet všech hodnot v jednom seznamu reprezentujícím řádek 3 (vyhrál
    křížek, nebo -3 (vyhrálo kolečko). """
    for row in board:
        if abs(sum(row)) == 3:
            return True

    """ Sloupce jsou trochu ošemetnější. Musím se vždycky podívat na součet
    i-tých hodnot v prvním, druhém a třetím řádku, kde i postupně nabývá hodnot
    0, 1 a 2. """
    for i in range(3):
        if abs(board[0][i] + board[1][i] + board[2][i]) == 3:
            return True

    """ Diagonály ošetřím natvrdo. Jsou jen dvě. """
    if abs(board[0][0] + board[1][1] + board[2][2]) == 3:
        return True

    if abs(board[0][2] + board[1][1] + board[2][0]) == 3:
        return True

    """ Když nenastala ani jedna z možností výše (nebo není remíza, na kterou
    jsem zapomněl), vrátím lež. """
    return False


""" Herní pole. Je to seznam, ve kterém jsou tři další seznamy. To mi umožňuje
přirozeně si pamatovat, kde jsou kolečka a kde křížky (to potřebuju vědět,
třeba proto, abych určil konec hry). Když se třeba chci podívat na 1. řádek a
1. sloupec herního pole, stačí napsat board[0][0]. board[0] je totiž seznam s
hodnotami prvního řádku. """
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
player = 1  # Začíná křížek.

""" Funkce onclick() je součástí knihovny 'turtle', konkrétně třídy Screen.
Dostane parametrem odkaz na funkci, která příjímá polohu myši v parametrech
x a y. V našem případě jsem ji nazvali 'handle_click'. """
screen.onclick(handle_click)

""" Tyhle dva příkazy jen dělají to, že želva kreslí rychle a není vidět. """
pen.speed(10)
pen.hideturtle()

""" Nakreslím mříž tak, aby měla střed v počátku. """
draw_grid(-BOUND, -BOUND, GRID_SIZE)

""" Probudí želvičku. """
tt.mainloop()
