from abc import ABC, abstractmethod
import internals.objects


class _AbstractHandler(ABC):
    pass


class DataHandler(_AbstractHandler):
    _lines = list[internals.objects.Line]
    _vertices = list[internals.objects.Vertex]
    _polygons = list[internals.objects.Polygon]

    def __init__(self):
        self._lines = [
            internals.objects.Line(
                internals.objects.Vertex(-200, 0, 0),
                internals.objects.Vertex(200, 0, 0),
                "blue"
            ),
            internals.objects.Line(
                internals.objects.Vertex(0, -200, 0),
                internals.objects.Vertex(0, 200, 0),
                "red"
            ),
            internals.objects.Line(
                internals.objects.Vertex(0, 0, -200),
                internals.objects.Vertex(0, 0, 200),
                "green"
            ),
        ]

        self._polygons = [
            internals.objects.Polygon(
                internals.objects.Vertex(-50, -50, -10),
                internals.objects.Vertex(-50, 50, -50),
                internals.objects.Vertex(50, 50, -10),
                "magenta"
            ),
            internals.objects.Polygon(
                internals.objects.Vertex(-50, -50, 10),
                internals.objects.Vertex(50, 50, 10),
                internals.objects.Vertex(50, -50, 50),
                "cyan"
            )
        ]

    def read_file(self, file_name, *args, **kwargs):
        pass

    def get_lines(self) -> list[internals.objects.Line]:
        return self._lines

    def get_polygons(self) -> list[internals.objects.Polygon]:
        return self._polygons
