import unittest
from rsa import (
    carmichael_rsa,
    fermat,
    rabin_miller,
    jacobi,
    solovay_strassen,
    is_prime,
    generate_prime,
    generate_keys,
    encrypt,
    decrypt
)
import math

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
SMALL_COMPOSITES = [4, 6, 8, 9, 10, 12, 14, 15, 18, 20, 21, 22, 24, 25, 26, 27]
CARMICHAEL_NUMBERS = [561, 1105, 1729]

class TestRSAFunctions(unittest.TestCase):
    def test_carmichael_rsa(self):
        self.assertEqual(carmichael_rsa(3, 11), math.lcm(2, 10))
        self.assertEqual(carmichael_rsa(5, 13), math.lcm(4, 12))
        self.assertEqual(carmichael_rsa(17, 19), math.lcm(16, 18)) 
        self.assertEqual(carmichael_rsa(7, 13), math.lcm(6, 12))
        self.assertEqual(carmichael_rsa(7, 13), math.lcm(6, 12))

    def test_jacobi_symbol(self):
        self.assertEqual(jacobi(2, 7), 1)
        self.assertEqual(jacobi(10, 21), -1)
        self.assertEqual(jacobi(15, 29), -1)
        self.assertEqual(jacobi(7, 15), -1)
        self.assertEqual(jacobi(0, 7), 0)
        self.assertEqual(jacobi(1, 11), 1)

        # Property (a/n) = (a % n / n)
        self.assertEqual(jacobi(17, 11), jacobi(6, 11))

        # Property (ab/n) = (a/n)(b/n)
        self.assertEqual(jacobi(6, 11), jacobi(2, 11) * jacobi(3, 11))
        
        with self.assertRaises(ValueError):
            jacobi(5, 8)

    def test_primality_tests(self):
        k = 20

        for p in SMALL_PRIMES:
            self.assertTrue(fermat(p, k), f"Fermat failed for prime {p}")
            self.assertTrue(rabin_miller(p, k), f"Miller-Rabin failed for prime {p}")
            self.assertTrue(is_prime(p, k), f"is_prime failed for prime {p}")

        for c in SMALL_COMPOSITES:
            self.assertFalse(rabin_miller(c, k), f"Miller-Rabin failed for composite {c}")
            self.assertFalse(solovay_strassen(c, k), f"Solovay-Strassen failed for composite {c}")
            self.assertFalse(fermat(c, k), f"Fermat incorrectly identified composite {c} as prime")
            self.assertFalse(is_prime(c, k), f"is_prime failed for composite {c}")

        for carmichael in CARMICHAEL_NUMBERS:
            self.assertFalse(rabin_miller(carmichael, k), f"Miller-Rabin failed for Carmichael {carmichael}")
            self.assertFalse(solovay_strassen(carmichael, k), f"Solovay-Strassen failed for Carmichael {carmichael}")
            self.assertFalse(is_prime(carmichael, k), f"is_prime failed for Carmichael {carmichael}")

        self.assertFalse(is_prime(0, k))
        self.assertFalse(is_prime(1, k))
        self.assertFalse(is_prime(-5, k))

    def test_generate_prime(self):
        bits = 64
        p = generate_prime(bits)
        self.assertTrue(p.bit_length() == bits)
        self.assertTrue(is_prime(p, 100))

    def test_generate_keys(self):
        bits = 512
        pubkey, privkey = generate_keys(bits)
        e, n = pubkey
        d, n_priv, p, q = privkey

        self.assertEqual(n, n_priv)
        self.assertEqual(n, p * q)
        self.assertTrue(is_prime(p, 40))
        self.assertTrue(is_prime(q, 40))
        self.assertNotEqual(p, q)

        lambda_n = carmichael_rsa(p, q)
        self.assertEqual((e * d) % lambda_n, 1)

    def test_encrypt_decrypt(self):
        bits = 512
        pubkey, privkey = generate_keys(bits)
        message = "This is a test message for RSA encryption and decryption!"

        encrypted = encrypt(message, pubkey)
        decrypted = decrypt(encrypted, privkey)
        self.assertEqual(message, decrypted)

        self.assertEqual(decrypt(encrypt("", pubkey), privkey), "")
        
        message_special = "Testing 123!@#$%^&*()_+=-`~[]{};':\",./<>?"
        self.assertEqual(decrypt(encrypt(message_special, pubkey), privkey), message_special)

if __name__ == '__main__':
    unittest.main()