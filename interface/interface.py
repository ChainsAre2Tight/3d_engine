from tkinter import *
from tkinter import ttk
from internals.render import Renderer
from internals.vectors import Vector, Quaternion, rotate_vector_by_quaternion
import internals.handlers
import math


class Window:
    fov = math.pi / 2
    aspect_ratio = 1
    camera_position = Vector(0, 0, -5)
    screen_height = 800
    camera_angle = Quaternion.from_euler(0, (0, 1, 0))
    move_magnitude = 0.5
    rotate_magnitude = math.radians(10)

    def __init__(self):

        # setup window
        self.root = Tk()
        self.root.title("Вывод")
        self.root.resizable(False, False)
        self.root.geometry(f'{int(self.screen_height * self.aspect_ratio)}x{self.screen_height + 100}')

        # initialize handlers
        self.data_handler = internals.handlers.DataHandler()
        self.data_handler.read_file(file_path="../data", file_name="triangulated_cube.obj")

        # initialize and place widgets
        self.canvas = Canvas(self.root, width=int(self.aspect_ratio * self.screen_height), height=self.screen_height,
                             bg='white')
        self.canvas.pack()

        self.rotate_button_frame = Frame(self.root)
        self.rotate_button_frame.pack(side="left")
        self.rotate_center_frame = Frame(self.rotate_button_frame)
        self.rotate_right_frame = Frame(self.rotate_button_frame)
        self.refresh_button = ttk.Button(self.rotate_center_frame, text="Обновить", command=self.refresh)
        self.rotate_x_plus_button = ttk.Button(self.rotate_right_frame, text="+y", command=self.rotate_y_plus)
        self.rotate_x_minus_button = ttk.Button(self.rotate_button_frame, text="-y", command=self.rotate_y_minus)
        self.rotate_x_minus_button.pack(side="left")
        self.rotate_y_minus_button = ttk.Button(self.rotate_center_frame, text="+x", command=self.rotate_x_plus)
        self.rotate_y_minus_button.pack(side="top")
        self.rotate_y_minus_button = ttk.Button(self.rotate_center_frame, text="-x", command=self.rotate_x_minus)
        self.rotate_y_minus_button.pack(side="bottom")
        self.rotate_z_minus_button = ttk.Button(self.rotate_right_frame, text="+z", command=self.rotate_z_plus)
        self.rotate_z_minus_button.pack(side="top")
        self.rotate_x_plus_button.pack(side="top")
        self.rotate_z_minus_button = ttk.Button(self.rotate_right_frame, text="-z", command=self.rotate_z_minus)
        self.rotate_z_minus_button.pack(side="bottom")
        self.rotate_right_frame.pack(side="right")
        self.rotate_center_frame.pack()
        self.refresh_button.pack()

        self.move_button_frame = Frame(self.root)
        self.move_button_frame.pack(side="right")
        self.move_center_frame = Frame(self.move_button_frame)
        self.move_right_frame = Frame(self.move_button_frame)
        self.lox_button = ttk.Button(self.move_center_frame, text="", command="")
        self.move_x_plus_button = ttk.Button(self.move_right_frame, text="d", command=self.move_right)
        self.move_x_minus_button = ttk.Button(self.move_button_frame, text="a", command=self.move_left)
        self.move_x_minus_button.pack(side="left")
        self.move_y_plus_button = ttk.Button(self.move_center_frame, text="w", command=self.move_forward)
        self.move_y_plus_button.pack(side="top")
        self.move_y_minus_button = ttk.Button(self.move_center_frame, text="s", command=self.move_backward)
        self.move_y_minus_button.pack(side="bottom")
        self.move_z_minus_button = ttk.Button(self.move_right_frame, text="+z", command=self.move_up)
        self.move_z_minus_button.pack(side="top")
        self.move_x_plus_button.pack(side="top")
        self.move_z_minus_button = ttk.Button(self.move_right_frame, text="-z", command=self.move_down)
        self.move_z_minus_button.pack(side="bottom")
        self.move_right_frame.pack(side="right")
        self.move_center_frame.pack()
        self.lox_button.pack()

        self.refresh()

    def refresh(self):
        self.canvas.delete("all")

        renderer = Renderer(
            data_handler=self.data_handler,
            fov=self.fov,
            aspect_ratio=self.aspect_ratio,
            camera_position=self.camera_position,
            screen_height=self.screen_height,
            camera_angle=self.camera_angle
        )

        list_of_polygons = renderer.render_polygons()

        for polygon in list_of_polygons:
            self.canvas.create_polygon(polygon.to_tuple(), fill=polygon.color)

        list_of_lines = renderer.render_lines()

        for line in list_of_lines:
            self.canvas.create_line(line.to_tuple(), fill=line.color, width=2)

    def rotate_y_plus(self):
        self.camera_angle = Quaternion.from_euler(self.rotate_magnitude, (0, -1, 0)) * self.camera_angle
        self.refresh()

    def rotate_y_minus(self):
        self.camera_angle = Quaternion.from_euler(self.rotate_magnitude, (0, 1, 0)) * self.camera_angle
        self.refresh()

    def rotate_x_plus(self):
        self.camera_angle = Quaternion.from_euler(self.rotate_magnitude, (-1, 0, 0)) * self.camera_angle
        self.refresh()

    def rotate_x_minus(self):
        self.camera_angle = Quaternion.from_euler(self.rotate_magnitude, (1, 0, 0)) * self.camera_angle
        self.refresh()

    def rotate_z_plus(self):
        self.camera_angle = Quaternion.from_euler(self.rotate_magnitude, (0, 0, -1)) * self.camera_angle
        self.refresh()

    def rotate_z_minus(self):
        self.camera_angle = Quaternion.from_euler(math.radians(5), (0, 0, 1)) * self.camera_angle
        self.refresh()

    def move_right(self):
        self.camera_position += internals.vectors.rotate_vector_by_quaternion(
            internals.vectors.Vector(1, 0, 0) * self.move_magnitude, self.camera_angle.invert())
        self.refresh()

    def move_left(self):
        self.camera_position += internals.vectors.rotate_vector_by_quaternion(
            internals.vectors.Vector(-1, 0, 0) * self.move_magnitude, self.camera_angle.invert())
        self.refresh()

    def move_up(self):
        self.camera_position += internals.vectors.rotate_vector_by_quaternion(
            internals.vectors.Vector(0, -1, 0) * self.move_magnitude, self.camera_angle.invert())
        self.refresh()

    def move_down(self):
        self.camera_position += internals.vectors.rotate_vector_by_quaternion(
            internals.vectors.Vector(0, 1, 0) * self.move_magnitude, self.camera_angle.invert())
        self.refresh()

    def move_forward(self):
        self.camera_position += internals.vectors.rotate_vector_by_quaternion(
            internals.vectors.Vector(0, 0, 1) * self.move_magnitude, self.camera_angle.invert())
        self.refresh()

    def move_backward(self):
        self.camera_position += internals.vectors.rotate_vector_by_quaternion(
            internals.vectors.Vector(0, 0, -1) * self.move_magnitude, self.camera_angle.invert())
        self.refresh()


if __name__ == "__main__":
    window = Window()
    window.root.mainloop()
