import math
import tkinter as tk
from typing import List
import copy


class Point:
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y

    def __str__(self):
        return f'(x: {self.x}, y: {self.y})'

    def clear(self):
        self.x = -1
        self.y = -1

    def has_point(self) -> bool:
        return self.x != -1 and self.y != -1

    def move_translation(self, x_factor, y_factor):
        self.x += x_factor
        self.y += y_factor

    def rotate(self, angle):
        self.x = round(self.x * math.cos(angle) - self.y * math.sin(angle))
        self.y = round(self.x * math.sin(angle) + self.y * math.cos(angle))

    def x_scale(self, scale):
        self.x = round(self.x * scale)

    def reflect_point_x(self):
        reflected_point = Point(self.x, canvas_size - self.y)
        return reflected_point

    def reflect_point_y(self):
        reflected_point = Point(canvas_size - self.x, self.y)
        return reflected_point


canvas_size = 400


class Window:
    def __init__(self) -> None:
        self.window_coordinates_points = []
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

    def clear(self) -> None:
        self.window_coordinates_points = []
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

    def has_defined_coordinates(self):
        if len(self.window_coordinates_points) == 2:
            return True
        return False

    def define_coordinates(self, point: Point) -> None:
        if len(self.window_coordinates_points) == 0:
            self.window_coordinates_points.append(point)
        elif len(self.window_coordinates_points) == 1:
            self.window_coordinates_points.append(point)
            point1 = self.window_coordinates_points[0]
            point2 = self.window_coordinates_points[1]

            self.x_min = min(point1.x, point2.x)
            self.x_max = max(point1.x, point2.x)
            self.y_min = min(point1.y, point2.y)
            self.y_max = max(point1.y, point2.y)

    def window_coordinates(self):
        return (self.x_min, self.y_min), (self.x_max, self.y_min), (self.x_max, self.y_max), (self.x_min, self.y_max)


