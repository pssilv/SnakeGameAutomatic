from scenario import Scenario
from entitymanager import EntityManager
import time
import random


class SnakeGame():
    def __init__(self, rows, cols, snakeQ, fruitG):
        self._scenario = Scenario(rows, cols)
        self.entitymanager = EntityManager(rows, cols, snakeQ, fruitG, self)

        while len(self.entitymanager._snake_list) > 1:
            for snake in self.entitymanager._snake_list:
                if self._scenario._win.get_is_running() is True:
                    self.snake_main_movement(snake)
                else:
                    break

            if self._scenario._win.get_is_running() is False:
                print("Window closed")
                break

            time.sleep(0.1)

        if len(self.entitymanager._snake_list) == 1:
            print(f"Snake {self.entitymanager._snake_list[0]._id} winned the game!")

    def find_the_nearest_fruit(self, snake):
        closest_fruit_y = float("inf")
        closest_fruit_x = float("inf")

        for fruit in self.entitymanager._fruit_list:
            fruit_dist_y = abs(snake._head_position[0] - fruit._pos[0])
            fruit_dist_x = abs(snake._head_position[1] - fruit._pos[1])

            total_fruit_dist = closest_fruit_y + closest_fruit_x

            if (fruit_dist_y + fruit_dist_x) < total_fruit_dist:
                closest_fruit_y = fruit_dist_y
                closest_fruit_x = fruit_dist_x
                fruit_index = self.entitymanager._fruit_list.index(fruit)

        return self.entitymanager._fruit_list[fruit_index]

    def snake_main_movement(self, snake):
        fruit = self.find_the_nearest_fruit(snake)
        self.calculate_available_paths(snake, fruit)

        snake._past_movement = (snake._head_position[0], snake._head_position[1])

        if len(snake._available_paths) > 0:
            snake._path_to_fruit.append(snake._available_paths[0])
            self.move_snake_to_fruit(snake)
            self.fruit_eated_listener(snake)
        else:
            print(f"Snake {snake._id} died!")
            self.remove_snake(snake)

    def move_snake_to_fruit(self, snake):
        self.delete_snake_old_pos(snake)

        snake._head_position = snake._path_to_fruit.pop(0)

        self.entitymanager.draw_entity(snake)

    def delete_snake_old_pos(self, entity):
        col = entity._head_position[0]
        row = entity._head_position[1]

        entity_assigned_cell = self._scenario._total_cells[col][row]

        factor_x = self._scenario._cell_size / 8
        factor_y = self._scenario._cell_col_size / 8

        x1 = entity_assigned_cell._x1 + factor_x
        y1 = entity_assigned_cell._y1 + factor_y
        x2 = entity_assigned_cell._x2 - factor_x
        y2 = entity_assigned_cell._y2 - factor_y

        entity_assigned_cell.generate_color([x1, y1, x2, y2], "black")

        self._scenario._win.redraw()

    def calculate_available_paths(self, snake, fruit):
        self.entitymanager.update_available_positions()

        next_move_y = self.update_next_move(snake._head_position[0], fruit._pos[0])
        next_move_x = self.update_next_move(snake._head_position[1], fruit._pos[1])

        head_pos_y = snake._head_position[0]
        head_pos_x = snake._head_position[1]

        moves = []
        snake._available_paths = []

        if (head_pos_y + 1, head_pos_x) in self._scenario._available_positions:
            moves.append( (head_pos_y + 1, head_pos_x) )

        if (head_pos_y - 1, head_pos_x) in self._scenario._available_positions:
            moves.append( (head_pos_y - 1, head_pos_x) )

        if (head_pos_y, head_pos_x + 1) in self._scenario._available_positions:
            moves.append( (head_pos_y, head_pos_x + 1) )

        if (head_pos_y, head_pos_x - 1) in self._scenario._available_positions:
            moves.append( (head_pos_y, head_pos_x - 1) )

        if snake._past_movement in moves:
            past_path = moves.index(snake._past_movement)
            del moves[past_path]

        for move in moves:
            if move == (head_pos_y + next_move_y, head_pos_x):
                snake._available_paths.append(move)
                move_index = moves.index(move)
                del moves[move_index]

            if move == (head_pos_y, head_pos_x + next_move_x):
                snake._available_paths.append(move)
                move_index = moves.index(move)
                del moves[move_index]

        while len(moves) > 0:
            move = random.choice(moves)
            move_index = moves.index(move)

            snake._available_paths.append(move)
            del moves[move_index]

        self.get_direction(snake)

        if snake._past_movement in snake._available_paths:
            past_index = snake._available_paths.index(snake._past_movement)
            del snake._available_paths[past_index]

    def update_next_move(self, head_pos, fruit_pos):
        if head_pos != fruit_pos:
            delta = fruit_pos - head_pos

            if delta > 0:
                return 1
            elif delta < 0:
                return -1
        return 0

    def get_direction(self, snake):
        head_pos = snake._head_position

        if len(snake._available_paths) > 0:
            next_move = snake._available_paths[0]
        else:
            next_move = (0, 0)

        if (next_move[0] - head_pos[0]) == 1:
            snake._direction = "down"
            snake._past_movement = (head_pos[0] - 1, head_pos[1])

        elif (next_move[1] - head_pos[1]) == 1:
            snake._direction = "right"
            snake._past_movement = (head_pos[0], head_pos[1] - 1)

        elif (next_move[0] - head_pos[0]) == -1:
            snake._direction = "up"
            snake._past_movement = (head_pos[0] + 1, head_pos[1])

        elif (next_move[1] - head_pos[1]) == -1:
            snake._direction = "left"
            snake._past_movement = (head_pos[0], head_pos[1] + 1)

    def remove_snake(self, snake):
        self.delete_snake_old_pos(snake)
        self.entitymanager._snake_list.remove(snake)

    def fruit_eated_listener(self, snake):
        for fruit in self.entitymanager._fruit_list:
            if fruit._pos == snake._head_position:
                self.entitymanager.regenerate_fruit(fruit)
