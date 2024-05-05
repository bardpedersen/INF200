from complex import ComplexNumber
import unittest


class ComplexTest(unittest.TestCase):
    def test_addition(self):
        z = ComplexNumber(2, 3)
        self.assertEqual(z + z, ComplexNumber(4, 6))
        self.assertNotEqual(z + z, ComplexNumber(3, 6))

    def test_subtraction(self):
        z = ComplexNumber(2, 3)
        self.assertEqual(z - ComplexNumber(0, 1), ComplexNumber(2, 2))
        self.assertNotEqual(z - ComplexNumber(0, 1), ComplexNumber(2, 5))

    def test_multiplication(self):
        z1 = ComplexNumber(1, 2)
        z2 = ComplexNumber(3, 4)
        self.assertEqual(z1 * z2, ComplexNumber(-5, 9))
        self.assertNotEqual(z1 * z2, ComplexNumber(-5, 8))

    def test_division(self):
        z1 = ComplexNumber(1, 2)
        z2 = ComplexNumber(3, 4)
        self.assertEqual(z1 / z2, ComplexNumber(0.44, 0.08))
        self.assertNotEqual(z1 / z2, ComplexNumber(0.44, 5))

    def test_equal(self):
        z = ComplexNumber(2, 3)
        self.assertTrue(z == ComplexNumber(2, 3))
        self.assertFalse(z == ComplexNumber(2, 2))

    def test_notequal(self):
        self.assertTrue(ComplexNumber(1, 2) != ComplexNumber(3, 4))
        self.assertFalse(ComplexNumber(1, 2) != ComplexNumber(1, 2))


if __name__ == '__main__':
    unittest.main(verbosity=2)
