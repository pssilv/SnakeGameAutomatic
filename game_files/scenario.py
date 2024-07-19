from graphics import Window
from cell import Cell


class Scenario:
    def __init__(self, rows, cols):
        # Create the window and intializes map size variables
        self._rows = rows
        self._cols = cols
        self._win = Window()

        # Get screen resolution
        self._resolution = self._win.get_display_size()
        self._width = self._resolution[0]
        self._height = self._resolution[1]

        # Optimzed for zoomed resolution
        self._x1 = (self._width * 99.048 / 100) * 1 / 100
        self._x2 = (self._width * 99.048 / 100) * 99 / 100
        self._y1 = (self._height * 91.666 / 100) * 1 / 100
        self._y2 = (self._height * 91.666 / 100) * 99 / 100

        # Build the map and add a listener for closing window
        self.draw_scenario()

    def draw_scenario(self):

        self._total_cells = []

        for cell_col in range(self._cols):

            cell_set = []

            for cell in range(self._rows):
                cell_set.append(Cell(self._win))

            self._total_cells.append(cell_set)

        self._cell_size = ((self._x2 - self._x1) / self._rows)
        self._cell_col_size = ((self._y2 - self._y1) / self._cols)

        y1 = self._y1
        y2 = self._y1 + self._cell_col_size

        self.remove_walls()

        for cell_col in self._total_cells:

            x1, x2 = self._x1, self._x1 + self._cell_size

            for cell in cell_col:
                cell.draw(x1, y1, x2, y2)

                if cell != cell_col[-1]:
                    x1, x2 = x1 + self._cell_size, x2 + self._cell_size

            if cell_col != self._total_cells[-1]:
                y1, y2 = y1 + self._cell_col_size, y2 + self._cell_col_size

    def remove_walls(self):
        for cell_col in self._total_cells:
            for cell in cell_col:
                col_index = self._total_cells.index(cell_col)
                row_index = cell_col.index(cell)

                if col_index == 0:
                    cell.has_bottom_wall = False

                if col_index == self._cols - 1:
                    cell.has_top_wall = False

                if col_index > 0 and col_index < self._cols - 1:
                    cell.has_top_wall = False
                    cell.has_bottom_wall = False

                if row_index == 0:
                    cell.has_right_wall = False

                if row_index == self._rows - 1:
                    cell.has_left_wall = False

                if row_index > 0 and row_index < self._rows - 1:
                    cell.has_left_wall = False
                    cell.has_right_wall = False
