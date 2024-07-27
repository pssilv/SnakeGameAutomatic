from entities import Snake, Fruit
from cell import Cell
import random
# Entities will be listeners too


class EntityManager():
    def __init__(self, rows, cols, snakeQ, fruitG, game_logic):
        # Scenario attributes
        self._rows = rows
        self._cols = cols
        self._scenario = game_logic._scenario

        # Available entities: snake, fruit
        self._id_increaser = 0
        self._total_ids = 0
        self._entities_ids = {}
        self._entities = []
        self._snake_list = []
        self._fruit_list = []

        # Methods to generate positions and add entities
        self._scenario.generate_available_positions()
        self.add_entity(Snake, snakeQ)
        self.add_entity(Fruit, fruitG)

        self.build_entities()
        self.fix_fruit_ids()

        self.display_entities_data()

    def add_entity(self, entity_type, quantity):
        entity_name = type(entity_type(self)).__name__
        self._entities_ids[entity_name] = 0

        for i in range(0, quantity):
            entity = entity_type(self)

            self._id_increaser += 1
            entity._id = self._id_increaser
            self._total_ids += 1

            self._entities.append(entity)

            if isinstance(entity, Fruit):
                self._fruit_list.append(entity)

            elif isinstance(entity, Snake):
                self._snake_list.append(entity)

    def regenerate_fruit(self, fruit):
        self.update_available_positions()

        self._respawn_positions = self._scenario._available_positions

        for fruit_entity in self._fruit_list:
            if fruit_entity._pos in self._respawn_positions:
                self._respawn_positions.remove(fruit_entity._pos)

        fruit._pos = random.choice(self._respawn_positions)

        print(f"fruit {fruit._id} regenerated at {fruit._pos}")

        self.draw_entity(fruit)

    def del_choosed_position(self, position):
        pos = self._scenario._available_positions.index(position)
        del self._scenario._available_positions[pos]

    def update_available_positions(self):
        self._scenario.generate_available_positions()

        for snake in self._snake_list:
            if snake._head_position in self._scenario._available_positions:
                self.del_choosed_position(snake._head_position)

    def draw_entity(self, entity):
        if isinstance(entity, Snake):
            col = entity._head_position[0]
            row = entity._head_position[1]

        elif isinstance(entity, Fruit):
            col = entity._pos[0]
            row = entity._pos[1]

        entity_assigned_cell = self._scenario._total_cells[col][row]
        entity_cell = Cell(self._scenario._win)

        factor_x = self._scenario._cell_size / 8
        factor_y = self._scenario._cell_col_size / 8

        x1 = entity_assigned_cell._x1 + factor_x
        y1 = entity_assigned_cell._y1 + factor_y
        x2 = entity_assigned_cell._x2 - factor_x
        y2 = entity_assigned_cell._y2 - factor_y

        if isinstance(entity, Snake):
            entity_cell.draw(x1, y1, x2, y2)
            entity_cell.generate_color([x1, y1, x2, y2], entity._color)
            entity_cell.draw_eyes(entity._eyes_color, entity._direction)

            entity_cell.has_top_wall = True
            entity_cell.has_bottom_wall = True
            entity_cell.has_right_wall = True
            entity_cell.has_left_wall = True

            self._scenario._win.redraw()

        elif isinstance(entity, Fruit):
            entity_cell.draw_fruit(x1, y1, x2, y2)
            self._scenario._win.redraw()

    def build_entities(self):
        for entity_instance in self._entities:
            entity_name = type(entity_instance).__name__
            self._entities_ids[entity_name] += 1
            id = self._entities_ids[entity_name]

            entity_instance.generate_attributes()

            if isinstance(entity_instance, Snake):
                self.del_choosed_position(entity_instance._head_position)
                position = entity_instance._head_position

            elif isinstance(entity_instance, Fruit):
                self.del_choosed_position(entity_instance._pos)
                position = entity_instance._pos

            self.draw_entity(entity_instance)

            print(f"{entity_name} {id} generated at {position}")

        self._entities = []

    def fix_fruit_ids(self):
        for fruit_id in range(1, self._entities_ids["Fruit"] + 1):
            self._fruit_list[fruit_id - 1]._id = fruit_id

    def display_entities_data(self):
        print("===== Entities data =====")
        for entity_key in self._entities_ids:
            print(f"total {entity_key}s: {self._entities_ids[entity_key]}")

        print(f"Total entities: {self._total_ids}")
        print("-------------------")
