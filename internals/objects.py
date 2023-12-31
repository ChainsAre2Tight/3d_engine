from abc import ABC, abstractmethod
import internals.vectors
import internals.rgb


class Vertex(internals.vectors.Vector):
    pass


class Object2D(ABC):

    @abstractmethod
    def to_tuple(self):
        pass


class Point2D(Object2D):
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
    color: internals.rgb.RGB

    def __init__(self, first: Vertex, second: Vertex, color: internals.rgb.RGB):
        self.first = first
        self.second = second
        self.color = color

    @property
    def vertices(self):
        return self.first, self.second


class Polygon(Line):
    third: Vertex
    normal: internals.vectors.Vector

    def __init__(self, first: Vertex, second: Vertex, third: Vertex, color: internals.rgb.RGB,
                 normal: internals.vectors.Vector):
        super().__init__(first, second, color)
        self.third = third
        self.normal = normal

    @property
    def vertices(self):
        return self.first, self.second, self.third


class Quad(Polygon):
    def __init__(self, first: Vertex, second: Vertex, third: Vertex, fourth: Vertex, color: internals.rgb.RGB,
                 normal: internals.vectors.Vector):
        super().__init__(first, second, third, color, normal)
        self.fourth = fourth

    @property
    def vertices(self):
        return self.first, self.second, self.third, self.fourth

    def get_polygons(self) -> tuple[Polygon, Polygon]:
        return Polygon(
            first=self.first,
            second=self.second,
            third=self.third,
            color=self.color,
            normal=self.normal
        ), Polygon(
            first=self.first,
            second=self.third,
            third=self.fourth,
            color=self.color,
            normal=self.normal
        )


class Object:
    name: str
    smooth_shading: int
    polygons: list
    normals: list
    vertices: list
    color: internals.rgb.RGB

    def __init__(self, name: str, color: internals.rgb.RGB):
        self.name = name
        self.smooth_shading = 0
        self.polygons = list()
        self.normals = list()
        self.vertices = list()
        self.color = color
