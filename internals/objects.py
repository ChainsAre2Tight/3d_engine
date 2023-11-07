from abc import ABC, abstractmethod
import internals.vectors


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
    color: str

    def __init__(self, first: Vertex, second: Vertex, color: str):
        self.first = first
        self.second = second
        self.color = color

    @property
    def vertices(self):
        return self.first, self.second


class Polygon(Line):
    def __init__(self, first: Vertex, second: Vertex, third: Vertex, color: str):
        super().__init__(first, second, color)
        self.third = third

    @property
    def vertices(self):
        return self.first, self.second, self.third

    # TODO calculate normals (so they face out from (0, 0, 0))


class Quad(Polygon):
    def __init__(self, first: Vertex, second: Vertex, third: Vertex, fourth: Vertex, color: str):
        super().__init__(first, second, third, color)
        self.fourth = fourth

    @property
    def vertices(self):
        return self.first, self.second, self.third, self.fourth

    def get_polygons(self) -> tuple[Polygon, Polygon]:
        return Polygon(
            first=self.first,
            second=self.second,
            third=self.third,
            color=self.color
        ), Polygon(
            first=self.first,
            second=self.third,
            third=self.fourth,
            color=self.color
        )


