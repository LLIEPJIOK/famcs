import unittest
from montgomery import extended_gcd, montgomery_pow
import math

class TestExtendedGCD(unittest.TestCase):
    def test_basic_gcd(self):
        a, b = 48, 18
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(a * x + b * y, g)

        a, b = 101, 13
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(a * x + b * y, g)

    def test_a_less_than_b(self):
        a, b = 18, 48
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(a * x + b * y, g)

    def test_one_input_zero(self):
        a, b = 35, 0
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(a * x + b * y, g)

        a, b = 0, 27
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(a * x + b * y, g)

    def test_both_inputs_zero(self):
        a, b = 0, 0
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(a * x + b * y, g)

    def test_coprime_numbers(self):
        a, b = 17, 5
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, 1)
        self.assertEqual(a * x + b * y, g)

        a, b = 34, 21
        g, x, y = extended_gcd(a, b)
        self.assertEqual(g, math.gcd(a, b))
        self.assertEqual(a * x + b * y, g)

class TestMontgomeryPow(unittest.TestCase):

    def test_small_numbers(self):
        self.assertEqual(montgomery_pow(3, 4, 5), pow(3, 4, 5))
        self.assertEqual(montgomery_pow(7, 10, 13), pow(7, 10, 13))
        self.assertEqual(montgomery_pow(2, 5, 7), pow(2, 5, 7))
        self.assertEqual(montgomery_pow(10, 3, 11), pow(10, 3, 11))

    def test_large_numbers(self):
        base = 12345678
        exp = 18765432
        mod = 1000000007
        self.assertEqual(montgomery_pow(base, exp, mod), pow(base, exp, mod))

        base = 2**100 + 1
        exp = 2**50 + 1
        mod = 2**128 - 159
        self.assertEqual(montgomery_pow(base, exp, mod), pow(base, exp, mod))

    def test_base_one(self):
        self.assertEqual(montgomery_pow(1, 100, 123), pow(1, 100, 123))

    def test_modulus_one(self):
        self.assertEqual(montgomery_pow(10, 5, 1), pow(10, 5, 1))

    def test_base_larger_than_modulus(self):
        self.assertEqual(montgomery_pow(100, 5, 13), pow(100, 5, 13))
        self.assertEqual(montgomery_pow(20, 3, 7), pow(20, 3, 7))

    def test_negative_exponent(self):
        with self.assertRaises(ValueError):
            montgomery_pow(10, -2, 7)

    def test_non_positive_modulus(self):
        with self.assertRaises(ValueError):
            montgomery_pow(10, 5, 0)
        with self.assertRaises(ValueError):
            montgomery_pow(10, 5, -7)

if __name__ == '__main__':
    unittest.main()