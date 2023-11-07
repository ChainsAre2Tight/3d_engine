import unittest
from internals.vectors import Vector, Quaternion, rotate_vector_by_quaternion
from math import pi
import math


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


class TestQuaternionCreation(unittest.TestCase):
    def test_1(self):
        q = Quaternion.from_euler(0.785, (1, 0, 0))
        self.assertEqual((0.3825, 0, 0, 0.924), q.to_tuple())

    def test_2(self):
        q = Quaternion.from_euler(0.785, (1, 1, 0))
        self.assertEqual((0.2705, 0.2705, 0, 0.924), q.to_tuple())

    def test_3(self):
        q = Quaternion.from_euler(0.785, (1, 1, 1))
        self.assertEqual((0.2209, 0.2209, 0.2209, 0.924), q.to_tuple())

    def test_4(self):
        q = Quaternion.from_euler(4, (1, 2, -3))
        self.assertEqual((0.2431, 0.4860, -0.7291, -0.4161), q.to_tuple())

    def test_5(self):
        q = Quaternion.from_euler(-32, (5, 2, 8))
        self.assertEqual((0.1493, 0.0597, 0.2388, -0.9577), q.to_tuple())

class TestQuaternionMultiplication(unittest.TestCase):

    def test_1(self):
        q1 = Quaternion(1, 1, -2, 3)
        q2 = Quaternion(-4, 2, -5, 1)
        q3 = q1 * q2
        self.assertEqual((-19, 11, 8, -12), q3.to_tuple())

    def test_2(self):
        q1 = Quaternion(-10, 9, -8, 7)
        q2 = Quaternion(-6, 5, -4, 3)
        q3 = q1 * q2
        self.assertEqual((-38, -100, 96, -68), q3.to_tuple())


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

    def test_2(self):
        vector = Vector(1, 0, 0)
        quaternion = Quaternion(w=0.944, x=0.269, y=0.145, z=0.128)
        self.assertEqual((0.9252, -0.1635, 0.3423), rotate_vector_by_quaternion(vector, quaternion).to_tuple())



    # TODO make sure quaternion rotation works as intended as there are strange behaviours observed when rotating along non-X axis


if __name__ == '__main__':
    unittest.main()
