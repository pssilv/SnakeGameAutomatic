from scenario import Scenario
from entitymanager import EntityManager
from entities import Snake, Fruit


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

            snake_pos_y = snake._head_position[0]
            snake_pos_x = snake._head_position[1]
            fruit_pos_y = fruit._pos[0]
            fruit_pos_x = fruit._pos[1]

            diff_y = fruit_pos_y - snake_pos_y
            diff_x = fruit_pos_x - snake_pos_x

            movements_y = []
            movements_x = []

            if diff_y < 0:
                for actual_y_pos in range(snake_pos_y, fruit_pos_y, -1):
                    movements_y.append(-1)
            else:
                for actual_y_pos in range(snake_pos_y, fruit_pos_y):
                    movements_y.append(1)

            if diff_x < 0:
                for actual_x_pos in range(snake_pos_x, fruit_pos_x, -1):
                    movements_x.append(-1)
            else:
                for actual_x_pos in range(snake_pos_x, fruit_pos_x):
                    movements_x.append(1)

            current_location_y = snake._head_position[0]
            current_location_x = snake._head_position[1]

            while current_location_y != fruit_pos_y or current_location_x != fruit_pos_x:
                if len(movements_y) > 0:
                    current_location_y += movements_y.pop(0)
                    snake._path_to_fruit.append( (current_location_y, current_location_x) )

                if len(movements_x) > 0:
                    current_location_x += movements_x.pop(0)
                    snake._path_to_fruit.append( (current_location_y, current_location_x) )

            print(snake._path_to_fruit)
