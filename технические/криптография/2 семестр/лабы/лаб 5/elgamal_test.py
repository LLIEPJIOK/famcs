import unittest
import math

from elgamal import (
    is_prime, mulmod, gen, sign, verify
)

class TestCryptoFunctions(unittest.TestCase):
    def test_mulmod(self):
        cases = [
            (2, 3, 5, 6 % 5),
            (10, 10, 7, 100 % 7),
            (123456, 654321, 12345, (123456 * 654321) % 12345)
        ]
        for a, b, mod, expected in cases:
            with self.subTest(a=a, b=b, mod=mod):
                self.assertEqual(mulmod(a, b, mod), expected)

    def test_gen_and_group_properties(self):
        bits = 512
        params, x, y = gen(bits)
        p, q, g = params
        # p and q primes
        self.assertTrue(is_prime(p), "p is not prime")
        self.assertTrue(is_prime(q), "q is not prime")
        # q divides p-1
        self.assertEqual((p - 1) % q, 0, "q does not divide p-1")
        # g^q mod p == 1
        self.assertEqual(pow(g, q, p), 1, "g^q mod p != 1")
        # x range and y correctness
        self.assertTrue(1 <= x < q, "x out of range")
        self.assertEqual(y, pow(g, x, p), "y != g^x mod p")

    def test_sign_verify(self):
        bits = 512
        params, x, y = gen(bits)
        message = "UnitTest Message"

        r, s = sign(params, x, message)
        # valid signature
        self.assertTrue(verify(params, y, message, (r, s)), "Valid signature failed verification")
        # tampered message
        self.assertFalse(verify(params, y, message + "!", (r, s)), "Verification passed for tampered message")
        # tampered signature
        self.assertFalse(verify(params, y, message, (r+1, s)), "Verification passed for tampered r")
        self.assertFalse(verify(params, y, message, (r, s+1)), "Verification passed for tampered s")

if __name__ == '__main__':
    unittest.main()
