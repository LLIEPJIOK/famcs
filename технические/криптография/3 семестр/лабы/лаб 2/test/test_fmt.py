"""
Тесты для модуля fmt.py - сериализация/десериализация
"""

import pytest
import sys
import os

# Добавляем путь к app в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from crypto.fmt import (
    serialize_bytes,
    serialize_int,
    serialize_point,
    deserialize_point,
)
from crypto.elliptic import EllipticCurve


class TestSerializeBytes:
    """Тесты для функции serialize_bytes"""

    def test_serialize_bytes_exact_length(self):
        """Сериализация bytes точной длины"""
        data = b'\x01\x02\x03\x04'
        result = serialize_bytes(data, 32)  # 4 байта
        assert result == data

    def test_serialize_bytes_shorter(self):
        """Сериализация bytes короче целевой длины - дополнение нулями"""
        data = b'\x01\x02'
        result = serialize_bytes(data, 32)  # 4 байта
        assert len(result) == 4
        assert result == b'\x01\x02\x00\x00'

    def test_serialize_bytes_longer(self):
        """Сериализация bytes длиннее целевой длины - обрезка"""
        data = b'\x01\x02\x03\x04\x05\x06'
        result = serialize_bytes(data, 32)  # 4 байта
        assert len(result) == 4
        assert result == b'\x01\x02\x03\x04'

    def test_serialize_bytes_empty(self):
        """Сериализация пустых данных"""
        data = b''
        result = serialize_bytes(data, 32)
        assert len(result) == 4
        assert result == b'\x00\x00\x00\x00'

    def test_serialize_bytes_invalid_bit_length(self):
        """Невалидная bit_length (не кратна 8)"""
        with pytest.raises(ValueError, match="invalid bit length"):
            serialize_bytes(b'\x01', 31)

    def test_serialize_bytes_zero_bit_length(self):
        """Нулевая bit_length"""
        result = serialize_bytes(b'\x01\x02\x03', 0)
        assert result == b''


class TestSerializeInt:
    """Тесты для функции serialize_int"""

    def test_serialize_int_zero(self):
        """Сериализация нуля"""
        result = serialize_int(0, 32)
        assert result == b'\x00\x00\x00\x00'

    def test_serialize_int_one(self):
        """Сериализация единицы"""
        result = serialize_int(1, 32)
        assert result == b'\x01\x00\x00\x00'

    def test_serialize_int_max_value(self):
        """Сериализация максимального значения для заданной длины"""
        result = serialize_int(0xFFFFFFFF, 32)
        assert result == b'\xff\xff\xff\xff'

    def test_serialize_int_little_endian(self):
        """Проверка little-endian порядка байтов"""
        result = serialize_int(0x12345678, 32)
        assert result == b'\x78\x56\x34\x12'

    def test_serialize_int_large_number(self):
        """Сериализация большого числа"""
        large_num = 2**256 - 1
        result = serialize_int(large_num, 256)
        assert len(result) == 32
        assert result == b'\xff' * 32

    def test_serialize_int_bit_length_not_multiple_of_8(self):
        """bit_length не кратен 8 - округление вверх"""
        result = serialize_int(0xFF, 9)
        assert len(result) == 2  # (9 + 7) // 8 = 2

    def test_serialize_int_overflow(self):
        """Число больше, чем можно вместить - вызывает исключение"""
        # 0x1FF требует 9 бит, но мы даем только 8
        # Python to_bytes выбрасывает OverflowError
        with pytest.raises(OverflowError):
            serialize_int(0x1FF, 8)


