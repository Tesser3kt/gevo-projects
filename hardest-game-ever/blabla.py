import pygame as pg

pg.init()
canvas = pg.display.set_mode((1000, 1000), pg.SCALED)
square = pg.Surface((100, 100))
square.fill((255, 0, 0))
square = square.convert()
canvas.blit(square, (100, 100))
square = pg.Surface((100, 100))
square.fill((0, 255, 0))
square = square.convert()
canvas.blit(square, (200, 200))
square = pg.Surface((100, 100))
square.fill((0, 0, 255))
square = square.convert()
canvas.blit(square, (300, 300))
pg.display.update()

while True:
    pass
