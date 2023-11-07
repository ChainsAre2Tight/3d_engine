import unittest
from internals.vectors import Vector, Quaternion, rotate_vector_by_quaternion
from math import pi


class TestVectors(unittest.TestCase):
    def test_str(self):
        vector = Vector(1.25, 3, -5.0)
        self.assertEqual("(1.25, 3.0, -5.0)", str(vector))

    def test_length(self):
        vector = Vector(5, 6, 8)
        self.assertEqual(125 ** 0.5, vector.length)

    def test_add(self):
        vector_A = Vector(5, 0, -3)
        vector_B = Vector(-7, 8, 6)
        vector_C = vector_A + vector_B
        self.assertEqual("(-2.0, 8.0, 3.0)", str(vector_C))

    def test_normalize(self):
        vector_A = Vector(1, 1, 0)
        vector_B = vector_A.normalize()
        self.assertEqual("(0.7071, 0.7071, 0.0)", str(vector_B))

    def test_mul_vector(self):
        vector_A = Vector(5, 0, -3)
        vector_B = Vector(-7, 8, 6)
        with self.assertRaises(NotImplementedError):
            vector_C = vector_A * vector_B

    def test_mul_number(self):
        vector_A = Vector(5, 0, -3)
        with self.assertRaises(NotImplementedError):
            vector_B = vector_A * 2

    def test_fail_mul(self):
        vector_A = Vector(1, 2, 3)
        with self.assertRaises(TypeError):
            vector_A * 'asd'


class TestQuaternions(unittest.TestCase):

    def test_str(self):
        quat = Quaternion(1, 2, 3, 4)
        self.assertEqual("(1.0, 2.0, 3.0, 4.0)", str(quat))

    def test_from_euler(self):
        quat = Quaternion.from_euler(pi / 2, (1, 0, 0))
        self.assertEqual("(0.7071, 0.7071, 0.0, 0.0)", str(quat))

    def test_add(self):
        quaternion_A = Quaternion(1, 2, 3, 4)
        quaternion_B = Quaternion(2, 3, 4, 5)
        with self.assertRaises(TypeError):
            quaternion_C = quaternion_A + quaternion_B

    def test_fail_mul(self):
        quaternion = Quaternion(1, 2, 3, 4)
        with self.assertRaises(TypeError):
            quaternion = quaternion * 2

    def test_mul(self):
        quaternion_A = Quaternion(0.7071, 0.7071, 0, 0)
        quaternion_B = Quaternion(0.7071, 0, 0.7071, 0)
        quaternion_C = quaternion_A * quaternion_B
        self.assertEqual("(0.5, 0.5, 0.5, 0.5)", str(quaternion_C))

    def test_mul_vector(self):
        quaternion_A = Quaternion(0.7071, 0.7071, 0, 0)
        vector_B = Vector(1, 0, 0)
        res = quaternion_A * vector_B
        self.assertEqual("(0.7071, 0.7071, 0.0, 0.0)", str(res))


class TestVectorRotation(unittest.TestCase):
    def test_1(self):
        vector = Vector(0, 0, 1)
        angle = pi
        axis = Vector(1, 0, 1)

        resulting_vector = rotate_vector_by_quaternion(
            vector=vector,
            quaternion=Quaternion.from_euler(
                rotation_angle=angle,
                rotate_axis=axis
            )
        )

        self.assertEqual("(1.0, 0.0, 0.0)", str(resulting_vector))

    # TODO make sure quaternion rotation works as intended as there are strange behaviours observed when rotating along non-X axis


if __name__ == '__main__':
    unittest.main()
