from abc import ABC, abstractmethod
import internals.objects
import internals.vectors
import internals.rgb


class _AbstractHandler(ABC):
    pass


class NoNormalsException(Exception):
    pass


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
        previous_indexes = 0
        previous_normals = 0

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
                    # TODO replace with dataclass
                    res[data] = internals.objects.Object(data, color=internals.rgb.next_color())
                    # res[data] = {"polygons": list(), "vertices": list(), "smooth_shading": 0, "normals": list()}
            elif prefix == "v":
                v1, v2, v3 = list(map(float, data.split()))
                # res[current_object]["vertices"].append(
                #     internals.objects.Vertex(x=v1, y=v2, z=v3)
                # )
                res[current_object].vertices.append(
                    internals.objects.Vertex(x=v1, y=v2, z=v3)
                )
                previous_indexes += 1
            elif prefix == "s":
                # res[current_object]["smooth_shading"] = int(data)
                res[current_object].smooth_shading = int(data)
            elif prefix == "vn":
                # res[current_object]["normals"].append(internals.vectors.Vector(*list(map(float, data.split()))))
                res[current_object].normals.append(internals.vectors.Vector(*list(map(float, data.split()))))
                previous_normals += 1
            elif prefix == "f":
                indexes = data.split()

                for i in range(len(indexes)):
                    smol_data = indexes[i].split("/")
                    if len(smol_data) == 1:
                        indexes[i] = int(smol_data[0])
                        normal = None
                        material = None
                    else:
                        index = int(smol_data[0]) - 1 - previous_indexes
                        material = smol_data[1]
                        normal = int(smol_data[2]) - 1 - previous_normals
                        indexes[i] = int(index)
                # polygon_normal = res[current_object]["normals"][normal]
                try:
                    polygon_normal = res[current_object].normals[normal]
                except TypeError:
                    raise NoNormalsException("Normals are missing")
                if len(indexes) == 3:
                    # print(indexes)
                    res[current_object].polygons.append(
                        internals.objects.Polygon(
                            first=res[current_object].vertices[indexes[0]],
                            second=res[current_object].vertices[indexes[1]],
                            third=res[current_object].vertices[indexes[2]],
                            color=res[current_object].color,
                            normal=polygon_normal
                        )
                    )
                elif len(indexes) == 4:
                        quad = internals.objects.Quad(
                            first=res[current_object].vertices[indexes[0]],
                            second=res[current_object].vertices[indexes[1]],
                            third=res[current_object].vertices[indexes[2]],
                            fourth=res[current_object].vertices[indexes[3]],
                            color=res[current_object].color,
                            normal=polygon_normal,
                        )
                        t1, t2 = quad.get_polygons()
                        res[current_object].polygons.append(t1)
                        res[current_object].polygons.append(t2)
                else:
                    raise NotImplementedError(f"Can only handle triangles and quads but got {len(indexes)}-gon")


            else:
                raise KeyError(
                    f'Got unexpected prefix "{prefix}" while reading {self._file_name} at line {line_number}')

        # return data
        # print(res)
        return res


class SceneData(_AbstractHandler):
    _lines: list[internals.objects.Line]
    _vertices: list[internals.objects.Vertex]
    _polygons: list[internals.objects.Polygon]
    _objects: dict

    def __init__(self):
        self._lines = [
            internals.objects.Line(
                internals.objects.Vertex(-2, 0, 0),
                internals.objects.Vertex(2, 0, 0),
                "blue"
            ),
            internals.objects.Line(
                internals.objects.Vertex(0, -2, 0),
                internals.objects.Vertex(0, 2, 0),
                "red"
            ),
            internals.objects.Line(
                internals.objects.Vertex(0, 0, -2),
                internals.objects.Vertex(0, 0, 2),
                "green"
            ),
        ]

        self._polygons = list()

    def read_file(self, file_path, file_name, *args, **kwargs):
        pass
        reader = FileHandler(file_path=file_path, file_name=file_name)
        self._objects = reader.interpret_file()

        for obj in self._objects.keys():
            self._polygons.extend(self._objects[obj].polygons)

    def get_lines(self) -> list[internals.objects.Line]:
        return self._lines

    def get_polygons(self) -> list[internals.objects.Polygon]:
        return self._polygons
