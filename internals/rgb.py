import random
import internals.vectors


class RGB:
    _r: int
    _g: int
    _b: int

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @staticmethod
    def from_hex(hex_color: str):
        if hex_color[0] == '#':
            hex_color = hex_color[1:]
        return RGB(
            r=int(hex_color[:2], 16),
            g=int(hex_color[2:4], 16),
            b=int(hex_color[4:], 16)
        )

    def to_hex(self) -> str:
        return f"#{str(hex(self.r))[2:]}{str(hex(self.g))[2:]}{str(hex(self.b))[2:]}"

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        if value > 255:
            value = 255
        elif value < 0:
            value = 0
        self._r = int(value)

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        if value > 255:
            value = 255
        elif value < 0:
            value = 0
        self._g = int(value)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if value > 255:
            value = 255
        elif value < 0:
            value = 0
        self._b = int(value)

    def to_tuple(self):
        return self.r, self.g, self.b

    def __str__(self):
        return str(self.to_tuple())

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return RGB(
                r=self.r*other,
                g=self.g*other,
                b=self.b*other,
            )
        else:
            raise NotImplementedError(type(other))


def light_gray_color():
    return RGB(50, 128, 200)


if __name__ == "__main__":
    print(light_gray_color().to_hex())


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


class Light:
    _intensity: float | int
    _direction: internals.vectors.Vector
    _albedo: float
    _color: RGB

    def __init__(self,
                 intensity: float | int,
                 direction: internals.vectors.Vector,
                 albedo: float,
                 color: RGB,
                 ):
        self._intensity = intensity
        self._direction = direction
        self._albedo = albedo
        self._color = color

    @property
    def intensity(self):
        return self._intensity

    @property
    def direction(self):
        return self._direction

    @property
    def albedo(self):
        return self._albedo

    @property
    def color(self):
        return self._color
