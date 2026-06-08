"""
Тесты для режимов шифрования.

Тестируют:
- ECB (Electronic Codebook)
- CBC (Cipher Block Chaining)
- PCBC (Propagating Cipher Block Chaining)
- CFB (Cipher Feedback)
- OFB (Output Feedback)
- CTR (Counter)
"""

import pytest
from crypto.ciphers.idea import IDEACipher
from crypto.modes.ecb import ECBMode
from crypto.modes.cbc import CBCMode
from crypto.modes.pcbc import PCBCMode
from crypto.modes.cfb import CFBMode
from crypto.modes.ofb import OFBMode
from crypto.modes.ctr import CTRMode


# =============================================================================
# ECB Mode Tests
# =============================================================================

class TestECBBlockSplitting:
    """Тесты разбиения на блоки в ECB."""
    
    @pytest.fixture
    def ecb(self):
        return ECBMode()
    
    def test_split_exact_blocks(self, ecb):
        """Тест разбиения данных, кратных размеру блока."""
        data = bytes(range(16))
        blocks = ecb._split_into_blocks(data, 8)
        assert len(blocks) == 2
        assert blocks[0] == bytes(range(8))
        assert blocks[1] == bytes(range(8, 16))
    
    def test_split_with_padding(self, ecb):
        """Тест разбиения с дополнением последнего блока."""
        data = bytes(range(10))
        blocks = ecb._split_into_blocks(data, 8)
        assert len(blocks) == 2
        assert blocks[0] == bytes(range(8))
        assert blocks[1] == bytes([8, 9, 0, 0, 0, 0, 0, 0])
    
    def test_split_single_block(self, ecb):
        """Тест разбиения одного полного блока."""
        data = bytes(range(8))
        blocks = ecb._split_into_blocks(data, 8)
        assert len(blocks) == 1
        assert blocks[0] == data
    
    def test_split_partial_block(self, ecb):
        """Тест разбиения неполного блока."""
        data = bytes([1, 2, 3])
        blocks = ecb._split_into_blocks(data, 8)
        assert len(blocks) == 1
        assert blocks[0] == bytes([1, 2, 3, 0, 0, 0, 0, 0])
    
    def test_split_empty(self, ecb):
        """Тест разбиения пустых данных."""
        blocks = ecb._split_into_blocks(bytes(), 8)
        assert len(blocks) == 0


class TestECBEncryption:
    """Тесты шифрования в режиме ECB."""
    
    @pytest.fixture
    def cipher(self):
        return IDEACipher(bytes(range(16)))
    
    @pytest.fixture
    def ecb(self):
        return ECBMode()
    
    def test_name(self, ecb):
        """Тест названия режима."""
        assert ecb.name == "ECB"
    
    def test_encrypt_single_block(self, ecb, cipher):
        """Тест шифрования одного блока."""
        plaintext = b"TESTDATA"
        ciphertext = ecb.encrypt(plaintext, cipher)
        assert len(ciphertext) == 8
        assert ciphertext != plaintext
    
    def test_encrypt_multiple_blocks(self, ecb, cipher):
        """Тест шифрования нескольких блоков."""
        plaintext = b"TESTDATA" * 3
        ciphertext = ecb.encrypt(plaintext, cipher)
        assert len(ciphertext) == 24
    
    def test_encrypt_with_padding(self, ecb, cipher):
        """Тест шифрования с дополнением."""
        plaintext = b"TEST"
        ciphertext = ecb.encrypt(plaintext, cipher)
        assert len(ciphertext) == 8
    
    def test_encrypt_empty(self, ecb, cipher):
        """Тест шифрования пустых данных."""
        ciphertext = ecb.encrypt(bytes(), cipher)
        assert ciphertext == bytes()
    
    def test_identical_blocks_produce_identical_ciphertext(self, ecb, cipher):
        """Тест: одинаковые блоки дают одинаковый шифротекст (уязвимость ECB)."""
        plaintext = b"AAAAAAAA" * 2
        ciphertext = ecb.encrypt(plaintext, cipher)
        assert ciphertext[:8] == ciphertext[8:16]


