""" Contains the Game class. """

import math
from typing import Tuple, Sequence
import pygame as pg

import constants as ct
from gfx import Graphics
from game_object import GameObject
from circle import Circle
from tile import Tile


class Game:
    """ Main game class. Controls the movement of game objects and handles user
    input. """

    def __init__(self):
        self.gfx: Graphics = None
        self.clock: pg.time.Clock = None
        self.running: bool = False
        self.paused: bool = False
        self.player: GameObject = None
        self.enemies: pg.sprite.Group = pg.sprite.Group()
        self.mobile_objects: pg.sprite.Group = pg.sprite.Group()
        self.enemy_path_index: list[int] = []
        self.enemy_pixel_debt: list[list[float, float]] = []
        self.walls: pg.sprite.Group = pg.sprite.Group()
        self.goals: pg.sprite.Group = pg.sprite.Group()
        self.immobile_objects: pg.sprite.Group = pg.sprite.Group()
        self.level: int = 0

    def __spawn_mobile(self) -> None:
        """ Spawns mobile game objects: player and enemy. """

        # create player object with starting position based on current level
        self.player = Circle(
            texture=self.gfx.textures['player'],
            x=ct.LEVELS[self.level]['player_start'][0] * ct.UNIT_SIZE,
            y=ct.LEVELS[self.level]['player_start'][1] * ct.UNIT_SIZE
        )

        # create enemy objects with starting position based on current level
        for path in ct.LEVELS[self.level]['enemy_paths']:
            self.enemies.add(Circle(
                texture=self.gfx.textures['enemy'],
                x=path[0][0] * ct.UNIT_SIZE,
                y=path[0][1] * ct.UNIT_SIZE
            ))
            self.enemy_path_index.append(1)
            self.enemy_pixel_debt.append([0, 0])

    def __spawn_walls_and_goal(self) -> None:
        """ Spawns walls and player goal. """

        # create wall objects based on current level
        for row_index, row in enumerate(ct.LEVELS[self.level]['walls']):
            for col, field in enumerate(row):
                if field:
                    self.walls.add(Tile(
                        texture=self.gfx.textures['wall'],
                        x=col * ct.UNIT_SIZE,
                        y=row_index * ct.UNIT_SIZE
                    ))

        # create player goal tiles and fill them with GOAL_COLOR
        for goal in ct.LEVELS[self.level]['player_goals']:
            # create GOAL_COLOR surface
            texture = pg.Surface(
                (goal[3] * ct.UNIT_SIZE, goal[2] * ct.UNIT_SIZE))
            texture = texture.convert()
            texture.fill(ct.GOAL_COLOR)

            # add goal to player goals list
            self.goals.add(Tile(
                texture=texture,
                x=goal[0] * ct.UNIT_SIZE,
                y=goal[1] * ct.UNIT_SIZE,
                height=goal[2] * ct.UNIT_SIZE,
                width=goal[3] * ct.UNIT_SIZE
            ))

    def __arrow_key_pressed(self, pressed: dict[str, bool]) -> bool:
        """ Checks if any arrow key was pressed. """

        return any((pressed[pg.K_UP],
                    pressed[pg.K_RIGHT],
                    pressed[pg.K_DOWN],
                    pressed[pg.K_LEFT]))

    def __get_player_dir_vector(self,
                                pressed: Sequence[bool]) -> Tuple[int, int]:
        """ Determines the direction vector based on the type of arrow pressed.
        """

        # handle diagonal directions
        movement_unit = ct.PLAYER_SPEED[self.level] * ct.UNIT_SIZE
        if pressed[pg.K_UP] and pressed[pg.K_RIGHT]:
            vector = 1, -1
        elif pressed[pg.K_RIGHT] and pressed[pg.K_DOWN]:
            vector = 1, 1
        elif pressed[pg.K_DOWN] and pressed[pg.K_LEFT]:
            vector = -1, 1
        elif pressed[pg.K_LEFT] and pressed[pg.K_UP]:
            vector = -1, -1

        # handle straight directions
        elif pressed[pg.K_UP]:
            vector = 0, -1
        elif pressed[pg.K_RIGHT]:
            vector = 1, 0
        elif pressed[pg.K_DOWN]:
            vector = 0, 1
        elif pressed[pg.K_LEFT]:
            vector = -1, 0

        return tuple(coor * movement_unit for coor in vector)

    def __player_can_move(self, vector: Tuple[int, int]) -> bool:
        """ Checks if player can move by the specified vector. """

        # remember current player position and move him by vector
        cur_player_pos = self.player.rect.copy()
        self.player.move(*vector)

        # check collision with walls
        collides = pg.sprite.spritecollideany(
            self.player, self.walls) is not None

        # move player back and return collision
        self.player.rect = cur_player_pos.copy()
        return not collides

    def __move_player(self, pressed: Sequence[bool]) -> pg.Rect:
        """ Moves the player based on the arrow pressed if game is not
        paused. """

        if self.paused:
            return None

        # get direction vector
        vector = self.__get_player_dir_vector(pressed)

        # check if a wall isn't in the way
        if not self.__player_can_move(vector):
            return None

        # remember player's last position
        current_player_pos = self.player.rect.copy()

        # move player
        self.player.move(*vector)

        # return the rect containing both player's old and new position
        return current_player_pos.union(self.player.rect)

    def __enemy_collides_with_goal(self, index: int, enemy: GameObject,
                                   path: list[Tuple[int, int]]) -> bool:
        """ Checks if the given enemy collides with a fixed point on its path.
        """

        enemy_cur_goal = path[self.enemy_path_index[index]]
        aux_rect = pg.Rect(
            enemy_cur_goal[0] * ct.UNIT_SIZE,
            enemy_cur_goal[1] * ct.UNIT_SIZE,
            ct.UNIT_SIZE,
            ct.UNIT_SIZE
        )
        error = ct.ENEMY_SPEED[self.level][index] * ct.UNIT_SIZE

        # check that centerpoints of both rects are sufficiently close to one
        # another
        return (aux_rect.centerx - error <= enemy.rect.centerx
                <= aux_rect.centerx + error)\
            and (aux_rect.centery - error <= enemy.rect.centery
                 <= aux_rect.centery + error)

    def __get_enemy_dir_vector(self, enemy_index: int, path_index: int,
                               path: list[Tuple[int, int]]) -> Tuple[int, int]:
        """ Calculates the direction vector for the enemy based on its path and
        speed. """

        vector = (path[path_index][0] - path[path_index - 1][0],
                  path[path_index][1] - path[path_index - 1][1])

        # normalize it to step size
        movement_unit = ct.UNIT_SIZE * ct.ENEMY_SPEED[self.level][enemy_index]
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        vector = (vector[0] * movement_unit / vector_length,
                  vector[1] * movement_unit / vector_length)

        # calculate pixel debt due to inaccuracies
        self.enemy_pixel_debt[enemy_index][0] += vector[0] % 1
        self.enemy_pixel_debt[enemy_index][1] += vector[1] % 1
        vector = math.floor(vector[0]), math.floor(vector[1])

        # add pixel debt to direction vector if greater than 1
        if self.enemy_pixel_debt[enemy_index][0] > 1:
            self.enemy_pixel_debt[enemy_index][0] -= 1
            vector = vector[0] + 1, vector[1]

        if self.enemy_pixel_debt[enemy_index][1] > 1:
            self.enemy_pixel_debt[enemy_index][1] -= 1
            vector = vector[0], vector[1] + 1

        return vector

    def __move_enemies(self) -> list[pg.Rect]:
        """ Moves each enemy along its given path. Returns the list of parts of
        canvas to update. """

        changed_rects: list[pg.Rect] = []

        for enemy_index, enemy in enumerate(self.enemies):
            # get enemy path
            enemy_path = ct.LEVELS[self.level]['enemy_paths'][enemy_index]

            # check if enemy collides with its goal rect
            if self.__enemy_collides_with_goal(enemy_index, enemy, enemy_path):
                # update path index
                self.enemy_path_index[enemy_index] += 1

                # if enemy reached the end of path, follow it again from start
                if self.enemy_path_index[enemy_index] == len(enemy_path):
                    self.enemy_path_index[enemy_index] = 1

            # calculate the direction vector for the enemy
            path_index = self.enemy_path_index[enemy_index]
            vector = self.__get_enemy_dir_vector(
                enemy_index, path_index, enemy_path)

            # remember previous enemy position
            prev_enemy_rect = enemy.rect.copy()

            # move enemy and add rect to changed rects
            enemy.move(*vector)
            changed_rects.append(enemy.rect.union(prev_enemy_rect))

        return changed_rects

    def __reset_level(self) -> None:
        """ Resets the state of moving objects in the current level. """

        # draw bg over all moving game objects and destroy them
        self.gfx.draw_bg_over_group(self.mobile_objects)
        self.mobile_objects.empty()
        self.player = None
        self.enemies.empty()
        self.enemy_path_index = []
        self.enemy_pixel_debt = []

        # spawn mobile objects anew
        self.__spawn_mobile()
        self.mobile_objects.add(self.player, self.enemies)

        # draw mobile objects onto the canvas
        self.gfx.draw_group(self.mobile_objects)

        # update the whole canvas (for simplicity)
        self.gfx.update_canvas()

    def __raise_level(self) -> None:
        """ Raises the game level clearing the entire canvas and redrawing
        sprites. """

        # draw background over the entire canvas
        self.gfx.clear_canvas()

        # delete all game objects
        self.mobile_objects.empty()
        self.enemies.empty()
        self.enemy_path_index = []
        self.enemy_pixel_debt = []
        self.player = None
        self.immobile_objects.empty()
        self.walls.empty()
        self.goals.empty()

        # raise the level (or go back to level 1 if no higher levels are
        # defined) and spawn game objects at new locations
        self.level = (self.level + 1) % len(ct.LEVELS)
        self.spawn_all()

    def ready(self) -> None:
        """ Initializes the game graphics and loads game object textures. """

        # init gfx
        self.gfx = Graphics()
        self.gfx.init_gfx()

        # load textures
        self.gfx.load_textures()

    def spawn_all(self) -> None:
        """ Spawns all game objects. """

        # spawn mobile
        self.__spawn_mobile()
        self.mobile_objects.add(self.player, self.enemies)

        # spawn immobile
        self.__spawn_walls_and_goal()
        self.immobile_objects.add(self.walls, self.goals)

        # draw all objects on screen
        self.gfx.draw_group(self.mobile_objects)
        self.gfx.draw_group(self.immobile_objects)

        # update the screen
        self.gfx.update_canvas()

    def update(self, rects_to_update: list[pg.Rect]) -> None:
        """ Updates the game every frame. Moves enemies along their paths and
        redraws the updated parts of canvas. Only run when game is not paused.
        """

        if self.paused:
            return

        rects_to_update += self.__move_enemies()

        # check if player hasn't collided with enemy
        if pg.sprite.spritecollideany(self.player, self.enemies):
            print('Player collided with enemy. Resetting level...')
            self.__reset_level()

        # check if player hasn't reached the goal
        if pg.sprite.spritecollideany(self.player, self.goals):
            print('Player has reached the goal. Up the level.')
            self.__raise_level()

        # draw background over moving objects
        self.gfx.draw_bg_over_group(self.mobile_objects)

        # redraw moving objects
        self.gfx.draw_group(self.mobile_objects)

        # update the changed parts of canvas
        self.gfx.update_canvas(rects_to_update)

    def run(self) -> None:
        """ Runs the game and keeps it running until exit signal is given. """
        self.running = True

        # start the FPS clock
        self.clock = pg.time.Clock()

        while self.running:
            # calculate time elapsed since last frame
            self.clock.tick(ct.MAX_FPS)

            # init list of changes parts of canvas
            rects_to_update: list[pg.Rect] = []

            # get key presses
            keys_pressed = pg.key.get_pressed()

            # check arrow key presses and move player accordingly
            if self.__arrow_key_pressed(keys_pressed):
                rects_to_update.append(self.__move_player(keys_pressed))

            # update
            self.update(rects_to_update)

            # check for possible quit and pause events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # quit the game
                    self.running = False
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # pause the game on ESC
                        self.paused = not self.paused
