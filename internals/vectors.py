import math


class Vector:
    x: float = 0
    y: float = 0
    z: float = 0

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def to_tuple(self):
        return self.x, self.y, self.z

    @property
    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def dot_product(self, other) -> float:
        if type(other) == Vector:
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise TypeError(f'Unsupported dot product operation for Vector and {type(other)}')

    def __add__(self, other):
        if type(other) != Vector:
            raise TypeError
        return Vector(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z
        )

    def __sub__(self, other):
        if type(other) != Vector:
            raise TypeError
        return Vector(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z
        )

    def __mul__(self, other):
        if type(other) == Vector:
            raise NotImplementedError
        if type(other) == int or type(other) == float:
            return Vector(
                x=round(self.x * other, 4),
                y=round(self.y * other, 4),
                z=round(self.z * other, 4)
            )
        else:
            raise TypeError

    def normalize(self):
        length = self.length
        return Vector(
            x=round(self.x / length, 4),
            y=round(self.y / length, 4),
            z=round(self.z / length, 4)
        )


class Quaternion(Vector):
    w: float = 0

    def __init__(self, w, x, y, z):
        super().__init__(x, y, z)
        self.w = float(w)

    @staticmethod
    def from_euler(rotation_angle: float | int, rotate_axis: Vector | tuple):
        if type(rotate_axis) == tuple:
            rotate_axis = Vector(
                x=rotate_axis[0],
                y=rotate_axis[1],
                z=rotate_axis[2]
            )

        rotate_axis = rotate_axis.normalize()

        return Quaternion(
            w=round(math.cos(rotation_angle / 2), 4),
            x=round(rotate_axis.x * math.sin(rotation_angle / 2), 4),
            y=round(rotate_axis.y * math.sin(rotation_angle / 2), 4),
            z=round(rotate_axis.z * math.sin(rotation_angle / 2), 4)
        )

    @property
    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w) ** 0.5

    def __str__(self):
        return f'({self.w}, {self.x}, {self.y}, {self.z})'

    def normalize(self):
        length = self.length
        return self * (1 / length)

    def invert(self):
        return Quaternion(
            w=self.w,
            x=-self.x,
            y=-self.y,
            z=-self.z
        )

    def __add__(self, other):
        raise TypeError

    def __sub__(self, other):
        raise TypeError

    def __mul__(self, other):
        if type(other) == int | float:
            return Quaternion(
                w=round(self.w * other, 4),
                x=round(self.x * other, 4),
                y=round(self.y * other, 4),
                z=round(self.z * other, 4)
            )
        elif type(other) == Quaternion:
            return Quaternion(
                w=round(self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z, 4),
                x=round(self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y, 4),
                y=round(self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x, 4),
                z=round(self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w, 4)
            )
        elif type(other) == Vector:
            return Quaternion(
                w=round(-self.x * other.x - self.y * other.y - self.z * other.z, 4),
                x=round(self.w * other.x + self.y * other.z - self.z * other.y, 4),
                y=round(self.w * other.y - self.x * other.z + self.z * other.x, 4),
                z=round(self.w * other.z + self.x * other.y - self.y * other.x, 4)
            )
        else:
            raise TypeError

    def to_tuple(self):
        return self.w, self.x, self.y, self.z

    def dot_product(self, other):
        raise NotImplementedError


def rotate_vector_by_quaternion(vector: Vector, quaternion: Quaternion) -> Vector:
    resulting_vector = quaternion * vector
    resulting_vector *= quaternion.invert()

    return Vector(
        x=resulting_vector.x,
        y=resulting_vector.y,
        z=resulting_vector.z,
    )


def get_cosine(v1: Vector, v2: Vector) -> float:
    return v1.dot_product(v2) / (v1.length * v2.length)


def calculate_angle(v1: Vector, v2: Vector) -> float:
    return math.acos(get_cosine(v1, v2))


if __name__ == "__main__":
    pass