class TestECBDecryption:
    """Тесты расшифрования в режиме ECB."""
    
    @pytest.fixture
    def cipher(self):
        return IDEACipher(bytes(range(16)))
    
    @pytest.fixture
    def ecb(self):
        return ECBMode()
    
    def test_decrypt_single_block(self, ecb, cipher):
        """Тест расшифрования одного блока."""
        plaintext = b"TESTDATA"
        ciphertext = ecb.encrypt(plaintext, cipher)
        decrypted = ecb.decrypt(ciphertext, cipher)
        assert decrypted == plaintext
    
    def test_decrypt_multiple_blocks(self, ecb, cipher):
        """Тест расшифрования нескольких блоков."""
        plaintext = b"ABCDEFGH" + b"12345678" + b"ZYXWVUTS"
        ciphertext = ecb.encrypt(plaintext, cipher)
        decrypted = ecb.decrypt(ciphertext, cipher)
        assert decrypted == plaintext
    
    def test_decrypt_empty(self, ecb, cipher):
        """Тест расшифрования пустых данных."""
        decrypted = ecb.decrypt(bytes(), cipher)
        assert decrypted == bytes()
    
    def test_decrypt_invalid_length(self, ecb, cipher):
        """Тест ошибки при некратной длине шифротекста."""
        with pytest.raises(ValueError) as exc_info:
            ecb.decrypt(bytes(10), cipher)
        assert "кратна" in str(exc_info.value).lower() or "кратн" in str(exc_info.value).lower()


class TestECBRoundtrip:
    """Тесты полного цикла шифрования-расшифрования ECB."""
    
    @pytest.fixture
    def cipher(self):
        key = bytes([0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45, 0x67, 0x89,
                     0x98, 0x76, 0x54, 0x32, 0x10, 0xFE, 0xDC, 0xBA])
        return IDEACipher(key)
    
    @pytest.fixture
    def ecb(self):
        return ECBMode()
    
    def test_roundtrip_exact_blocks(self, ecb, cipher):
        """Тест полного цикла для данных кратных размеру блока."""
        original = b"EXACTBLK"
        encrypted = ecb.encrypt(original, cipher)
        decrypted = ecb.decrypt(encrypted, cipher)
        assert decrypted == original
    
    def test_roundtrip_multiple_blocks(self, ecb, cipher):
        """Тест полного цикла для нескольких блоков."""
        original = bytes(range(64))
        encrypted = ecb.encrypt(original, cipher)
        decrypted = ecb.decrypt(encrypted, cipher)
        assert decrypted == original
    
    def test_roundtrip_all_zeros(self, ecb, cipher):
        """Тест с нулевыми данными."""
        original = bytes(16)
        encrypted = ecb.encrypt(original, cipher)
        decrypted = ecb.decrypt(encrypted, cipher)
        assert decrypted == original
    
    def test_roundtrip_all_ones(self, ecb, cipher):
        """Тест с данными из 0xFF."""
        original = bytes([0xFF] * 24)
        encrypted = ecb.encrypt(original, cipher)
        decrypted = ecb.decrypt(encrypted, cipher)
        assert decrypted == original


# =============================================================================
# CBC Mode Tests
# =============================================================================

