"""
Тесты для схем дополнения (padding).

Тестируемые схемы:
- PKCS7: стандарт PKCS#7 (RFC 5652)
- ISO7816: ISO/IEC 7816-4 (bit padding)
- ANSI_X923: ANSI X9.23
- ISO10126: ISO 10126 (случайные байты)
- None: без дополнения
"""

import pytest
from crypto.padding import (
    PaddingFactory,
    PaddingScheme,
    PKCS7Padding,
    ISO7816Padding,
    ANSIX923Padding,
    ISO10126Padding,
    NonePadding,
)


# =============================================================================
# Padding Factory Tests
# =============================================================================

class TestPaddingFactory:
    """Тесты фабрики дополнений."""
    
    def test_create_pkcs7(self):
        """Создание PKCS7."""
        padding = PaddingFactory.create("pkcs7")
        assert isinstance(padding, PKCS7Padding)
    
    def test_create_pkcs5_alias(self):
        """PKCS5 - алиас PKCS7."""
        padding = PaddingFactory.create("pkcs5")
        assert isinstance(padding, PKCS7Padding)
    
    def test_create_iso7816(self):
        """Создание ISO7816."""
        padding = PaddingFactory.create("iso7816")
        assert isinstance(padding, ISO7816Padding)
    
    def test_create_ansi_x923(self):
        """Создание ANSI X9.23."""
        padding = PaddingFactory.create("ansi_x923")
        assert isinstance(padding, ANSIX923Padding)
    
    def test_create_x923_alias(self):
        """X923 - алиас ANSI X9.23."""
        padding = PaddingFactory.create("x923")
        assert isinstance(padding, ANSIX923Padding)
    
    def test_create_iso10126(self):
        """Создание ISO 10126."""
        padding = PaddingFactory.create("iso10126")
        assert isinstance(padding, ISO10126Padding)
    
    def test_create_none(self):
        """Создание None padding."""
        padding = PaddingFactory.create("none")
        assert isinstance(padding, NonePadding)
    
    def test_create_case_insensitive(self):
        """Имена не чувствительны к регистру."""
        assert isinstance(PaddingFactory.create("PKCS7"), PKCS7Padding)
        assert isinstance(PaddingFactory.create("Pkcs7"), PKCS7Padding)
    
    def test_create_unknown(self):
        """Неизвестная схема вызывает ошибку."""
        with pytest.raises(ValueError, match="не найдена"):
            PaddingFactory.create("unknown")
    
    def test_get_available(self):
        """Список доступных схем."""
        available = PaddingFactory.get_available()
        assert "PKCS7" in available
        assert "ISO7816" in available
        assert "ANSI_X923" in available
        assert "ISO10126" in available
        assert "NONE" in available


# =============================================================================
# PKCS7 Padding Tests
# =============================================================================

