from graphics import Line, Point


class Cell:
    def __init__(self, win):
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self.has_top_wall = True
        self._has_collision = False
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        if self.has_right_wall:

            self._win.draw_line(Line(
                Point(self._x2, self._y1), Point(self._x2, self._y2))
            )

        if self.has_bottom_wall:

            self._win.draw_line(Line(
                Point(self._x1, self._y2), Point(self._x2, self._y2))
            )

        if self.has_left_wall:

            self._win.draw_line(Line(
                Point(self._x1, self._y1), Point(self._x1, self._y2))
            )

        if self.has_top_wall:

            self._win.draw_line(Line(
                Point(self._x1, self._y1), Point(self._x2, self._y1))
            )

    def generate_color(self, points, color):
        x1, y1, x2, y2 = points[0], points[1], points[2], points[3]

        self._win.generate_polygon_color(
            [x1, y1, x2, y1,
             x2, y1, x2, y2,
             x2, y2, x1, y2,
             x1, y2, x1, y1,
             ],
            color
        )

    def draw_eyes(self, eye_color):
        delta_x = self._x2 - self._x1
        delta_y = self._y2 - self._y1

        left_eye_x = self._x1 + delta_x / 3
        left_eye_y = self._y1 + delta_y / 3

        right_eye_x = self._x2 - delta_x / 3
        right_eye_y = self._y1 + delta_y / 3

        self._win.draw_line(Line(
            Point(left_eye_x, left_eye_y), Point(self._x1, left_eye_y))
        )

        self._win.draw_line(Line(
            Point(left_eye_x, left_eye_y), Point(left_eye_x, self._y1))
        )

        self._win.draw_line(Line(
            Point(right_eye_x, right_eye_y), Point(self._x2, right_eye_y))
        )

        self._win.draw_line(Line(
            Point(right_eye_x, right_eye_y), Point(right_eye_x, self._y1))
        )

        # Left eye
        self.generate_color([self._x1, self._y1, left_eye_x, left_eye_y],
                            eye_color)
        # Right eye
        self.generate_color([self._x2, self._y1, right_eye_x, right_eye_y],
                            eye_color)
