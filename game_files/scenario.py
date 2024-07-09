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
        self._x1 = (self._width * 99.048 / 100) * 5 / 100
        self._x2 = (self._width * 99.048 / 100) * 95 / 100
        self._y1 = (self._height * 91.666 / 100) * 5 / 100
        self._y2 = (self._height * 91.666 / 100) * 95 / 100

        # Build the map and add a listener for closing window
        self.build()

    def build(self):
        self._area = Cell(self._win)
        self._area.draw(self._x1, self._y1, self._x2, self._y2)

        self.set_hitboxes()

    def set_hitboxes(self):

        self._total_cells = []

        for cell_col in range(self._cols):

            cell_set = []

            for cell in range(self._rows):
                cell_set.append(Cell(self._win))
                self._win.redraw()

            self._total_cells.append(cell_set)

        self.remove_walls()

        cell_size = ((self._x2 - self._x1) / self._rows)
        cell_col_size = ((self._y2 - self._y1) / self._cols)

        y1 = self._y1
        y2 = self._y1 + cell_col_size

        for cell_col in self._total_cells:

            x1, x2 = self._x1, self._x1 + cell_size

            for cell in cell_col:
                cell.draw(x1, y1, x2, y2)

                if cell != cell_col[-1]:
                    x1, x2 = x1 + cell_size, x2 + cell_size

            if cell_col != self._total_cells[-1]:
                y1, y2 = y1 + cell_col_size, y2 + cell_col_size

    def remove_walls(self):
        for cell_col in self._total_cells:
            for cell in cell_col:
                cell.has_right_wall = False
                cell.has_left_wall = False
                cell.has_bottom_wall = False
                cell.has_top_wall = False
