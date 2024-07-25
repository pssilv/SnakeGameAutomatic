from scenario import Scenario
from entitymanager import EntityManager
from entities import Snake, Fruit
import time
import random


class SnakeGame():
    def __init__(self, rows, cols, snakeQ, fruitG):
        self._scenario = Scenario(rows, cols)
        self.entitymanager = EntityManager(rows, cols, snakeQ, fruitG, self)

        self.set_fruit_list()
        self.set_snake_list()
        self.calculate_path_to_fruit()

        self._scenario._win.wait_for_close()

    # You need to define the list attribute inside method or else the window will close
    def set_fruit_list(self):
        self._fruit_list = []

        for entity in self.entitymanager._entities:
            if isinstance(entity, Fruit):
                self._fruit_list.append(entity)

    def set_snake_list(self):
        self._snake_list = []

        # structure: self.snake_pos_list = {"snake 1": {"head_pos": (0, 0), "body_parts_pos": [1,1, 1,2]} }
        for entity in self.entitymanager._entities:
            if isinstance(entity, Snake):
                self._snake_list.append(entity)

    def find_the_nearest_fruit(self):

        for snake in self._snake_list:
            closest_fruit_y = float("inf")
            closest_fruit_x = float("inf")

            for fruit in self._fruit_list:
                fruit_dist_y = abs(snake._head_position[0] - fruit._pos[0])
                fruit_dist_x = abs(snake._head_position[1] - fruit._pos[1])

                total_fruit_dist = closest_fruit_y + closest_fruit_x

                if (fruit_dist_y + fruit_dist_x) < total_fruit_dist:
                    print(f"Fruit {fruit._id}")
                    closest_fruit_y = fruit_dist_y
                    closest_fruit_x = fruit_dist_x
                    fruit_index = self._fruit_list.index(fruit)

            print(f"Snake {snake._id}")
            yield snake, self._fruit_list[fruit_index]

    def calculate_path_to_fruit(self):
        for snake_and_fruit in self.find_the_nearest_fruit():
            snake, fruit = snake_and_fruit[0], snake_and_fruit[1]

            fruit_pos_y = fruit._pos[0]
            fruit_pos_x = fruit._pos[1]

            while snake._head_position[0] != fruit_pos_y or snake._head_position[1] != fruit_pos_x:

                self.detect_others_snakes(snake)
                self.calculate_available_paths(snake, fruit)

                print(f"Actual position: {snake._head_position[0], snake._head_position[1]}")

                snake._past_movement = (snake._head_position[0], snake._head_position[1])
                print(f"Past movement: {snake._past_movement}")

                if len(snake._available_paths) > 0:
                    snake._path_to_fruit.append(snake._available_paths[0])
                    self.get_direction(snake)
                    self.move_snake_to_fruit(snake)
                else:
                    print("Snaked died!")
                    break

    def move_snake_to_fruit(self, snake):
        self.delete_snake_old_pos(snake)

        snake._head_position = snake._path_to_fruit.pop(0)
        print(f"Head position: {snake._head_position}")

        self.entitymanager.draw_entity(snake)
        time.sleep(0.25)

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

    def detect_others_snakes(self, snake):
        self._occupied_positions = []

        for other_snake in self._snake_list:
            if other_snake._id != snake._id:
                self._occupied_positions.append(other_snake._head_position)

        print(f"Occupied positions: {self._occupied_positions}")

    def calculate_available_paths(self, snake, fruit):
        next_move_y = self.update_next_move(snake._head_position[0], fruit._pos[0])
        next_move_x = self.update_next_move(snake._head_position[1], fruit._pos[1])

        head_pos_y = snake._head_position[0]
        head_pos_x = snake._head_position[1]

        scenario_limits_y = [-1, len(self._scenario._total_cells)]
        scenario_limits_x = [-1, len(self._scenario._total_cells[0])]

        moves = []
        snake._available_paths = []

        if (head_pos_y + 1, head_pos_x) not in self._occupied_positions:
            moves.append( (head_pos_y + 1, head_pos_x) )

        if (head_pos_y - 1, head_pos_x) not in self._occupied_positions:
            moves.append( (head_pos_y - 1, head_pos_x) )

        if (head_pos_y, head_pos_x + 1) not in self._occupied_positions:
            moves.append( (head_pos_y, head_pos_x + 1) )

        if (head_pos_y, head_pos_x - 1) not in self._occupied_positions:
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

        for path in snake._available_paths:
            path_index = snake._available_paths.index(path)

            limit_y_passed = False
            limit_x_passed = False

            if path[0] <= scenario_limits_y[0] or path[0] >= scenario_limits_y[1]:
                limit_y_passed = True

            if path[1] <= scenario_limits_x[0] or path[1] >= scenario_limits_x[1]:
                limit_x_passed = True

            if limit_y_passed or limit_x_passed:
                del snake._available_paths[path_index]

        print(f"Available paths: {snake._available_paths}")

    def update_next_move(self, head_pos, fruit_pos):
        if head_pos != fruit_pos:
            delta = fruit_pos - head_pos

            if delta > 0:
                return 1
            elif delta < 0:
                return -1
        return 0

    def get_direction(self, snake):
        next_move = snake._available_paths[0]
        head_pos = snake._head_position
        if (next_move[0] - head_pos[0]) == 1:
            snake._direction = "down"

        elif (next_move[1] - head_pos[1]) == 1:
            snake._direction = "right"

        elif (next_move[0] - head_pos[0]) == -1:
            snake._direction = "up"

        elif (next_move[1] - head_pos[1]) == -1:
            snake._direction = "left"