class TestSerializePoint:
    """Тесты для функции serialize_point"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    def test_serialize_point_base_point(self, curve: EllipticCurve):
        """Сериализация базовой точки"""
        result = serialize_point(curve.G, curve.l, 4 * curve.l)
        assert len(result) == 4 * curve.l // 8

    def test_serialize_point_half_length(self, curve: EllipticCurve):
        """Сериализация с укороченной длиной (2*l)"""
        result = serialize_point(curve.G, curve.l, 2 * curve.l)
        assert len(result) == 2 * curve.l // 8

    def test_serialize_point_infinity(self, curve: EllipticCurve):
        """Сериализация точки на бесконечности должна выбросить исключение"""
        with pytest.raises(ValueError, match="cannot serialize point at infinity"):
            serialize_point(None, curve.l, 4 * curve.l)

    def test_serialize_point_invalid_bit_length_not_multiple(self, curve: EllipticCurve):
        """Невалидная bit_length (не кратна 8)"""
        with pytest.raises(ValueError, match="invalid n"):
            serialize_point(curve.G, curve.l, 127)

    def test_serialize_point_bit_length_too_large(self, curve: EllipticCurve):
        """bit_length больше 4*l"""
        with pytest.raises(ValueError, match="invalid n"):
            serialize_point(curve.G, curve.l, 5 * curve.l)

    def test_serialize_point_roundtrip(self, curve: EllipticCurve):
        """Сериализация и десериализация дают исходную точку"""
        P = curve.mul(12345, curve.G)
        serialized = serialize_point(P, curve.l, 4 * curve.l)
        deserialized = deserialize_point(serialized, curve.l)
        assert deserialized == P


class TestDeserializePoint:
    """Тесты для функции deserialize_point"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    def test_deserialize_point_valid(self, curve: EllipticCurve):
        """Десериализация валидных данных"""
        P = curve.G
        serialized = serialize_point(P, curve.l, 4 * curve.l)
        result = deserialize_point(serialized, curve.l)
        assert result == P

    def test_deserialize_point_wrong_length(self, curve: EllipticCurve):
        """Десериализация с неправильной длиной данных"""
        data = b'\x00' * 10  # Неправильная длина
        with pytest.raises(ValueError, match="cannot deserialize"):
            deserialize_point(data, curve.l)

    def test_deserialize_point_empty(self, curve: EllipticCurve):
        """Десериализация пустых данных"""
        with pytest.raises(ValueError, match="cannot deserialize"):
            deserialize_point(b'', curve.l)

    def test_deserialize_point_all_zeros(self, curve: EllipticCurve):
        """Десериализация нулевых данных"""
        data = b'\x00' * (4 * curve.l // 8)
        result = deserialize_point(data, curve.l)
        assert result == (0, 0)

    def test_deserialize_point_multiple_roundtrips(self, curve: EllipticCurve):
        """Множественные roundtrip сериализации"""
        P = curve.mul(99999, curve.G)
        
        for _ in range(5):
            serialized = serialize_point(P, curve.l, 4 * curve.l)
            P = deserialize_point(serialized, curve.l)
        
        expected = curve.mul(99999, curve.G)
        assert P == expected


class TestEdgeCasesIntegration:
    """Интеграционные тесты для краевых случаев"""

    @pytest.fixture
    def curve(self) -> EllipticCurve:
        return EllipticCurve.default_curve()

    def test_serialize_max_coordinate_point(self, curve: EllipticCurve):
        """Точка с максимальными координатами"""
        # Создаем точку близкую к максимуму
        P = curve.mul(curve.q - 1, curve.G)
        if P is not None:
            serialized = serialize_point(P, curve.l, 4 * curve.l)
            deserialized = deserialize_point(serialized, curve.l)
            assert deserialized == P

    def test_serialize_after_many_operations(self, curve: EllipticCurve):
        """Сериализация после многих операций"""
        P = curve.G
        for i in range(1, 20):
            P = curve.add(P, curve.mul(i, curve.G))
            if P is None:
                continue
            
            serialized = serialize_point(P, curve.l, 4 * curve.l)
            deserialized = deserialize_point(serialized, curve.l)
            assert deserialized == P

    def test_different_l_values(self):
        """Тест с разными значениями l (если поддерживается)"""
        # Стандартная кривая имеет l=128
        curve = EllipticCurve.default_curve()
        assert curve.l == 128
        
        P = curve.G
        serialized = serialize_point(P, curve.l, 4 * curve.l)
        assert len(serialized) == 64  # 4 * 128 / 8 = 64
