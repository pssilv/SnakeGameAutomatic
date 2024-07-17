from scenario import Scenario
from entitymanager import EntityManager
from entities import Snake, Fruit


class SnakeGame():
    def __init__(self, rows, cols, snakeQ, fruitG):
        self._scenario = Scenario(rows, cols)
        self.entitymanager = EntityManager(rows, cols, snakeQ, fruitG, self)

        self.update_fruit_pos_list()
        print(self.fruit_pos_list)
        self.set_snake_pos_list()
        self.update_snake_pos_list()
        print(self.snake_pos_list)

    # You need to define the list attribute inside method or else the window will close
    def update_fruit_pos_list(self):
        self.fruit_pos_list = []

        for entity in self.entitymanager._entities:
            if isinstance(entity, Fruit):
                self.fruit_pos_list.append(entity._pos)

    def set_snake_pos_list(self):
        self.snake_pos_list = {}

        # structure: self.snake_pos_list = {"snake 1": {"head_pos": (0, 0), "body_parts_pos": [1,1, 1,2]} }
        for entity in self.entitymanager._entities:
            if isinstance(entity, Snake):
                self.snake_pos_list["snake " + str(entity._id)] = {"head_pos": None, "body_parts_pos": []}

    def update_snake_pos_list(self):
        for entity in self.entitymanager._entities:
            if isinstance(entity, Snake):
                self.snake_pos_list["snake " + str(entity._id)]["head_pos"] = entity._head_position
                #  placeholder
                self.snake_pos_list["snake " + str(entity._id)]["body_parts_pos"].append( (0, 0) )

        self._scenario._win.wait_for_close()
