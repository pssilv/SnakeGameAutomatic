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
        self.snake_polygon = {"head": None, "body": [],
                              "left_eye": None, "right_eye": None}
        self.fruit_polygon = {"fruit": None}

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

    def draw_eyes(self, x1, y1, x2, y2, eye_color, direction):
        delta_x = x2 - x1
        delta_y = y2 - y1

        if direction == "up":
            left_eye_x = x1 + delta_x / 3
            left_eye_y = y1 + delta_y / 3

            right_eye_x = x1 + delta_x / 3 * 2
            right_eye_y = y1 + delta_y / 3

            # Left eye
            self.snake_polygon["left_eye"] = (
                self._win.draw_rectangle(x1, y1, left_eye_x, left_eye_y,
                                         eye_color)
            )
            # Right eye
            self.snake_polygon["right_eye"] = (
                self._win.draw_rectangle(right_eye_x, y1, x2, right_eye_y,
                                         eye_color)
            )

        elif direction == "down":
            left_eye_x = x1 + delta_x / 3
            left_eye_y = y1 + delta_y / 3 * 2

            right_eye_x = x1 + delta_x / 3 * 2
            right_eye_y = y1 + delta_y / 3 * 2
            # Left eye
            self.snake_polygon["left_eye"] = (
                self._win.draw_rectangle(x1, left_eye_y, left_eye_x, y2,
                                         eye_color)
            )
            # Right eye
            self.snake_polygon["right_eye"] = (
                self._win.draw_rectangle(right_eye_x, right_eye_y, x2, y2,
                                         eye_color)
            )

        elif direction == "right":
            left_eye_x = x1 + delta_x / 3 * 2
            left_eye_y = y1 + delta_y / 3

            right_eye_x = x1 + delta_x / 3 * 2
            right_eye_y = y1 + delta_y / 3 * 2

            # Left eye
            self.snake_polygon["left_eye"] = (
                self._win.draw_rectangle(left_eye_x, y1, x2, left_eye_y,
                                         eye_color)
            )
            # Right eye
            self.snake_polygon["right_eye"] = (
                self._win.draw_rectangle(right_eye_x, right_eye_y, x2, y2,
                                         eye_color)
            )

        elif direction == "left":
            left_eye_x = x1 + delta_x / 3
            left_eye_y = y1 + delta_y / 3 * 2

            right_eye_x = x1 + delta_x / 3
            right_eye_y = y1 + delta_y / 3

            # Left eye
            self.snake_polygon["left_eye"] = (
                self._win.draw_rectangle(x1, left_eye_y, left_eye_x, y2,
                                         eye_color)
            )
            # Right eye
            self.snake_polygon["right_eye"] = (
                self._win.draw_rectangle(x1, y1, right_eye_x, right_eye_y,
                                         eye_color)
            )

    def draw_fruit(self, x1, y1, x2, y2, fruit):
        self.fruit_polygon["fruit"] = (
            self._win.draw_oval(x1, y1, x2, y2, "white")
        )

        fruit._past_polygons = self.fruit_polygon

    def draw_snake_head(self, x1, y1, x2, y2, snake):
        self.snake_polygon["head"] = (
                self._win.draw_rectangle(x1, y1, x2, y2, snake._color)
        )
        self.draw_eyes(x1, y1, x2, y2, snake._eyes_color, snake._direction)

        snake._past_polygons = self.snake_polygon

    def draw_snake_body(self, x1, y1, x2, y2, snake):
        self.snake_polygon["body"].append(
            self._win.draw_rectangle(x1, y1, x2, y2, snake._color)
        )

        snake._past_polygons["body"] = self.snake_polygon["body"]