class TestCBCMode:
    """Тесты для режима CBC."""
    
    @pytest.fixture
    def cipher(self):
        return IDEACipher(bytes(range(16)))
    
    @pytest.fixture
    def iv(self):
        return bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
    
    def test_name(self):
        """Проверка названия режима."""
        mode = CBCMode()
        assert mode.name == "CBC"
    
    def test_encrypt_decrypt_one_block(self, cipher, iv):
        """Шифрование/расшифрование одного блока."""
        mode = CBCMode(iv)
        plaintext = b"12345678"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
        assert ciphertext != plaintext
    
    def test_encrypt_decrypt_multiple_blocks(self, cipher, iv):
        """Шифрование/расшифрование нескольких блоков."""
        mode = CBCMode(iv)
        plaintext = b"Hello, CBC mode encryption test!"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
    
    def test_different_iv_different_ciphertext(self, cipher):
        """Разные IV дают разный шифротекст."""
        iv1 = bytes([0x01] * 8)
        iv2 = bytes([0x02] * 8)
        plaintext = b"TestData"
        
        mode1 = CBCMode(iv1)
        mode2 = CBCMode(iv2)
        
        ciphertext1 = mode1.encrypt(plaintext, cipher)
        ciphertext2 = mode2.encrypt(plaintext, cipher)
        
        assert ciphertext1 != ciphertext2
    
    def test_identical_blocks_different_ciphertext(self, cipher, iv):
        """Одинаковые блоки открытого текста → разный шифротекст (в отличие от ECB)."""
        mode = CBCMode(iv)
        plaintext = b"AAAAAAAAAAAAAAAA"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        
        assert ciphertext[:8] != ciphertext[8:16]
    
    def test_no_iv_raises_error(self, cipher):
        """Шифрование без IV вызывает ошибку."""
        mode = CBCMode()
        with pytest.raises(ValueError, match="IV.*не установлен"):
            mode.encrypt(b"TestData", cipher)
    
    def test_wrong_iv_size_raises_error(self, cipher):
        """Неправильный размер IV вызывает ошибку."""
        mode = CBCMode(iv=b"short")
        with pytest.raises(ValueError, match="размер"):
            mode.encrypt(b"TestData", cipher)
    
    def test_empty_data(self, cipher, iv):
        """Шифрование пустых данных."""
        mode = CBCMode(iv)
        assert mode.encrypt(b"", cipher) == b""
        assert mode.decrypt(b"", cipher) == b""
    
    def test_set_iv(self, cipher):
        """Установка IV через метод set_iv."""
        mode = CBCMode()
        iv = bytes([0x11] * 8)
        mode.set_iv(iv)
        
        plaintext = b"TestData"
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext


# =============================================================================
# PCBC Mode Tests
# =============================================================================

class TestPCBCMode:
    """Тесты для режима PCBC (Propagating Cipher Block Chaining)."""
    
    @pytest.fixture
    def cipher(self):
        return IDEACipher(bytes(range(16)))
    
    @pytest.fixture
    def iv(self):
        return bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
    
    def test_name(self):
        """Проверка названия режима."""
        mode = PCBCMode()
        assert mode.name == "PCBC"
    
    def test_encrypt_decrypt_one_block(self, cipher, iv):
        """Шифрование/расшифрование одного блока."""
        mode = PCBCMode(iv)
        plaintext = b"12345678"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
        assert ciphertext != plaintext
        assert len(ciphertext) == 8
    
    def test_encrypt_decrypt_multiple_blocks(self, cipher, iv):
        """Шифрование/расшифрование нескольких блоков."""
        mode = PCBCMode(iv)
        plaintext = b"Hello, PCBC mode encryption test"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
        assert len(ciphertext) == 32
    
    def test_different_iv_different_ciphertext(self, cipher):
        """Разные IV дают разный шифротекст."""
        iv1 = bytes([0x01] * 8)
        iv2 = bytes([0x02] * 8)
        plaintext = b"TestData"
        
        mode1 = PCBCMode(iv1)
        mode2 = PCBCMode(iv2)
        
        ciphertext1 = mode1.encrypt(plaintext, cipher)
        ciphertext2 = mode2.encrypt(plaintext, cipher)
        
        assert ciphertext1 != ciphertext2
    
    def test_identical_blocks_different_ciphertext(self, cipher, iv):
        """Одинаковые блоки открытого текста → разный шифротекст."""
        mode = PCBCMode(iv)
        plaintext = b"AAAAAAAAAAAAAAAA"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        
        assert ciphertext[:8] != ciphertext[8:16]
    
    def test_no_iv_raises_error(self, cipher):
        """Шифрование без IV вызывает ошибку."""
        mode = PCBCMode()
        with pytest.raises(ValueError, match="IV"):
            mode.encrypt(b"TestData", cipher)
    
    def test_wrong_iv_size_raises_error(self, cipher):
        """Неправильный размер IV вызывает ошибку."""
        mode = PCBCMode(iv=b"short")
        with pytest.raises(ValueError, match="размер"):
            mode.encrypt(b"TestData", cipher)
    
    def test_empty_data(self, cipher, iv):
        """Шифрование пустых данных."""
        mode = PCBCMode(iv)
        assert mode.encrypt(b"", cipher) == b""
        assert mode.decrypt(b"", cipher) == b""
    
    def test_set_iv(self, cipher):
        """Установка IV через метод set_iv."""
        mode = PCBCMode()
        iv = bytes([0x11] * 8)
        mode.set_iv(iv)
        
        plaintext = b"TestData"
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
    
    def test_invalid_plaintext_length(self, cipher, iv):
        """Ошибка при некратной длине открытого текста."""
        mode = PCBCMode(iv)
        with pytest.raises(ValueError, match="кратна"):
            mode.encrypt(b"Short", cipher)
    
    def test_invalid_ciphertext_length(self, cipher, iv):
        """Ошибка при некратной длине шифротекста."""
        mode = PCBCMode(iv)
        with pytest.raises(ValueError, match="кратна"):
            mode.decrypt(b"Short", cipher)


