from .quaternions import Vector, Quaternion, rotate_vector_by_quaternion
from abc import ABC, abstractmethod
import math


class Vertex(Vector):
    pass


class Object2D(ABC):

    @abstractmethod
    def to_tuple(self):
        pass


class Point2D:
    x: float
    y: float

    def __init__(self, x: int | float, y: int | float):
        self.x = float(x)
        self.y = float(y)

    def to_tuple(self):
        return self.x, self.y


class CanvasLine(Object2D):
    first: Point2D
    second: Point2D
    color: str

    def __init__(self, first: Point2D, second: Point2D, color: str):
        self.first = first
        self.second = second
        self.color = color

    def to_tuple(self):
        return self.first.x, self.first.y, self.second.x, self.second.y

    def __str__(self):
        return f'Line at {self.to_tuple()}'


class CanvasPolygon(CanvasLine):

    def __init__(self, first: Point2D, second: Point2D, third: Point2D, color: str):
        super().__init__(first, second, color)
        self.third = third

    def to_tuple(self):
        return self.first.x, self.first.y, self.second.x, self.second.y, self.third.x, self.third.y

    def __str__(self):
        return f'Polygon at {self.to_tuple()}'


class Line:
    first: Vertex
    second: Vertex
    color: str

    def __init__(self, first: Vertex, second: Vertex, color: str):
        self.first = first
        self.second = second
        self.color = color

    @property
    def vertices(self):
        return self.first, self.second

    def to_2d(self, center: dict) -> CanvasLine:
        new_vertices = list()
        for point_in_3d in self.vertices:
            new_vertices.append(
                Point2D(
                    point_in_3d.x + center["x"],
                    point_in_3d.y + center["y"]
                )
            )

        return CanvasLine(
            first=new_vertices[0],
            second=new_vertices[1],
            color=self.color
        )


class Polygon(Line):
    def __init__(self, first: Vertex, second: Vertex, third: Vertex, color: str):
        super().__init__(first, second, color)
        self.third = third

    @property
    def vertices(self):
        return self.first, self.second, self.third

    def to_2d(self, center: dict) -> CanvasPolygon:
        new_vertices = list()
        for point_in_3d in self.vertices:
            new_vertices.append(
                Point2D(
                    point_in_3d.x + center["x"],
                    point_in_3d.y + center["y"]
                )
            )

        return CanvasPolygon(
            first=new_vertices[0],
            second=new_vertices[1],
            third=new_vertices[2],
            color=self.color
        )


def convert_vertex_to_2d(vertex: Vertex, fov: float | int, aspect_ratio: float, camera_position: Vector,
                         screen_height: int, camera_angle: Quaternion) -> tuple[Point2D, float]:
    tan_fy = round(math.tan(fov / 2), 4)

    position = Vector(*vertex.to_tuple())

    rotated_position = rotate_vector_by_quaternion(position, camera_angle)

    res_y = (rotated_position.y * screen_height / (
            2 * (camera_position.length + rotated_position.z) * tan_fy)) + screen_height // 2
    res_x = (rotated_position.x * screen_height / (
            2 * aspect_ratio * (
            camera_position.length + rotated_position.z) * tan_fy)) + screen_height * aspect_ratio // 2
    depth = round(
        (rotated_position.x ** 2 + rotated_position.y ** 2 + (camera_position.length + rotated_position.z) ** 2) ** 0.5,
        4)

    # print(f'Vertex {vertex.to_tuple()} -> point ({res_x}, {res_y}) with depth {depth}')

    return Point2D(res_x, res_y), depth


def convert_polygon_to_2d(polygon: Polygon, fov: float | int, aspect_ratio: float, camera_position: Vector,
                          screen_height: int, camera_angle: Quaternion) -> tuple[CanvasPolygon, float]:
    average_depth = 0
    resulting_vertices = []

    for vertex in polygon.vertices:
        point, depth = convert_vertex_to_2d(
            vertex=vertex,
            fov=fov,
            aspect_ratio=aspect_ratio,
            camera_position=camera_position,
            screen_height=screen_height,
            camera_angle=camera_angle
        )
        average_depth += depth
        resulting_vertices.append(point)

    average_depth = round(average_depth / 3, 4)
    return CanvasPolygon(*resulting_vertices, color=polygon.color), average_depth


def convert_line_to_2d(line: Line, fov: float | int, aspect_ratio: float, camera_position: Vector,
                       screen_height: int, camera_angle: Quaternion) -> tuple[CanvasLine, float]:
    average_depth = 0
    resulting_vertices = []

    for vertex in line.vertices:
        point, depth = convert_vertex_to_2d(
            vertex=vertex,
            fov=fov,
            aspect_ratio=aspect_ratio,
            camera_position=camera_position,
            screen_height=screen_height,
            camera_angle=camera_angle
        )
        average_depth += depth
        resulting_vertices.append(point)

    average_depth = round(average_depth / 2, 4)
    return CanvasLine(*resulting_vertices, color=line.color), average_depth


def get_polygons(
        fov: float | int, aspect_ratio: float, camera_position: Vector,
        screen_height: int, camera_angle: Quaternion
) -> list[CanvasPolygon]:
    list_of_polygons = [
        Polygon(
            Vertex(-50, -50, -10),
            Vertex(-50, 50, -50),
            Vertex(50, 50, -10),
            "magenta"
        ),
        Polygon(
            Vertex(-50, -50, 10),
            Vertex(50, 50, 10),
            Vertex(50, -50, 50),
            "cyan"
        )
    ]

    list_of_canvas_polygons_unsorted = []

    for polygon in list_of_polygons:
        canvas_polygon, depth = convert_polygon_to_2d(
            polygon=polygon,
            fov=fov,
            aspect_ratio=aspect_ratio,
            camera_position=camera_position,
            screen_height=screen_height,
            camera_angle=camera_angle
        )
        list_of_canvas_polygons_unsorted.append((canvas_polygon, depth))

    list_of_canvas_polygons_unsorted.sort(key=lambda x: -x[1])

    list_of_canvas_polygons = list(map(lambda x: x[0], list_of_canvas_polygons_unsorted))

    return list_of_canvas_polygons


def get_lines(fov: float | int, aspect_ratio: float, camera_position: Vector,
              screen_height: int, camera_angle: Quaternion
              ) -> list[CanvasLine]:
    list_of_lines = [
        Line(
            Vertex(-200, 0, 0),
            Vertex(200, 0, 0),
            "blue"
        ),
        Line(
            Vertex(0, -200, 0),
            Vertex(0, 200, 0),
            "red"
        ),
        Line(
            Vertex(0, 0, -200),
            Vertex(0, 0, 200),
            "green"
        ),
    ]

    list_of_canvas_lines_unsorted = []

    for line in list_of_lines:
        canvas_line, depth = convert_line_to_2d(
            line=line,
            fov=fov,
            aspect_ratio=aspect_ratio,
            camera_position=camera_position,
            screen_height=screen_height,
            camera_angle=camera_angle
        )
        list_of_canvas_lines_unsorted.append((canvas_line, depth))

    list_of_canvas_lines_unsorted.sort(key=lambda x: x[1])

    list_of_canvas_lines = list(map(lambda x: x[0], list_of_canvas_lines_unsorted))

    return list_of_canvas_lines
