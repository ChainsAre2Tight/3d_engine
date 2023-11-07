import internals.vectors
import internals.objects
import internals.handlers
import math


class Renderer:
    data_handler: internals.handlers.DataHandler
    fov: float | int
    aspect_ratio: float
    camera_position: internals.vectors.Vector
    screen_height: int
    camera_angle: internals.vectors.Quaternion

    def __init__(self,
                 data_handler: internals.handlers.DataHandler,
                 fov: float | int,
                 aspect_ratio: float,
                 camera_position: internals.vectors.Vector,
                 screen_height: int,
                 camera_angle: internals.vectors.Quaternion
                 ):
        self.data_handler = data_handler
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.camera_position = camera_position
        self.screen_height = screen_height
        self.camera_angle = camera_angle

    def render_polygons(self) -> list[internals.objects.CanvasPolygon]:

        list_of_polygons = self.data_handler.get_polygons()

        list_of_canvas_polygons_unsorted = []

        for polygon in list_of_polygons:
            canvas_polygon, depth = _convert_polygon_to_2d(
                polygon=polygon,
                fov=self.fov,
                aspect_ratio=self.aspect_ratio,
                camera_position=self.camera_position,
                screen_height=self.screen_height,
                camera_angle=self.camera_angle,
                depth_interpolation_method="average",
            )
            list_of_canvas_polygons_unsorted.append((canvas_polygon, depth))

        # TODO sort out polygons whose normals are more than 90 degrees from camera


        list_of_canvas_polygons_unsorted.sort(key=lambda x: -x[1])

        list_of_canvas_polygons = list(map(lambda x: x[0], list_of_canvas_polygons_unsorted))

        return list_of_canvas_polygons

    def render_lines(self) -> list[internals.objects.CanvasLine]:

        list_of_lines = self.data_handler.get_lines()

        list_of_canvas_lines_unsorted = []

        for line in list_of_lines:
            canvas_line, depth = _convert_line_to_2d(
                line=line,
                fov=self.fov,
                aspect_ratio=self.aspect_ratio,
                camera_position=self.camera_position,
                screen_height=self.screen_height,
                camera_angle=self.camera_angle
            )
            list_of_canvas_lines_unsorted.append((canvas_line, depth))

        list_of_canvas_lines_unsorted.sort(key=lambda x: x[1])

        list_of_canvas_lines = list(map(lambda x: x[0], list_of_canvas_lines_unsorted))

        return list_of_canvas_lines


def _convert_vertex_to_2d(vertex: internals.objects.Vertex, fov: float | int, aspect_ratio: float,
                          camera_position: internals.vectors.Vector,
                          screen_height: int, camera_angle: internals.vectors.Quaternion) -> tuple[
    internals.objects.Point2D, float]:
    tan_fy = round(math.tan(fov / 2), 4)

    position = internals.vectors.Vector(*vertex.to_tuple())

    rotated_position = internals.vectors.rotate_vector_by_quaternion(position, camera_angle)

    res_y = (rotated_position.y * screen_height / (
            2 * (camera_position.length + rotated_position.z) * tan_fy)) + screen_height // 2
    res_x = (rotated_position.x * screen_height / (
            2 * aspect_ratio * (
            camera_position.length + rotated_position.z) * tan_fy)) + screen_height * aspect_ratio // 2
    depth = round(
        (rotated_position.x ** 2 + rotated_position.y ** 2 + (camera_position.length + rotated_position.z) ** 2) ** 0.5,
        4)

    # print(f'Vertex {vertex.to_tuple()} -> point ({res_x}, {res_y}) with depth {depth}')

    return internals.objects.Point2D(res_x, res_y), depth


def _convert_polygon_to_2d(polygon: internals.objects.Polygon, fov: float | int, aspect_ratio: float,
                           camera_position: internals.vectors.Vector,
                           screen_height: int, camera_angle: internals.vectors.Quaternion,
                           depth_interpolation_method: str
                           ) -> tuple[internals.objects.CanvasPolygon, float]:
    depthes = []
    resulting_vertices = []

    for vertex in polygon.vertices:
        point, depth = _convert_vertex_to_2d(
            vertex=vertex,
            fov=fov,
            aspect_ratio=aspect_ratio,
            camera_position=camera_position,
            screen_height=screen_height,
            camera_angle=camera_angle
        )
        depthes.append(depth)
        resulting_vertices.append(point)

    resulting_depth: float
    if depth_interpolation_method == "average":
        resulting_depth = round(sum(depthes) / 3, 4)
    elif depth_interpolation_method == "nearest":
        resulting_depth = min(depthes)
    elif depth_interpolation_method == "furthest":
        resulting_depth = max(depthes)
    else:
        raise KeyError("Unknown interpolation method")
    return internals.objects.CanvasPolygon(*resulting_vertices, color=polygon.color), resulting_depth


def _convert_line_to_2d(line: internals.objects.Line, fov: float | int, aspect_ratio: float,
                        camera_position: internals.vectors.Vector,
                        screen_height: int, camera_angle: internals.vectors.Quaternion) -> tuple[
    internals.objects.CanvasLine, float]:
    average_depth = 0
    resulting_vertices = []

    for vertex in line.vertices:
        point, depth = _convert_vertex_to_2d(
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
    return internals.objects.CanvasLine(*resulting_vertices, color=line.color), average_depth
