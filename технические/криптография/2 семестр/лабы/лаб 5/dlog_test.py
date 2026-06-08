import math
import unittest

from dlog import big_little_step, pollard_rho
from elgamal import gen

class TestBigLittleStep(unittest.TestCase):
    test_data = [
        (2, 0, 7, 0),   # 2^0 mod 7 = 1
        (2, 1, 7, 1),   # 2^1 mod 7 = 2
        (2, 2, 7, 2),   # 2^2 mod 7 = 4
        (3, 3, 11, 3),  # 3^3 mod 11 = 5
        (2, 5, 11, 5),  # 2^5 mod 11 = 10
        (10, 7, 29, 7), # 10^7 mod 29
        (5, 4, 23, 4),  # 5^4 mod 23 = 4
        (2, 3, 13, 3),  # 2^3 mod 13 = 8
        (6, 5, 17, 5),  # 6^5 mod 17
    ]

    @classmethod
    def setUpClass(cls):
        for p in [17, 19, 23, 29]:
            g = 2
            for x in range(1, 5):
                y = pow(g, x, p)
                cls.test_data.append((g, x, p, x))

    def test_table_cases(self):
        for g, x, p, expected in self.test_data:
            with self.subTest(g=g, x=x, p=p):
                y = pow(g, x, p)
                result = big_little_step(g, y, p)
                self.assertEqual(
                    result, expected,
                    f"log_{g}({y}) mod {p} должно быть {expected}, получено {result}"
                )

class TestPollardRhoDLog(unittest.TestCase):
    # Табличные тестовые данные: (g, x, y, p, q)
    test_data = []

    @classmethod
    def setUpClass(cls):
        for i in range(10):
            params, x, y = gen(32, 8)
            p, q, g = params
            cls.test_data.append((g, x, y, p, q))

    def test_table_cases(self):
        """Проверяем табличные случаи для pollard_rho"""
        for g, x, y, p, q in self.test_data:
            with self.subTest(g=g, x=x, y=y, p=p, q=q):
                result = pollard_rho(g, y, p, q)
                self.assertEqual(result, x,
                    f"Pollard rho log_{g}({y}) mod {p} должно быть {x}, получено {result}")

if __name__ == '__main__':
    unittest.main()
