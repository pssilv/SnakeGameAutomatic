from scenario import Scenario
from entitymanager import EntityManager
import time
import random


class SnakeGame():
    def __init__(self, rows, cols, snakeQ, fruitG):
        self._scenario = Scenario(rows, cols)
        self.entitymanager = EntityManager(rows, cols, snakeQ, fruitG, self)

        game_iterations = 0
        while len(self.entitymanager._snake_list) > 1:
            for snake in self.entitymanager._snake_list:
                if self._scenario._win.get_is_running() is True:
                    self.snake_main_movement(snake)
                else:
                    break

            if self._scenario._win.get_is_running() is False:
                break

            game_iterations += 1
            time.sleep(0.1)

        if len(self.entitymanager._snake_list) == 1:
            print(f"Snake {self.entitymanager._snake_list[0]._id} winned the game!")
            print(f"Total iterations: {game_iterations}")

        self._scenario._win.wait_for_close()

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
        self.entitymanager.delete_entity_polygon(snake)
        snake._head_position = snake._path_to_fruit.pop(0)

        self.update_snake_body_size(snake)

        self.entitymanager.draw_entity(snake)

    def calculate_available_paths(self, snake, fruit):
        self.entitymanager.update_available_positions()

        next_move_y = self.update_next_move(snake._head_position[0], fruit._pos[0])
        next_move_x = self.update_next_move(snake._head_position[1], fruit._pos[1])

        head_pos_y = snake._head_position[0]
        head_pos_x = snake._head_position[1]

        moves = []
        snake._available_paths = []

        if (head_pos_y + 1, head_pos_x) in self._scenario._available_positions:
            moves.append((head_pos_y + 1, head_pos_x))

        if (head_pos_y - 1, head_pos_x) in self._scenario._available_positions:
            moves.append((head_pos_y - 1, head_pos_x))

        if (head_pos_y, head_pos_x + 1) in self._scenario._available_positions:
            moves.append((head_pos_y, head_pos_x + 1))

        if (head_pos_y, head_pos_x - 1) in self._scenario._available_positions:
            moves.append((head_pos_y, head_pos_x - 1))

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
            next_move = (-1, -1)

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
        self.entitymanager.delete_entity_polygon(snake)
        self.entitymanager._snake_list.remove(snake)

    def fruit_eated_listener(self, snake):
        for fruit in self.entitymanager._fruit_list:
            if fruit._pos == snake._head_position:
                self.increase_snake(snake)
                self.entitymanager.regenerate_fruit(fruit)

                if fruit._pos == snake._head_position:
                    self.entitymanager.delete_entity_polygon(fruit)

    def increase_snake(self, snake):

        if len(snake._body_parts_pos) == 0:
            snake._body_parts_pos = [snake._past_movement]

        elif len(snake._body_parts_pos) == 1:
            body_part = snake._body_parts_pos[0]

            if snake._head_position[0] - body_part[0] == 1:
                snake._body_parts_pos.append((body_part[0] - 1, body_part[1]))

            elif snake._head_position[0] - body_part[0] == -1:
                snake._body_parts_pos.append((body_part[0] + 1, body_part[1]))

            elif snake._head_position[1] - body_part[1] == 1:
                snake._body_parts_pos.append((body_part[0], body_part[1] - 1))

            elif snake._head_position[1] - body_part[1] == -1:
                snake._body_parts_pos.append((body_part[0], body_part[1] + 1))

        elif len(snake._body_parts_pos) > 1:
            body_part = snake._body_parts_pos[-1]
            to_move = snake._body_parts_pos[-2]

            if to_move[0] - body_part[0] == 1:
                snake._body_parts_pos.append((body_part[0] - 1, body_part[1]))

            elif to_move[0] - body_part[0] == -1:
                snake._body_parts_pos.append((body_part[0] + 1, body_part[1]))

            elif to_move[1] - body_part[1] == 1:
                snake._body_parts_pos.append((body_part[0], body_part[1] - 1))

            elif to_move[1] - body_part[1] == -1:
                snake._body_parts_pos.append((body_part[0], body_part[1] + 1))

    def update_snake_body_size(self, snake):
        snake_body_copy = []
        for body_part in snake._body_parts_pos:
            snake_body_copy.append(body_part)

        for i in range(0, len(snake._body_parts_pos)):
            if i == 0:
                snake._body_parts_pos[0] = snake._past_movement
            else:
                snake._body_parts_pos[i] = snake_body_copy[i - 1]
