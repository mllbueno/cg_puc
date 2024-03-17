import math
import tkinter as tk
from typing import List
import copy


class Point:
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

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
        self.x *= scale


canvas_size = 400


class PointSelector:
    def __init__(self, root):

        self.root = root
        self.root.title("Canvas")

        # Define Sliders
        self.x_translation = tk.DoubleVar()
        self.y_translation = tk.DoubleVar()
        self.rotation_angle = tk.DoubleVar()
        self.scale_value = tk.DoubleVar()

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

        # Slider for Scale
        tk.Label(root, text="Scale").grid(row=4, column=0)
        self.scale_slider = tk.Scale(root, variable=self.scale_value, from_=-10, to=10, orient=tk.HORIZONTAL)
        self.scale_slider.grid(row=4, column=1)
        self.apply_scale_btn = tk.Button(root, text="Apply", command=self.apply_scale)
        self.apply_scale_btn.grid(row=4, column=2, columnspan=1)

        # Button to clear the line and preserve initial and final point
        self.clear_line = tk.Button(root, text="Clear Line", command=self.clear_line)
        self.clear_line.grid(row=6, column=0, columnspan=2)
        # Button to clear all points
        self.clear_button = tk.Button(root, text="Clear Canvas", command=self.clear_points)
        self.clear_button.grid(row=6, column=1, columnspan=2)

        # Apply DDA
        self.apply_dda_btn = tk.Button(root, text="Apply DDA", command=self.apply_DDA)
        self.apply_dda_btn.grid(row=7, column=0, columnspan=2)
        # Apply DDA
        self.apply_bres_btn = tk.Button(root, text="Apply Bres", command=self.apply_bres)
        self.apply_bres_btn.grid(row=7, column=1, columnspan=2)

        # User interaction with interface
        self.canvas.bind("<Button-1>", self.on_click)

    # Handle user click on interface
    def on_click(self, event):
        x, y = event.x, event.y

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

    def plot_point(self, point: Point, color='red'):
        self.canvas.create_oval(point.x - 5, point.y - 5, point.x + 5, point.y + 5, fill=color)

    def has_defined_points(self):
        if len(self.points) >= 2:
            return True
        return False

    def clear_points(self):
        self.points = []
        self.initial_point = None
        self.final_point = None
        self.clear_canvas()

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
        def translate_to_origin(polygon):
            centroid_x = sum(vertex.x for vertex in polygon) / len(polygon)
            centroid_y = sum(vertex.y for vertex in polygon) / len(polygon)

            translated_polygon = [Point(vertex.x - centroid_x, vertex.y - centroid_y) for vertex in polygon]

            return translated_polygon, (centroid_x, centroid_y)

        def rollback_translation(polygon, centroid_val):
            # Rollback translation
            rolled_back_polygon = [Point(vertex.x + centroid_val[0], vertex.y + centroid_val[1]) for vertex in polygon]

            return rolled_back_polygon

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

        # Translate to origin
        new_points, centroid = translate_to_origin(copy.copy(self.points))

        # Rotate points
        for point in new_points:
            point.rotate(rot_angle_rad)

        # Return to correct position
        self.points = rollback_translation(new_points, centroid)

        self.clear_canvas()
        for point in self.points:
            self.plot_point(point)

    def apply_scale(self):
        if not self.has_defined_points():
            return

        scale = self.scale_value.get()
        print("SCALE: " + str(scale))
        self.print_points()

        if scale != 0 and scale != 1 and scale != -1:
            self.clear_canvas()
            for point in self.points:
                point.x_scale(scale if scale > 0 else 1/-scale)
                self.plot_point(point)

            self.print_points()

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

    def apply_DDA(self):
        if not self.has_defined_points():
            return

        dx = self.final_point.x - self.initial_point.x
        dy = self.final_point.y - self.initial_point.y

        steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

        x_increment = dx / steps
        y_increment = dy / steps

        self.clear_canvas()
        self.points = []

        x = self.initial_point.x
        y = self.initial_point.y

        point = Point(x, y)
        self.plot_point(point)
        self.points.append(point)

        for step in range(1, steps+1):
            x += x_increment
            y += y_increment
            next_point = Point(round(x), round(y))
            self.plot_point(next_point)
            self.points.append(next_point)

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


if __name__ == "__main__":
    root = tk.Tk()
    point_selector = PointSelector(root)
    root.mainloop()
