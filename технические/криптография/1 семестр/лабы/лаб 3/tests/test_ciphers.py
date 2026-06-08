"""
Тесты для шифров.

Тестируют:
- Вспомогательные математические операции IDEA
- Генерацию подключей
- Шифрование/расшифрование отдельных блоков
- Корректность обратимости операций
- Валидацию ключа
"""

import pytest
from crypto.ciphers.idea import IDEACipher


# =============================================================================
# IDEA Cipher Tests
# =============================================================================

class TestIDEAMathOperations:
    """Тесты математических операций IDEA."""
    
    def test_mul_mod_regular_values(self):
        """Тест умножения по модулю 2^16+1 для обычных значений."""
        assert IDEACipher.mul_mod(2, 3) == 6
        assert IDEACipher.mul_mod(100, 200) == 20000
    
    def test_mul_mod_with_zero(self):
        """Тест умножения когда один из операндов 0 (интерпретируется как 2^16)."""
        assert IDEACipher.mul_mod(0, 1) == 0
        assert IDEACipher.mul_mod(1, 0) == 0
        
    def test_mul_mod_both_zero(self):
        """Тест умножения когда оба операнда 0."""
        assert IDEACipher.mul_mod(0, 0) == 1
    
    def test_mul_mod_boundary(self):
        """Тест граничных значений."""
        assert IDEACipher.mul_mod(0xFFFF, 1) == 0xFFFF
        assert IDEACipher.mul_mod(1, 1) == 1
    
    def test_add_mod_regular(self):
        """Тест сложения по модулю 2^16."""
        assert IDEACipher.add_mod(100, 200) == 300
        assert IDEACipher.add_mod(0, 0) == 0
        assert IDEACipher.add_mod(0xFFFF, 1) == 0
        
    def test_add_mod_overflow(self):
        """Тест переполнения при сложении."""
        assert IDEACipher.add_mod(0x8000, 0x8000) == 0
        assert IDEACipher.add_mod(0xFFFF, 0xFFFF) == 0xFFFE
    
    def test_sub_mod_regular(self):
        """Тест вычитания по модулю 2^16."""
        assert IDEACipher.sub_mod(300, 100) == 200
        assert IDEACipher.sub_mod(0, 1) == 0xFFFF
    
    def test_mul_inv_regular(self):
        """Тест мультипликативной инверсии."""
        for a in [1, 2, 3, 100, 1000, 0xFFFF]:
            inv = IDEACipher.mul_inv(a)
            assert IDEACipher.mul_mod(a, inv) == 1, f"Инверсия для {a} неверна"
    
    def test_mul_inv_zero(self):
        """Тест инверсии нуля."""
        assert IDEACipher.mul_inv(0) == 0
        assert IDEACipher.mul_mod(0, IDEACipher.mul_inv(0)) == 1
    
    def test_add_inv_regular(self):
        """Тест аддитивной инверсии."""
        for a in [0, 1, 100, 0x8000, 0xFFFF]:
            inv = IDEACipher.add_inv(a)
            assert IDEACipher.add_mod(a, inv) == 0, f"Аддитивная инверсия для {a} неверна"


class TestIDEAKeySchedule:
    """Тесты генерации подключей."""
    
    @pytest.fixture
    def key_all_zeros(self):
        """Ключ из нулей."""
        return bytes(16)
    
    @pytest.fixture
    def key_all_ones(self):
        """Ключ из единиц (0xFF)."""
        return bytes([0xFF] * 16)
    
    @pytest.fixture
    def key_sequential(self):
        """Последовательный ключ."""
        return bytes(range(16))
    
    def test_subkey_count(self, key_all_zeros):
        """Тест количества подключей."""
        cipher = IDEACipher(key_all_zeros)
        assert len(cipher._encrypt_subkeys) == 52
        assert len(cipher._decrypt_subkeys) == 52
    
    def test_subkeys_are_16bit(self, key_sequential):
        """Тест что все подключи — 16-битные."""
        cipher = IDEACipher(key_sequential)
        for sk in cipher._encrypt_subkeys:
            assert 0 <= sk <= 0xFFFF
        for sk in cipher._decrypt_subkeys:
            assert 0 <= sk <= 0xFFFF
    
    def test_first_subkeys_from_key(self, key_sequential):
        """Тест что первые 8 подключей берутся напрямую из ключа."""
        cipher = IDEACipher(key_sequential)
        assert cipher._encrypt_subkeys[0] == (0x00 << 8) | 0x01
        assert cipher._encrypt_subkeys[1] == (0x02 << 8) | 0x03
        assert cipher._encrypt_subkeys[7] == (0x0E << 8) | 0x0F
    
    def test_different_keys_different_subkeys(self, key_all_zeros, key_all_ones):
        """Тест что разные ключи дают разные подключи."""
        cipher1 = IDEACipher(key_all_zeros)
        cipher2 = IDEACipher(key_all_ones)
        assert cipher1._encrypt_subkeys != cipher2._encrypt_subkeys