class TestPKCS7Padding:
    """Тесты PKCS#7 дополнения."""
    
    @pytest.fixture
    def padding(self):
        return PKCS7Padding()
    
    def test_name(self, padding):
        assert padding.name == "PKCS7"
    
    def test_pad_5_bytes_to_8(self, padding):
        """5 байт -> 8 байт (добавляем 3 байта 0x03)."""
        data = b"Hello"
        padded = padding.pad(data, 8)
        assert padded == b"Hello\x03\x03\x03"
        assert len(padded) == 8
    
    def test_pad_8_bytes_to_16(self, padding):
        """8 байт (кратно) -> 16 байт (добавляем полный блок)."""
        data = b"12345678"
        padded = padding.pad(data, 8)
        assert padded == b"12345678\x08\x08\x08\x08\x08\x08\x08\x08"
        assert len(padded) == 16
    
    def test_pad_1_byte_to_8(self, padding):
        """1 байт -> 8 байт (добавляем 7 байт 0x07)."""
        data = b"A"
        padded = padding.pad(data, 8)
        assert padded == b"A\x07\x07\x07\x07\x07\x07\x07"
    
    def test_pad_7_bytes_to_8(self, padding):
        """7 байт -> 8 байт (добавляем 1 байт 0x01)."""
        data = b"1234567"
        padded = padding.pad(data, 8)
        assert padded == b"1234567\x01"
    
    def test_pad_empty(self, padding):
        """Пустые данные -> полный блок дополнения."""
        padded = padding.pad(b"", 8)
        assert padded == b"\x08\x08\x08\x08\x08\x08\x08\x08"
    
    def test_unpad_valid(self, padding):
        """Корректное удаление дополнения."""
        data = b"Hello\x03\x03\x03"
        unpadded = padding.unpad(data, 8)
        assert unpadded == b"Hello"
    
    def test_unpad_full_block(self, padding):
        """Удаление полного блока дополнения."""
        data = b"12345678\x08\x08\x08\x08\x08\x08\x08\x08"
        unpadded = padding.unpad(data, 8)
        assert unpadded == b"12345678"
    
    def test_unpad_empty(self, padding):
        """Пустые данные."""
        assert padding.unpad(b"", 8) == b""
    
    def test_unpad_invalid_length_zero(self, padding):
        """Ошибка: длина дополнения = 0."""
        with pytest.raises(ValueError, match="длина 0"):
            padding.unpad(b"Hello\x00", 8)
    
    def test_unpad_invalid_length_too_large(self, padding):
        """Ошибка: длина дополнения > размера блока."""
        with pytest.raises(ValueError, match="длина 9"):
            padding.unpad(b"Hello\x09", 8)
    
    def test_unpad_invalid_bytes(self, padding):
        """Ошибка: байты дополнения не совпадают."""
        with pytest.raises(ValueError, match="не совпадают"):
            padding.unpad(b"Hello\x03\x03\x02", 8)
    
    def test_roundtrip(self, padding):
        """Цикл pad -> unpad возвращает исходные данные."""
        original = b"Test data!"
        padded = padding.pad(original, 8)
        unpadded = padding.unpad(padded, 8)
        assert unpadded == original


# =============================================================================
# ISO7816 Padding Tests
# =============================================================================

class TestISO7816Padding:
    """Тесты ISO/IEC 7816-4 дополнения."""
    
    @pytest.fixture
    def padding(self):
        return ISO7816Padding()
    
    def test_name(self, padding):
        assert padding.name == "ISO7816"
    
    def test_pad_5_bytes_to_8(self, padding):
        """5 байт -> 8 байт (0x80 + 2 нуля)."""
        data = b"Hello"
        padded = padding.pad(data, 8)
        assert padded == b"Hello\x80\x00\x00"
    
    def test_pad_8_bytes_to_16(self, padding):
        """8 байт (кратно) -> 16 байт (полный блок дополнения)."""
        data = b"12345678"
        padded = padding.pad(data, 8)
        assert padded == b"12345678\x80\x00\x00\x00\x00\x00\x00\x00"
    
    def test_pad_7_bytes_to_8(self, padding):
        """7 байт -> 8 байт (только 0x80)."""
        data = b"1234567"
        padded = padding.pad(data, 8)
        assert padded == b"1234567\x80"
    
    def test_unpad_valid(self, padding):
        """Корректное удаление дополнения."""
        data = b"Hello\x80\x00\x00"
        unpadded = padding.unpad(data, 8)
        assert unpadded == b"Hello"
    
    def test_unpad_only_marker(self, padding):
        """Удаление только маркера 0x80."""
        data = b"1234567\x80"
        unpadded = padding.unpad(data, 8)
        assert unpadded == b"1234567"
    
    def test_unpad_invalid(self, padding):
        """Ошибка: маркер 0x80 не найден."""
        with pytest.raises(ValueError, match="маркер 0x80 не найден"):
            padding.unpad(b"Hello\x00\x00\x00", 8)
    
    def test_roundtrip(self, padding):
        """Цикл pad -> unpad."""
        original = b"ISO7816 test"
        padded = padding.pad(original, 8)
        unpadded = padding.unpad(padded, 8)
        assert unpadded == original


# =============================================================================
# ANSI X9.23 Padding Tests
# =============================================================================

