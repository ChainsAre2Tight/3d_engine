from tkinter import *
from tkinter import ttk
from internals.render import get_polygons, get_lines
from internals.quaternions import Vector, Quaternion, rotate_vector_by_quaternion
import math


class Window:
    fov = math.pi / 5
    aspect_ratio = 1
    camera_position = Vector(0, 0, -320)
    screen_height = 512
    camera_angle = Quaternion.from_euler(0, (0, 1, 0, 0))

    def __init__(self):
        self.root = Tk()
        self.root.title("Вывод")
        self.root.resizable(False, False)
        self.root.geometry(f'{int(self.screen_height * self.aspect_ratio)}x{self.screen_height + 100}')

        self.canvas = Canvas(self.root, width=int(self.aspect_ratio * self.screen_height), height=self.screen_height,
                             bg='white')
        self.canvas.pack()

        self.button_frame = Frame(self.root)
        self.button_frame.pack()

        self.center_frame = Frame(self.button_frame)


        self.refresh_button = ttk.Button(self.center_frame, text="Обновить", command=self.refresh)


        self.rotate_x_plus_button = ttk.Button(self.button_frame, text="right", command=self.rotate_x_plus)
        self.rotate_x_plus_button.pack(side="right")

        self.rotate_x_minus_button = ttk.Button(self.button_frame, text="left", command=self.rotate_x_minus)
        self.rotate_x_minus_button.pack(side="left")

        self.rotate_y_minus_button = ttk.Button(self.center_frame, text="up", command=self.rotate_y_plus)
        self.rotate_y_minus_button.pack(side="top")

        self.rotate_y_minus_button = ttk.Button(self.center_frame, text="down", command=self.rotate_y_minus)
        self.rotate_y_minus_button.pack(side="bottom")

        self.center_frame.pack()
        self.refresh_button.pack()



    def refresh(self):
        self.canvas.delete("all")

        list_of_polygons = get_polygons(
            fov=self.fov,
            aspect_ratio=self.aspect_ratio,
            camera_position=self.camera_position,
            screen_height=self.screen_height,
            camera_angle=self.camera_angle
        )

        for polygon in list_of_polygons:
            self.canvas.create_polygon(polygon.to_tuple(), fill=polygon.color)

        list_of_lines = get_lines(
            fov=self.fov,
            aspect_ratio=self.aspect_ratio,
            camera_position=self.camera_position,
            screen_height=self.screen_height,
            camera_angle=self.camera_angle
        )

        for line in list_of_lines:
            self.canvas.create_line(line.to_tuple(), fill=line.color)

    def rotate_x_plus(self):
        rotation = Quaternion.from_euler(math.radians(10), (0, 1, 0))
        self.camera_angle *= rotation
        # self.camera_position = rotate_vector_by_quaternion(self.camera_position, rotation)
        self.refresh()

    def rotate_x_minus(self):
        rotation = Quaternion.from_euler(math.radians(10), (0, -1, 0))
        self.camera_angle *= rotation
        # self.camera_position = rotate_vector_by_quaternion(self.camera_position, rotation)
        self.refresh()

    # TODO fix rotation quaternion
    def rotate_y_plus(self):
        axis = Vector(1, 0, 0)
        axis = rotate_vector_by_quaternion(axis, self.camera_angle)
        print(axis)
        rotation = Quaternion.from_euler(math.radians(10), axis)
        self.camera_angle *= rotation
        # self.camera_position = rotate_vector_by_quaternion(self.camera_position, rotation)
        self.refresh()

    def rotate_y_minus(self):
        axis = Vector(-1, 0, 0)
        axis = rotate_vector_by_quaternion(axis, self.camera_angle)
        print(axis)
        rotation = Quaternion.from_euler(math.radians(10), axis)
        self.camera_angle *= rotation
        # self.camera_position = rotate_vector_by_quaternion(self.camera_position, rotation)
        self.refresh()


if __name__ == "__main__":
    window = Window()
    window.root.mainloop()