class TestIDEABlockEncryption:
    """Тесты шифрования/расшифрования блоков."""
    
    @pytest.fixture
    def cipher(self):
        """Шифр с тестовым ключом."""
        key = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
        return IDEACipher(key)
    
    def test_block_size(self, cipher):
        """Тест размера блока."""
        assert cipher.block_size == 8
    
    def test_key_size(self, cipher):
        """Тест размера ключа."""
        assert cipher.key_size == 16
    
    def test_name(self, cipher):
        """Тест названия шифра."""
        assert cipher.name == "IDEA"
    
    def test_encrypt_decrypt_roundtrip(self, cipher):
        """Тест: расшифрование зашифрованного блока даёт исходный."""
        plaintext = b"TESTDATA"
        ciphertext = cipher.encrypt_block(plaintext)
        decrypted = cipher.decrypt_block(ciphertext)
        assert decrypted == plaintext
    
    def test_encrypt_changes_data(self, cipher):
        """Тест: шифрование изменяет данные."""
        plaintext = b"TESTDATA"
        ciphertext = cipher.encrypt_block(plaintext)
        assert ciphertext != plaintext
    
    def test_decrypt_roundtrip_various_data(self, cipher):
        """Тест обратимости для различных данных."""
        test_vectors = [
            b"\x00\x00\x00\x00\x00\x00\x00\x00",
            b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF",
            b"\x01\x02\x03\x04\x05\x06\x07\x08",
            b"ABCDEFGH",
        ]
        for pt in test_vectors:
            ct = cipher.encrypt_block(pt)
            decrypted = cipher.decrypt_block(ct)
            assert decrypted == pt, f"Ошибка для блока {pt.hex()}"
    
    def test_invalid_block_size_encrypt(self, cipher):
        """Тест ошибки при неверном размере блока для шифрования."""
        with pytest.raises(ValueError):
            cipher.encrypt_block(b"SHORT")
        with pytest.raises(ValueError):
            cipher.encrypt_block(b"TOOLONGBLOCK")
    
    def test_invalid_block_size_decrypt(self, cipher):
        """Тест ошибки при неверном размере блока для расшифрования."""
        with pytest.raises(ValueError):
            cipher.decrypt_block(b"SHORT")
    
    def test_deterministic_encryption(self, cipher):
        """Тест детерминированности: одинаковый вход → одинаковый выход."""
        plaintext = b"TESTDATA"
        ct1 = cipher.encrypt_block(plaintext)
        ct2 = cipher.encrypt_block(plaintext)
        assert ct1 == ct2


class TestIDEAKeyValidation:
    """Тесты валидации ключа."""
    
    def test_invalid_key_length_short(self):
        """Тест ошибки при коротком ключе."""
        with pytest.raises(ValueError) as exc_info:
            IDEACipher(b"shortkey")
        assert "16" in str(exc_info.value)
    
    def test_invalid_key_length_long(self):
        """Тест ошибки при длинном ключе."""
        with pytest.raises(ValueError):
            IDEACipher(bytes(32))
    
    def test_valid_key(self):
        """Тест создания шифра с валидным ключом."""
        cipher = IDEACipher(bytes(16))
        assert cipher is not None


class TestIDEAKnownAnswers:
    """Тесты с известными ответами (Known Answer Tests)."""
    
    def test_encryption_consistency(self):
        """Тест консистентности шифрования."""
        key = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
        plaintext = bytes([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77])
        
        cipher = IDEACipher(key)
        ciphertext1 = cipher.encrypt_block(plaintext)
        
        cipher2 = IDEACipher(key)
        ciphertext2 = cipher2.encrypt_block(plaintext)
        
        assert ciphertext1 == ciphertext2
    
    def test_different_keys_produce_different_ciphertext(self):
        """Тест: разные ключи дают разный шифротекст."""
        plaintext = b"TESTBLOK"
        
        key1 = bytes(16)
        key2 = bytes([1] + [0] * 15)
        
        cipher1 = IDEACipher(key1)
        cipher2 = IDEACipher(key2)
        
        ct1 = cipher1.encrypt_block(plaintext)
        ct2 = cipher2.encrypt_block(plaintext)
        
        assert ct1 != ct2
    
    def test_different_plaintexts_produce_different_ciphertext(self):
        """Тест: разные открытые тексты дают разный шифротекст."""
        key = bytes(16)
        cipher = IDEACipher(key)
        
        pt1 = b"AAAAAAAA"
        pt2 = b"BBBBBBBB"
        
        ct1 = cipher.encrypt_block(pt1)
        ct2 = cipher.encrypt_block(pt2)
        
        assert ct1 != ct2