class PointSelector:
    def __init__(self, root):

        self.root = root
        self.root.title("Canvas")

        # Define Sliders
        self.x_translation = tk.DoubleVar()
        self.y_translation = tk.DoubleVar()
        self.rotation_angle = tk.DoubleVar()
        self.scale_value = tk.DoubleVar()

        # Define initial window variables
        self.is_defining_window = False
        self.window: Window = Window()

        # Define canvas
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Define initial variables
        self.points: List[Point] = []
        self.initial_point: Point
        self.final_point: Point

        # Slider and Apply Btn for Translation X
        tk.Label(root, text="X Translation").grid(row=1, column=0)
        self.x_slider = tk.Scale(root, variable=self.x_translation, from_=-200, to=200, orient=tk.HORIZONTAL)
        self.x_slider.grid(row=1, column=1)
        self.apply_x_translation_btn = tk.Button(root, text="Apply", command=self.apply_x_translation)
        self.apply_x_translation_btn.grid(row=1, column=2, columnspan=1)

        # Slider Translation Y
        tk.Label(root, text="Y Translation").grid(row=2, column=0)
        self.y_slider = tk.Scale(root, variable=self.y_translation, from_=-200, to=200, orient=tk.HORIZONTAL)
        self.y_slider.grid(row=2, column=1)
        self.apply_y_translation_btn = tk.Button(root, text="Apply", command=self.apply_y_translation)
        self.apply_y_translation_btn.grid(row=2, column=2, columnspan=1)

        # Slider for Rotation
        tk.Label(root, text="Rotation Angle").grid(row=3, column=0)
        self.rotation_slider = tk.Scale(root, variable=self.rotation_angle, from_=-180, to=180, orient=tk.HORIZONTAL)
        self.rotation_slider.grid(row=3, column=1)
        self.apply_rotation_btn = tk.Button(root, text="Apply", command=self.rotate_point)
        self.apply_rotation_btn.grid(row=3, column=2, columnspan=1)

        # Button to reflect x
        self.reflect_x_btn = tk.Button(root, text="Reflect X", command=self.reflect_x)
        self.reflect_x_btn.grid(row=4, column=0, columnspan=1)
        # Button to reflect y
        self.reflect_y_btn = tk.Button(root, text="Reflect Y", command=self.reflect_y)
        self.reflect_y_btn.grid(row=4, column=1, columnspan=1)
        # Button to reflect x y
        self.reflect_xy_btn = tk.Button(root, text="Reflect XY", command=self.reflect_xy)
        self.reflect_xy_btn.grid(row=4, column=2, columnspan=1)

        # Slider for Scale
        tk.Label(root, text="Scale").grid(row=5, column=0)
        self.scale_slider = tk.Scale(root, variable=self.scale_value, from_=-10, to=10, orient=tk.HORIZONTAL)
        self.scale_slider.grid(row=5, column=1)
        self.apply_scale_btn = tk.Button(root, text="Apply", command=self.apply_scale)
        self.apply_scale_btn.grid(row=5, column=2, columnspan=1)

        # Button to clear the line and preserve initial and final point
        self.clear_line_btn = tk.Button(root, text="Clear Line", command=self.clear_line)
        self.clear_line_btn.grid(row=6, column=0, columnspan=2)
        # Button to clear all points
        self.clear_btn = tk.Button(root, text="Clear Canvas", command=self.clear_points)
        self.clear_btn.grid(row=6, column=1, columnspan=2)

        # Apply DDA
        self.apply_dda_btn = tk.Button(root, text="Apply DDA", command=self.apply_DDA)
        self.apply_dda_btn.grid(row=7, column=0, columnspan=1)
        # Apply BRESENHAM
        self.apply_bres_btn = tk.Button(root, text="Apply Bres", command=self.apply_bres)
        self.apply_bres_btn.grid(row=7, column=1, columnspan=1)
        # Apply Circ BRESENHAM
        self.apply_circ_bres_btn = tk.Button(root, text="Apply Circ Bres", command=self.apply_circ_bres)
        self.apply_circ_bres_btn.grid(row=7, column=2, columnspan=1)

        # Button to define window
        self.define_window_button = tk.Button(root, text="Define window", command=self.define_window)
        self.define_window_button.grid(row=8, column=0, columnspan=2)
        # Button to clear window
        self.clear_window_button = tk.Button(root, text="Clear window", command=self.clear_window)
        self.clear_window_button.grid(row=8, column=1, columnspan=2)

        # Apply Cohen-Sutherland
        self.apply_cohen_btn = tk.Button(root, text="Apply Cohen-Sutherland", command=self.apply_cohen)
        self.apply_cohen_btn.grid(row=9, column=0, columnspan=1)
        # Apply Liang-Barsky
        self.apply_liang_btn = tk.Button(root, text="Apply Liang-Barsky", command=self.apply_liang)
        self.apply_liang_btn.grid(row=9, column=1, columnspan=1)

        # User interaction with interface
        self.canvas.bind("<Button-1>", self.on_click)

    # Handle user click on interface
    def on_click(self, event):
        x, y = event.x, event.y

        # Check if user is defining window
        if self.is_defining_window:
            window_point = Point(x, y)
            if len(self.window.window_coordinates_points) == 0:
                self.window.define_coordinates(window_point)
            elif len(self.window.window_coordinates_points) == 1:
                self.is_defining_window = False
                self.window.define_coordinates(window_point)
                self.draw_window_coordinates()

            return

        # Check if canvas is clean
        if len(self.points) >= 2:
            return

        # Check if canvas is waiting for first point to be defined
        if len(self.points) == 0:
            point = Point(x, y)
            self.initial_point = point
            # add initial point in array and plot it
            self.points.append(point)
            self.plot_point(point)

        # Check if canvas is waiting for final point to be defined
        elif len(self.points) == 1:
            point = Point(x, y)
            self.final_point = point
            # add final point in array and plot it
            self.points.append(point)
            self.plot_point(point)

    def draw_window_coordinates(self):
        for coord in self.window.window_coordinates():
            self.plot_point(Point(coord[0], coord[1]), "blue")

    def define_window(self):
        self.is_defining_window = True

    def clear_window(self):
        self.is_defining_window = False
        for coord in self.window.window_coordinates():
            self.remove_point(Point(coord[0], coord[1]))

        self.window.clear()

    def plot_point(self, point: Point, color='red'):
        self.canvas.create_oval(point.x - 5, point.y - 5, point.x + 5, point.y + 5, fill=color)

    def remove_point(self, point: Point):
        item_id = self.canvas.find_closest(point.x, point.y)[0]
        self.canvas.delete(item_id)

    def has_defined_points(self):
        if len(self.points) >= 2:
            return True
        return False

    def clear_points(self):
        self.points = []
        self.initial_point = None
        self.final_point = None
        self.clear_canvas()
        self.window.clear()

    def clear_canvas(self):
        self.canvas.delete("all")

    def clear_line(self):
        if self.has_defined_points():
            self.canvas.delete("all")
            self.points = []
            self.points.append(self.initial_point)
            self.plot_point(self.initial_point)
            self.points.append(self.final_point)
            self.plot_point(self.final_point)

    def print_points(self):
        str_points = "[ "
        for point in self.points:
            str_points += str(point)
            str_points += " "
        str_points += "]"
        print(str_points)

    def apply_x_translation(self):
        if not self.has_defined_points():
            return

        factor = self.x_translation.get()

        print("FACTOR: " + str(factor))
        self.print_points()

        if factor != 0:
            # Clear previous points
            self.clear_canvas()
            for point in self.points:
                point.move_translation(factor, 0)
                self.plot_point(point)

            self.print_points()

    def apply_y_translation(self):
        if not self.has_defined_points():
            return

        factor = self.y_translation.get()

        print("FACTOR: " + str(factor))
        self.print_points()

        if factor != 0:
            # Clear previous points
            self.clear_canvas()
            for point in self.points:
                point.move_translation(0, factor)
                self.plot_point(point)

            self.print_points()

    def rotate_point(self):
        if not self.has_defined_points():
            return

        print('ROTATION:')
        angle = self.rotation_angle.get()

        if angle == 0:
            return

        rot_angle_rad = angle * math.pi / 180.0
        print("ANGLE: " + str(angle))
        print(rot_angle_rad)
        self.print_points()

        # Rotate points
        for point in self.points:
            point.rotate(rot_angle_rad)

        self.clear_canvas()
        for point in self.points:
            self.plot_point(point)

    def reflect_x(self):
        if not self.has_defined_points():
            return

        new_initial_point = self.initial_point.reflect_point_x()
        new_final_point = self.final_point.reflect_point_x()

        self.clear_canvas()
        self.draw_DDA_line(new_initial_point, new_final_point)

    def reflect_y(self):
        if not self.has_defined_points():
            return

        new_initial_point = self.initial_point.reflect_point_y()
        new_final_point = self.final_point.reflect_point_y()

        self.clear_canvas()
        self.draw_DDA_line(new_initial_point, new_final_point)

    def reflect_xy(self):
        if not self.has_defined_points():
            return

        new_initial_point = self.initial_point.reflect_point_x()
        new_final_point = self.final_point.reflect_point_x()

        self.clear_canvas()
        self.draw_DDA_line(new_initial_point.reflect_point_y(), new_final_point.reflect_point_y())

    def apply_scale(self):
        if not self.has_defined_points():
            return

        scale = self.scale_value.get()
        print("SCALE: " + str(scale))
        self.print_points()

        if scale != 0 and scale != 1 and scale != -1:
            new_final_point = copy.copy(self.final_point)
            new_final_point.x_scale(scale if scale > 0 else 1 / -scale)
            self.clear_canvas()

            self.draw_DDA_line(self.initial_point, new_final_point)

    def check_final_point(self):
        if self.final_point.x == self.points[len(self.points) - 1].x:
            print("ok x")
        else:
            print("quase")
            print(self.final_point.x)
            print(self.points[len(self.points) - 1].x)
        if self.final_point.y == self.points[len(self.points) - 1].y:
            print("ok y")
        else:
            print("quase")
            print(self.final_point.y)
            print(self.points[len(self.points) - 1].y)

    def draw_DDA_line(self, point1, point2):
        dx = point2.x - point1.x
        dy = point2.y - point1.y

        steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

        x_increment = dx / steps
        y_increment = dy / steps

        self.points = []

        x = point1.x
        y = point1.y

        point = Point(x, y)
        self.plot_point(point)
        self.points.append(point)

        for step in range(1, steps + 1):
            x += x_increment
            y += y_increment
            next_point = Point(round(x), round(y))
            self.plot_point(next_point)
            self.points.append(next_point)

    def apply_DDA(self):
        if not self.has_defined_points():
            return

        self.clear_canvas()
        self.draw_DDA_line(self.initial_point, self.final_point)

        print("DDA:")
        self.check_final_point()

    def apply_bres(self):
        if not self.has_defined_points():
            return

        dx = self.final_point.x - self.initial_point.x
        dy = self.final_point.y - self.initial_point.y

        if dx >= 0:
            x_increment = 1
        else:
            x_increment = -1
            dx = -dx

        if dy >= 0:
            y_increment = 1
        else:
            y_increment = -1
            dy = -dy

        self.clear_canvas()
        self.points = []

        x = self.initial_point.x
        y = self.initial_point.y

        point = Point(x, y)
        self.plot_point(point)
        self.points.append(point)

        if dx > dy:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)
            for i in range(dx):
                x += x_increment
                if p < 0:
                    p += const1
                else:
                    y += y_increment
                    p += const2
                new_point = Point(x, y)
                self.points.append(new_point)
                self.plot_point(new_point)
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)
            for i in range(dy):
                y += y_increment
                if p < 0:
                    p += const1
                else:
                    x += x_increment
                    p += const2
                new_point = Point(x, y)
                self.points.append(new_point)
                self.plot_point(new_point)

        print("BRESENHAM:")
        self.check_final_point()

    def plot_circular_point(self, point, x, y):
        self.plot_point(Point(point.x + x, point.y + y))
        self.points.append(Point(point.x + x, point.y + y))
        self.plot_point(Point(point.x - x, point.y + y))
        self.points.append(Point(point.x - x, point.y + y))
        self.plot_point(Point(point.x + x, point.y - y))
        self.points.append(Point(point.x + x, point.y - y))
        self.plot_point(Point(point.x - x, point.y - y))
        self.points.append(Point(point.x - x, point.y - y))

        self.plot_point(Point(point.x + y, point.y + x))
        self.points.append(Point(point.x + y, point.y + x))
        self.plot_point(Point(point.x - y, point.y + x))
        self.points.append(Point(point.x - y, point.y + x))
        self.plot_point(Point(point.x + y, point.y - x))
        self.points.append(Point(point.x + y, point.y - x))
        self.plot_point(Point(point.x - y, point.y - x))
        self.points.append(Point(point.x - y, point.y - x))

    def apply_circ_bres(self):
        if not self.has_defined_points():
            return

        radius = (
            int(round(math.sqrt(
                (self.final_point.x - self.initial_point.x) ** 2 + (self.final_point.y - self.initial_point.y) ** 2)
            )))

        x = 0
        y = radius
        d = 3 - 2 * radius

        self.points = []
        self.clear_canvas()
        self.plot_circular_point(self.initial_point, x, y)

        while y >= x:
            x += 1
            if d > 0:
                y += -1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            self.plot_circular_point(self.initial_point, x, y)

    def apply_cohen(self):
        if not self.has_defined_points():
            return
        if not self.window.has_defined_coordinates():
            return

        def region_code(point: Point):
            code = 0
            # Left bit 0
            if point.x < self.window.x_min:
                code = code + 1
            # Right bit 1
            if point.x > self.window.x_max:
                code = code + 2
            # Bottom bit 2
            if point.y < self.window.y_min:
                code = code + 4
            # Top bit 3
            if point.y > self.window.y_max:
                code = code + 8
            return code

        def cohen_sutherland_clip(point1: Point, point2: Point):
            c1 = region_code(point1)
            c2 = region_code(point2)

            while True:
                # Both points are inside
                if not (c1 | c2):
                    return point1, point2
                # Both points are outside
                elif c1 & c2:
                    return None, None
                # At least one point is outside
                else:
                    if c1:
                        outcode_checking = c1
                    else:
                        outcode_checking = c2

                    # Find the intersection point
                    if outcode_checking & 8:  # Top
                        x = point1.x + (point2.x - point1.x) * (self.window.y_max - point1.y) / (point2.y - point1.y)
                        y = self.window.y_max
                    elif outcode_checking & 4:  # Bottom
                        x = point1.x + (point2.x - point1.x) * (self.window.y_min - point1.y) / (point2.y - point1.y)
                        y = self.window.y_min
                    elif outcode_checking & 2:  # Right
                        y = point1.y + (point2.y - point1.y) * (self.window.x_max - point1.x) / (point2.x - point1.x)
                        x = self.window.x_max
                    else:  # Left
                        y = point1.y + (point2.y - point1.y) * (self.window.x_min - point1.x) / (point2.x - point1.x)
                        x = self.window.x_min

                    final_point = Point(round(x), round(y))
                    # Update the point outside the window
                    if outcode_checking == c1:
                        point1 = final_point
                        c1 = region_code(point1)
                    else:
                        point2 = final_point
                        c2 = region_code(point2)

        print("COHEN SUTHERLAND")
        print(self.window.window_coordinates())
        print("Before")
        print(str(self.initial_point), str(self.final_point))
        res = cohen_sutherland_clip(point1=self.initial_point, point2=self.final_point)
        print("After")
        print(res[0], res[1])

        self.clear_canvas()
        self.draw_window_coordinates()

        if res[0] is not None:
            self.draw_DDA_line(res[0], res[1])

        print("done")

    def apply_liang(self):
        if not self.has_defined_points():
            return
        if not self.window.has_defined_coordinates():
            return

        def cliptest(p, q, u1, u2):
            result = True
            if p < 0:
                r = q / p
                if r > u2:
                    result = False
                elif r > u1:
                    u1 = r
            elif p > 0:
                r = q / p
                if r < u1:
                    result = False
                elif r < u2:
                    u2 = r
            elif q < 0:
                result = False
            return result, u1, u2

        def liang_barsky_line_clip(point1, point2):
            dx = point2.x - point1.x
            dy = point2.y - point1.y

            u1, u2 = 0, 1

            ans, u1, u2 = cliptest(-dx, point1.x - self.window.x_min, u1, u2)
            if ans:
                ans, u1, u2 = cliptest(dx, self.window.x_max - point1.x, u1, u2)
                if ans:
                    ans, u1, u2 = cliptest(-dy, point1.y - self.window.y_min, u1, u2)
                    if ans:
                        ans, u1, u2 = cliptest(dy, self.window.y_max - point1.y, u1, u2)
                        if ans:
                            new_point1 = Point(point1.x, point1.y)
                            new_point2 = Point(point2.x, point2.y)
                            if u2 < 1:
                                new_point2.x = round(point1.x + u2 * dx)
                                new_point2.y = round(point1.y + u2 * dy)
                            if u1 > 0:
                                new_point1.x = round(point1.x + u1 * dx)
                                new_point1.y = round(point1.y + u1 * dy)

                            return new_point1, new_point2

            return None, None

        print("LIANG BARSKY")
        print(self.window.window_coordinates())
        print("Before")
        print(str(self.initial_point), str(self.final_point))
        res = liang_barsky_line_clip(point1=self.initial_point, point2=self.final_point)
        print("After")
        print(res[0], res[1])

        self.clear_canvas()
        self.draw_window_coordinates()

        if res[0] is not None:
            self.draw_DDA_line(res[0], res[1])

        print("done")


if __name__ == "__main__":
    root = tk.Tk()
    point_selector = PointSelector(root)
    root.mainloop()
