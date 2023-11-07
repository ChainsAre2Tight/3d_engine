from abc import ABC, abstractmethod
import internals.objects
import random


class _AbstractHandler(ABC):
    pass


def random_color(exclude: str = '') -> str:
    colors = [
        "black",
        # "white",
        "red",
        "green",
        "blue",
        "cyan",
        "yellow",
        "magenta",
    ]
    if exclude != "":
        colors.remove(exclude)
    return random.choice(colors)


class FileHandler(_AbstractHandler):
    _file_path: str
    _file_name: str

    def __init__(self, file_path, file_name):
        self._file_path = file_path
        self._file_name = file_name

    def read_file(self) -> list[str]:
        with open(f"{self._file_path}/{self._file_name}") as file:
            list_of_lines = list(map(lambda x: x.rstrip(), file.readlines()))

        return list_of_lines

    def interpret_file(self):
        lines = self.read_file()
        current_object = "None"
        res = dict()
        line_number = 0

        for line in lines:
            line_number += 1
            # print(line)
            first_space = line.find(" ")
            prefix = line[:first_space]
            if prefix == "#":
                continue
            data = line[first_space + 1:]

            if prefix == "o":
                current_object = data
                if data in res.keys():
                    raise NameError(f"Two objects have the same name {data} in .OBJ file {self._file_name}")
                else:
                    res[data] = {"polygons": list(), "vertices": list(), "smooth_shading": 0}
            elif prefix == "v":
                v1, v2, v3 = list(map(float, data.split()))
                res[current_object]["vertices"].append(
                    internals.objects.Vertex(x=v1, y=v2, z=v3)
                )
            elif prefix == "s":
                res[current_object]["smooth_shading"] = int(data)
            elif prefix == "f":
                indexes = list(map(lambda x: int(x) - 1, data.split()))
                if len(indexes) == 3:
                    res[current_object]["polygons"].append(
                        internals.objects.Polygon(
                            first=res[current_object]["vertices"][indexes[0]],
                            second=res[current_object]["vertices"][indexes[1]],
                            third=res[current_object]["vertices"][indexes[2]],
                            color=random_color()
                        )
                    )
                elif len(indexes) == 4:
                    quad = internals.objects.Quad(
                        first=res[current_object]["vertices"][indexes[0]],
                        second=res[current_object]["vertices"][indexes[1]],
                        third=res[current_object]["vertices"][indexes[2]],
                        fourth=res[current_object]["vertices"][indexes[3]],
                        color=random_color()
                    )
                    t1, t2 = quad.get_polygons()
                    t1.color = random_color()
                    t2.color = random_color(t1.color)

                    res[current_object]["polygons"].append(t1)
                    res[current_object]["polygons"].append(t2)
                else:
                    raise NotImplementedError(f"Can only handle triangles and quads but got {len[indexes]}-gon")
            else:
                raise KeyError(
                    f'Got unexpected prefix "{prefix}" while reading {self._file_name} at line {line_number}')

        # return data
        return res


class DataHandler(_AbstractHandler):
    _lines: list[internals.objects.Line]
    _vertices: list[internals.objects.Vertex]
    _polygons: list[internals.objects.Polygon]
    _objects: dict

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

        # self._polygons = [
        #     internals.objects.Polygon(
        #         internals.objects.Vertex(-50, -50, -10),
        #         internals.objects.Vertex(-50, 50, -50),
        #         internals.objects.Vertex(50, 50, -10),
        #         "magenta"
        #     ),
        #     internals.objects.Polygon(
        #         internals.objects.Vertex(-50, -50, 10),
        #         internals.objects.Vertex(50, 50, 10),
        #         internals.objects.Vertex(50, -50, 50),
        #         "cyan"
        #     )
        # ]
        self._polygons = list()

    def read_file(self, file_path, file_name, *args, **kwargs):
        pass
        reader = FileHandler(file_path=file_path, file_name=file_name)
        self._objects = reader.interpret_file()

        for obj in self._objects.keys():
            self._polygons.extend(self._objects[obj]["polygons"])

    def get_lines(self) -> list[internals.objects.Line]:
        return self._lines

    def get_polygons(self) -> list[internals.objects.Polygon]:
        return self._polygons