# =============================================================================
# CFB Mode Tests
# =============================================================================

class TestCFBMode:
    """Тесты для режима CFB."""
    
    @pytest.fixture
    def cipher(self):
        return IDEACipher(bytes(range(16)))
    
    @pytest.fixture
    def iv(self):
        return bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
    
    def test_name(self):
        """Проверка названия режима."""
        mode = CFBMode()
        assert mode.name == "CFB"
    
    def test_encrypt_decrypt_full_block(self, cipher, iv):
        """Шифрование/расшифрование полного блока."""
        mode = CFBMode(iv)
        plaintext = b"12345678"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
    
    def test_encrypt_decrypt_partial_block(self, cipher, iv):
        """CFB работает с произвольной длиной (потоковый режим)."""
        mode = CFBMode(iv)
        plaintext = b"Short"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert len(ciphertext) == len(plaintext)
        assert decrypted == plaintext
    
    def test_encrypt_decrypt_long_data(self, cipher, iv):
        """Шифрование длинных данных."""
        mode = CFBMode(iv)
        plaintext = b"A" * 100
        
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert len(ciphertext) == 100
        assert decrypted == plaintext
    
    def test_same_ciphertext_length(self, cipher, iv):
        """Размер шифротекста равен размеру открытого текста."""
        mode = CFBMode(iv)
        
        for length in [1, 5, 8, 13, 16, 100]:
            plaintext = bytes([0x41] * length)
            ciphertext = mode.encrypt(plaintext, cipher)
            assert len(ciphertext) == length
    
    def test_no_iv_raises_error(self, cipher):
        """Шифрование без IV вызывает ошибку."""
        mode = CFBMode()
        with pytest.raises(ValueError, match="IV.*не установлен"):
            mode.encrypt(b"test", cipher)
    
    def test_empty_data(self, cipher, iv):
        """Пустые данные."""
        mode = CFBMode(iv)
        assert mode.encrypt(b"", cipher) == b""
        assert mode.decrypt(b"", cipher) == b""


# =============================================================================
# OFB Mode Tests
# =============================================================================

class TestOFBMode:
    """Тесты для режима OFB."""
    
    @pytest.fixture
    def cipher(self):
        return IDEACipher(bytes(range(16)))
    
    @pytest.fixture
    def iv(self):
        return bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
    
    def test_name(self):
        """Проверка названия режима."""
        mode = OFBMode()
        assert mode.name == "OFB"
    
    def test_encrypt_decrypt_roundtrip(self, cipher, iv):
        """Шифрование/расшифрование."""
        mode = OFBMode(iv)
        plaintext = b"Hello, OFB mode!"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
    
    def test_symmetric_operation(self, cipher, iv):
        """OFB симметричен: encrypt == decrypt."""
        mode = OFBMode(iv)
        plaintext = b"TestData"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        
        mode2 = OFBMode(iv)
        decrypted = mode2.encrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
    
    def test_preserves_length(self, cipher, iv):
        """Потоковый режим: длина сохраняется."""
        mode = OFBMode(iv)
        
        for length in [1, 5, 8, 13, 16, 100]:
            plaintext = bytes([0x42] * length)
            ciphertext = mode.encrypt(plaintext, cipher)
            assert len(ciphertext) == length
    
    def test_keystream_independent_of_plaintext(self, cipher, iv):
        """Ключевой поток не зависит от открытого текста."""
        mode1 = OFBMode(iv)
        mode2 = OFBMode(iv)
        
        keystream = mode1.encrypt(bytes(16), cipher)
        
        plaintext = b"0123456789ABCDEF"
        ciphertext = mode2.encrypt(plaintext, cipher)
        
        for i in range(len(plaintext)):
            assert ciphertext[i] == plaintext[i] ^ keystream[i]
    
    def test_no_iv_raises_error(self, cipher):
        """Шифрование без IV вызывает ошибку."""
        mode = OFBMode()
        with pytest.raises(ValueError, match="IV.*не установлен"):
            mode.encrypt(b"test", cipher)
    
    def test_empty_data(self, cipher, iv):
        """Пустые данные."""
        mode = OFBMode(iv)
        assert mode.encrypt(b"", cipher) == b""
        assert mode.decrypt(b"", cipher) == b""


