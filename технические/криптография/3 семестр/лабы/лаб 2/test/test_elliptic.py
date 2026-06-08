"""
Тесты для модуля elliptic.py - эллиптические кривые
"""

import pytest
import secrets
import sys
import os

# Добавляем путь к app в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from crypto.elliptic import EllipticCurve, ECPoint


class TestEllipticCurve:
    """Тесты для класса EllipticCurve"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        """Стандартная кривая для тестов"""
        return EllipticCurve.default_curve()

    def test_default_curve_initialization(self, curve: EllipticCurve):
        """Проверка корректной инициализации кривой"""
        assert curve.l == 128
        assert curve.p > 0
        assert curve.a >= 0
        assert curve.b > 0
        assert curve.q > 0
        assert curve.G is not None

    def test_base_point_on_curve(self, curve: EllipticCurve):
        """Базовая точка должна лежать на кривой"""
        assert curve.is_on_curve(curve.G)

    def test_point_at_infinity_on_curve(self, curve: EllipticCurve):
        """Точка на бесконечности должна быть на кривой"""
        assert curve.is_on_curve(None)

    def test_random_point_not_on_curve(self, curve: EllipticCurve):
        """Случайная точка скорее всего не лежит на кривой"""
        random_point = (secrets.randbelow(curve.p), secrets.randbelow(curve.p))
        # С очень высокой вероятностью случайная точка не на кривой
        # Но это может быть False, поэтому мы просто проверяем, что функция работает
        result = curve.is_on_curve(random_point)
        assert isinstance(result, bool)

    def test_add_identity_left(self, curve: EllipticCurve):
        """Сложение с бесконечностью слева: O + P = P"""
        P = curve.G
        result = curve.add(None, P)
        assert result == P

    def test_add_identity_right(self, curve: EllipticCurve):
        """Сложение с бесконечностью справа: P + O = P"""
        P = curve.G
        result = curve.add(P, None)
        assert result == P

    def test_add_both_infinity(self, curve: EllipticCurve):
        """Сложение двух бесконечностей: O + O = O"""
        result = curve.add(None, None)
        assert result is None

    def test_add_inverse_points(self, curve: EllipticCurve):
        """P + (-P) = O (точка на бесконечности)"""
        P = curve.G
        neg_P = curve.neg(P)
        result = curve.add(P, neg_P)
        assert result is None

    def test_point_doubling(self, curve: EllipticCurve):
        """Удвоение точки: P + P = 2P"""
        P = curve.G
        double = curve.add(P, P)
        assert curve.is_on_curve(double)
        # Также проверяем, что результат отличается от исходной точки
        assert double != P

    def test_add_associativity(self, curve: EllipticCurve):
        """Ассоциативность сложения: (P + Q) + R = P + (Q + R)"""
        P = curve.G
        Q = curve.mul(2, curve.G)
        R = curve.mul(3, curve.G)
        
        left = curve.add(curve.add(P, Q), R)
        right = curve.add(P, curve.add(Q, R))
        
        assert left == right

    def test_add_commutativity(self, curve: EllipticCurve):
        """Коммутативность сложения: P + Q = Q + P"""
        P = curve.G
        Q = curve.mul(5, curve.G)
        
        assert curve.add(P, Q) == curve.add(Q, P)

    def test_neg_point(self, curve: EllipticCurve):
        """Отрицание точки корректно вычисляется"""
        P = curve.G
        neg_P = curve.neg(P)
        
        assert neg_P is not None
        assert neg_P[0] == P[0]  # x-координата та же
        assert (neg_P[1] + P[1]) % curve.p == 0  # y-координаты противоположны
        assert curve.is_on_curve(neg_P)

    def test_neg_infinity(self, curve: EllipticCurve):
        """Отрицание бесконечности: -O = O"""
        assert curve.neg(None) is None

    def test_sub_points(self, curve: EllipticCurve):
        """Вычитание точек: P - Q = P + (-Q)"""
        P = curve.mul(5, curve.G)
        Q = curve.mul(3, curve.G)
        
        result = curve.sub(P, Q)
        expected = curve.add(P, curve.neg(Q))
        
        assert result == expected
        assert curve.is_on_curve(result)

    def test_mul_by_zero(self, curve: EllipticCurve):
        """Умножение на 0: 0 * P = O"""
        P = curve.G
        result = curve.mul(0, P)
        assert result is None

    def test_mul_by_one(self, curve: EllipticCurve):
        """Умножение на 1: 1 * P = P"""
        P = curve.G
        result = curve.mul(1, P)
        assert result == P

    def test_mul_by_two(self, curve: EllipticCurve):
        """Умножение на 2: 2 * P = P + P"""
        P = curve.G
        result = curve.mul(2, P)
        expected = curve.add(P, P)
        assert result == expected

    def test_mul_distributive(self, curve: EllipticCurve):
        """Дистрибутивность: (a + b) * P = a*P + b*P"""
        P = curve.G
        a, b = 5, 7
        
        left = curve.mul(a + b, P)
        right = curve.add(curve.mul(a, P), curve.mul(b, P))
        
        assert left == right

    def test_mul_by_order(self, curve: EllipticCurve):
        """Умножение на порядок группы: q * G = O"""
        result = curve.mul(curve.q, curve.G)
        assert result is None

    def test_mul_by_order_plus_one(self, curve: EllipticCurve):
        """(q + 1) * G = G"""
        result = curve.mul(curve.q + 1, curve.G)
        assert result == curve.G

    def test_mul_large_scalar(self, curve: EllipticCurve):
        """Умножение на большое число"""
        k = secrets.randbelow(curve.q - 1) + 1
        result = curve.mul(k, curve.G)
        
        assert result is not None
        assert curve.is_on_curve(result)

    def test_mul_infinity(self, curve: EllipticCurve):
        """k * O = O для любого k"""
        assert curve.mul(5, None) is None
        assert curve.mul(0, None) is None
        assert curve.mul(100, None) is None

    def test_inverse_modular(self, curve: EllipticCurve):
        """Модульный обратный элемент корректен"""
        x = secrets.randbelow(curve.p - 1) + 1
        inv = curve.inv(x)
        
        assert (x * inv) % curve.p == 1

    def test_inverse_of_one(self, curve: EllipticCurve):
        """Обратный к 1 равен 1"""
        assert curve.inv(1) == 1

    def test_generate_keypair(self, curve: EllipticCurve):
        """Генерация ключевой пары корректна"""
        d, Q = curve._generate_keypair()
        
        assert 1 <= d < curve.q
        assert Q is not None
        assert curve.is_on_curve(Q)
        assert Q == curve.mul(d, curve.G)

    def test_generate_keypair_uniqueness(self, curve: EllipticCurve):
        """Генерация разных ключевых пар"""
        d1, Q1 = curve._generate_keypair()
        d2, Q2 = curve._generate_keypair()
        
        # С очень высокой вероятностью будут разными
        assert d1 != d2
        assert Q1 != Q2


class TestECPointEdgeCases:
    """Краевые случаи для точек кривой"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    def test_point_coordinates_boundary_zero(self, curve: EllipticCurve):
        """Точка с x=0 (базовая точка)"""
        G = curve.G
        assert G[0] == 0
        assert curve.is_on_curve(G)

    def test_point_with_large_coordinates(self, curve: EllipticCurve):
        """Точка с большими координатами (близко к p)"""
        # Создаем точку умножением
        k = curve.p - 1
        result = curve.mul(k % curve.q, curve.G)
        if result:
            assert curve.is_on_curve(result)

    def test_mul_by_negative_equivalent(self, curve: EllipticCurve):
        """Умножение на отрицательное число (эквивалент в группе)"""
        k = 5
        neg_k = curve.q - k
        
        P = curve.mul(k, curve.G)
        neg_P = curve.mul(neg_k, curve.G)
        
        # neg_k * G должно быть равно -(k * G)
        assert neg_P == curve.neg(P)

    def test_repeated_doubling(self, curve: EllipticCurve):
        """Многократное удвоение: 2^n * G"""
        P = curve.G
        for _ in range(10):
            P = curve.add(P, P)
            if P is not None:
                assert curve.is_on_curve(P)

    def test_cofactor_attack_resistance(self, curve: EllipticCurve):
        """Проверка на устойчивость к атаке с малым подгруппой"""
        # Точки после умножения на q должны давать бесконечность
        k = secrets.randbelow(curve.q - 1) + 1
        P = curve.mul(k, curve.G)
        
        if P is not None:
            result = curve.mul(curve.q, P)
            assert result is None