class TestANSIX923Padding:
    """Тесты ANSI X9.23 дополнения."""
    
    @pytest.fixture
    def padding(self):
        return ANSIX923Padding()
    
    def test_name(self, padding):
        assert padding.name == "ANSI_X923"
    
    def test_pad_5_bytes_to_8(self, padding):
        """5 байт -> 8 байт (нули + 0x03)."""
        data = b"Hello"
        padded = padding.pad(data, 8)
        assert padded == b"Hello\x00\x00\x03"
    
    def test_pad_8_bytes_to_16(self, padding):
        """8 байт (кратно) -> 16 байт."""
        data = b"12345678"
        padded = padding.pad(data, 8)
        assert padded == b"12345678\x00\x00\x00\x00\x00\x00\x00\x08"
    
    def test_pad_7_bytes_to_8(self, padding):
        """7 байт -> 8 байт (только 0x01)."""
        data = b"1234567"
        padded = padding.pad(data, 8)
        assert padded == b"1234567\x01"
    
    def test_unpad_valid(self, padding):
        """Корректное удаление дополнения."""
        data = b"Hello\x00\x00\x03"
        unpadded = padding.unpad(data, 8)
        assert unpadded == b"Hello"
    
    def test_unpad_invalid_not_zeros(self, padding):
        """Ошибка: байты не нулевые."""
        with pytest.raises(ValueError, match="не все байты нулевые"):
            padding.unpad(b"Hello\x01\x00\x03", 8)
    
    def test_unpad_invalid_length(self, padding):
        """Ошибка: некорректная длина."""
        with pytest.raises(ValueError, match="длина 0"):
            padding.unpad(b"Hello\x00", 8)
    
    def test_roundtrip(self, padding):
        """Цикл pad -> unpad."""
        original = b"ANSI test"
        padded = padding.pad(original, 8)
        unpadded = padding.unpad(padded, 8)
        assert unpadded == original


# =============================================================================
# ISO 10126 Padding Tests
# =============================================================================

class TestISO10126Padding:
    """Тесты ISO 10126 дополнения (случайные байты)."""
    
    @pytest.fixture
    def padding(self):
        return ISO10126Padding()
    
    def test_name(self, padding):
        assert padding.name == "ISO10126"
    
    def test_pad_length(self, padding):
        """Проверяем корректную длину после дополнения."""
        data = b"Hello"
        padded = padding.pad(data, 8)
        assert len(padded) == 8
        assert padded[-1] == 3
    
    def test_pad_starts_with_original(self, padding):
        """Padded данные начинаются с оригинала."""
        data = b"Hello"
        padded = padding.pad(data, 8)
        assert padded[:5] == data
    
    def test_pad_8_bytes_to_16(self, padding):
        """8 байт (кратно) -> 16 байт."""
        data = b"12345678"
        padded = padding.pad(data, 8)
        assert len(padded) == 16
        assert padded[-1] == 8
        assert padded[:8] == data
    
    def test_unpad_valid(self, padding):
        """Корректное удаление дополнения."""
        data = b"Hello\xAB\xCD\x03"
        unpadded = padding.unpad(data, 8)
        assert unpadded == b"Hello"
    
    def test_unpad_invalid_length(self, padding):
        """Ошибка: некорректная длина."""
        with pytest.raises(ValueError, match="длина 0"):
            padding.unpad(b"Hello\x00", 8)
    
    def test_roundtrip(self, padding):
        """Цикл pad -> unpad."""
        original = b"ISO 10126 random test"
        padded = padding.pad(original, 8)
        unpadded = padding.unpad(padded, 8)
        assert unpadded == original


# =============================================================================
# None Padding Tests
# =============================================================================

class TestNonePadding:
    """Тесты отсутствия дополнения."""
    
    @pytest.fixture
    def padding(self):
        return NonePadding()
    
    def test_name(self, padding):
        assert padding.name == "None"
    
    def test_pad_aligned(self, padding):
        """Данные кратны блоку - возвращаются без изменений."""
        data = b"12345678"
        assert padding.pad(data, 8) == data
    
    def test_pad_not_aligned_error(self, padding):
        """Данные не кратны блоку - ошибка."""
        data = b"Hello"
        with pytest.raises(ValueError, match="должна быть кратна"):
            padding.pad(data, 8)
    
    def test_unpad_passthrough(self, padding):
        """unpad возвращает данные без изменений."""
        data = b"12345678"
        assert padding.unpad(data, 8) == data