# =============================================================================
# CTR Mode Tests
# =============================================================================

class TestCTRMode:
    """Тесты для режима CTR."""
    
    @pytest.fixture
    def cipher(self):
        return IDEACipher(bytes(range(16)))
    
    @pytest.fixture
    def nonce(self):
        return bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01])
    
    def test_name(self):
        """Проверка названия режима."""
        mode = CTRMode()
        assert mode.name == "CTR"
    
    def test_encrypt_decrypt_roundtrip(self, cipher, nonce):
        """Шифрование/расшифрование."""
        mode = CTRMode(nonce)
        plaintext = b"Hello, CTR mode!"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
    
    def test_symmetric_operation(self, cipher, nonce):
        """CTR симметричен: encrypt == decrypt."""
        mode = CTRMode(nonce)
        plaintext = b"TestData"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        
        mode2 = CTRMode(nonce)
        decrypted = mode2.encrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
    
    def test_preserves_length(self, cipher, nonce):
        """Потоковый режим: длина сохраняется."""
        mode = CTRMode(nonce)
        
        for length in [1, 5, 8, 13, 16, 100]:
            plaintext = bytes([0x43] * length)
            ciphertext = mode.encrypt(plaintext, cipher)
            assert len(ciphertext) == length
    
    def test_random_access(self, cipher, nonce):
        """CTR поддерживает произвольный доступ к блокам."""
        mode = CTRMode(nonce)
        plaintext = b"Block1__Block2__Block3__"
        
        ciphertext = mode.encrypt(plaintext, cipher)
        
        mode2 = CTRMode(nonce)
        block2_decrypted = mode2.decrypt_block_at(ciphertext[8:16], 1, cipher)
        
        assert block2_decrypted == b"Block2__"
    
    def test_counter_increments(self, cipher):
        """Счётчик инкрементируется для каждого блока."""
        nonce = bytes([0x00] * 8)
        mode = CTRMode(nonce)
        
        keystream = mode.encrypt(bytes(24), cipher)
        
        block1 = keystream[0:8]
        block2 = keystream[8:16]
        block3 = keystream[16:24]
        
        assert block1 != block2
        assert block2 != block3
        assert block1 != block3
    
    def test_counter_overflow(self, cipher):
        """Счётчик корректно переполняется."""
        nonce = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE])
        mode = CTRMode(nonce)
        
        plaintext = bytes(24)
        ciphertext = mode.encrypt(plaintext, cipher)
        
        assert len(ciphertext) == 24
    
    def test_no_nonce_raises_error(self, cipher):
        """Шифрование без nonce вызывает ошибку."""
        mode = CTRMode()
        with pytest.raises(ValueError, match="Nonce.*не установлен"):
            mode.encrypt(b"test", cipher)
    
    def test_set_nonce(self, cipher):
        """Установка nonce через метод set_nonce."""
        mode = CTRMode()
        nonce = bytes([0x12] * 8)
        mode.set_nonce(nonce)
        
        plaintext = b"TestData"
        ciphertext = mode.encrypt(plaintext, cipher)
        decrypted = mode.decrypt(ciphertext, cipher)
        
        assert decrypted == plaintext
    
    def test_set_iv_alias(self, cipher):
        """set_iv работает как алиас для set_nonce."""
        mode = CTRMode()
        iv = bytes([0x12] * 8)
        mode.set_iv(iv)
        
        assert mode.iv == iv
        assert mode.nonce == iv
    
    def test_empty_data(self, cipher, nonce):
        """Пустые данные."""
        mode = CTRMode(nonce)
        assert mode.encrypt(b"", cipher) == b""
        assert mode.decrypt(b"", cipher) == b""
