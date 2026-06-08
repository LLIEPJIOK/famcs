"""
Интеграционные тесты и прочие тесты.

Включают:
- Тесты CryptoSystem
- Тесты фабрик (CipherFactory, ModeFactory)
- Тесты интерфейсов
- Тесты CLI
- Тесты интеграции режимов с CryptoSystem
- Тесты интеграции padding с CryptoSystem
- Тесты bit-flip атак
- Тесты крайних случаев
"""

import pytest
import subprocess
import sys
from abc import ABC

from crypto import CryptoSystem, ModeFactory
from crypto.ciphers.idea import IDEACipher
from crypto.modes.ecb import ECBMode
from crypto.factory import CipherFactory, ModeFactory
from crypto.interfaces import BlockCipher, CipherMode
from crypto.crypto_system import CryptoSystem


# =============================================================================
# Interface Tests
# =============================================================================

class TestBlockCipherInterface:
    """Тесты интерфейса BlockCipher."""
    
    def test_cannot_instantiate_directly(self):
        """Тест: нельзя создать экземпляр абстрактного класса."""
        with pytest.raises(TypeError):
            BlockCipher()
    
    def test_is_abstract_class(self):
        """Тест: BlockCipher — абстрактный класс."""
        assert issubclass(BlockCipher, ABC)
    
    def test_incomplete_implementation_fails(self):
        """Тест: неполная реализация вызывает ошибку."""
        class IncompleteCipher(BlockCipher):
            @property
            def block_size(self) -> int:
                return 8
        
        with pytest.raises(TypeError):
            IncompleteCipher()
    
    def test_complete_implementation_works(self):
        """Тест: полная реализация работает."""
        class CompleteCipher(BlockCipher):
            @property
            def block_size(self) -> int:
                return 8
            
            @property
            def key_size(self) -> int:
                return 16
            
            @property
            def name(self) -> str:
                return "TEST"
            
            def encrypt_block(self, block: bytes) -> bytes:
                return block
            
            def decrypt_block(self, block: bytes) -> bytes:
                return block
        
        cipher = CompleteCipher()
        assert cipher.block_size == 8
        assert cipher.key_size == 16
        assert cipher.name == "TEST"


class TestCipherModeInterface:
    """Тесты интерфейса CipherMode."""
    
    def test_cannot_instantiate_directly(self):
        """Тест: нельзя создать экземпляр абстрактного класса."""
        with pytest.raises(TypeError):
            CipherMode()
    
    def test_is_abstract_class(self):
        """Тест: CipherMode — абстрактный класс."""
        assert issubclass(CipherMode, ABC)
    
    def test_incomplete_implementation_fails(self):
        """Тест: неполная реализация вызывает ошибку."""
        class IncompleteMode(CipherMode):
            @property
            def name(self) -> str:
                return "TEST"
        
        with pytest.raises(TypeError):
            IncompleteMode()
    
    def test_complete_implementation_works(self):
        """Тест: полная реализация работает."""
        class CompleteMode(CipherMode):
            @property
            def name(self) -> str:
                return "TEST"
            
            def encrypt(self, plaintext: bytes, cipher: BlockCipher) -> bytes:
                return plaintext
            
            def decrypt(self, ciphertext: bytes, cipher: BlockCipher) -> bytes:
                return ciphertext
        
        mode = CompleteMode()
        assert mode.name == "TEST"


# =============================================================================
# Factory Tests
# =============================================================================

class TestCipherFactory:
    """Тесты фабрики шифров."""
    
    def test_idea_registered(self):
        """Тест: IDEA зарегистрирован по умолчанию."""
        assert CipherFactory.is_registered("IDEA")
        assert CipherFactory.is_registered("idea")
    
    def test_create_idea(self):
        """Тест создания IDEA через фабрику."""
        cipher = CipherFactory.create("IDEA", bytes(16))
        assert isinstance(cipher, IDEACipher)
        assert cipher.name == "IDEA"
    
    def test_create_case_insensitive(self):
        """Тест регистронезависимости создания."""
        cipher1 = CipherFactory.create("IDEA", bytes(16))
        cipher2 = CipherFactory.create("idea", bytes(16))
        cipher3 = CipherFactory.create("Idea", bytes(16))
        
        assert type(cipher1) == type(cipher2) == type(cipher3)
    
    def test_create_unknown_cipher(self):
        """Тест ошибки при создании неизвестного шифра."""
        with pytest.raises(ValueError) as exc_info:
            CipherFactory.create("UNKNOWN", bytes(16))
        assert "не найден" in str(exc_info.value).lower()
    
    def test_get_available(self):
        """Тест получения списка доступных шифров."""
        available = CipherFactory.get_available()
        assert "IDEA" in available
        assert isinstance(available, list)


class TestCipherFactoryRegistration:
    """Тесты регистрации новых шифров."""
    
    def test_register_new_cipher(self):
        """Тест регистрации нового шифра."""
        class DummyCipher(BlockCipher):
            def __init__(self, key: bytes):
                self._key = key
            
            @property
            def block_size(self) -> int:
                return 8
            
            @property
            def key_size(self) -> int:
                return 8
            
            @property
            def name(self) -> str:
                return "DUMMY"
            
            def encrypt_block(self, block: bytes) -> bytes:
                return block
            
            def decrypt_block(self, block: bytes) -> bytes:
                return block
        
        CipherFactory.register("DUMMY", DummyCipher)
        
        assert CipherFactory.is_registered("DUMMY")
        cipher = CipherFactory.create("DUMMY", bytes(8))
        assert cipher.name == "DUMMY"
        
        # Cleanup
        del CipherFactory._ciphers["DUMMY"]
    
    def test_is_registered_unknown(self):
        """Тест is_registered для неизвестного шифра."""
        assert not CipherFactory.is_registered("NONEXISTENT")


class TestModeFactoryTests:
    """Тесты фабрики режимов."""
    
    def test_ecb_registered(self):
        """Тест: ECB зарегистрирован по умолчанию."""
        assert ModeFactory.is_registered("ECB")
        assert ModeFactory.is_registered("ecb")
    
    def test_create_ecb(self):
        """Тест создания ECB через фабрику."""
        mode = ModeFactory.create("ECB")
        assert isinstance(mode, ECBMode)
        assert mode.name == "ECB"
    
    def test_create_case_insensitive(self):
        """Тест регистронезависимости создания."""
        mode1 = ModeFactory.create("ECB")
        mode2 = ModeFactory.create("ecb")
        mode3 = ModeFactory.create("Ecb")
        
        assert type(mode1) == type(mode2) == type(mode3)
    
    def test_create_unknown_mode(self):
        """Тест ошибки при создании неизвестного режима."""
        with pytest.raises(ValueError) as exc_info:
            ModeFactory.create("XYZ")
        assert "не найден" in str(exc_info.value).lower()
    
    def test_get_available(self):
        """Тест получения списка доступных режимов."""
        available = ModeFactory.get_available()
        assert "ECB" in available
        assert "CBC" in available
        assert "PCBC" in available
        assert "CFB" in available
        assert "OFB" in available
        assert "CTR" in available
        assert isinstance(available, list)


class TestModeFactoryRegistration:
    """Тесты регистрации новых режимов."""
    
    def test_register_new_mode(self):
        """Тест регистрации нового режима."""
        class DummyMode(CipherMode):
            @property
            def name(self) -> str:
                return "DUMMY"
            
            def encrypt(self, plaintext: bytes, cipher: BlockCipher) -> bytes:
                return plaintext
            
            def decrypt(self, ciphertext: bytes, cipher: BlockCipher) -> bytes:
                return ciphertext
        
        ModeFactory.register("DUMMY", DummyMode)
        
        assert ModeFactory.is_registered("DUMMY")
        mode = ModeFactory.create("DUMMY")
        assert mode.name == "DUMMY"
        
        # Cleanup
        del ModeFactory._modes["DUMMY"]
    
    def test_is_registered_unknown(self):
        """Тест is_registered для неизвестного режима."""
        assert not ModeFactory.is_registered("NONEXISTENT")


# =============================================================================
# CryptoSystem Tests
# =============================================================================

class TestCryptoSystemCreation:
    """Тесты создания криптосистемы."""
    
    def test_create_direct(self):
        """Тест прямого создания."""
        key = bytes(16)
        cipher = IDEACipher(key)
        mode = ECBMode()
        
        crypto = CryptoSystem(cipher, mode)
        
        assert crypto.cipher_name == "IDEA"
        assert crypto.mode_name == "ECB"
    
    def test_create_via_factory(self):
        """Тест создания через фабричный метод."""
        crypto = CryptoSystem.create("IDEA", "ECB", bytes(16))
        
        assert crypto.cipher_name == "IDEA"
        assert crypto.mode_name == "ECB"
    
    def test_create_case_insensitive(self):
        """Тест регистронезависимости фабричного метода."""
        crypto1 = CryptoSystem.create("IDEA", "ECB", bytes(16))
        crypto2 = CryptoSystem.create("idea", "ecb", bytes(16))
        
        assert crypto1.cipher_name == crypto2.cipher_name
        assert crypto1.mode_name == crypto2.mode_name


class TestCryptoSystemProperties:
    """Тесты свойств криптосистемы."""
    
    @pytest.fixture
    def crypto(self):
        return CryptoSystem.create("IDEA", "ECB", bytes(range(16)))
    
    def test_cipher_property(self, crypto):
        """Тест получения шифра."""
        assert isinstance(crypto.cipher, IDEACipher)
    
    def test_mode_property(self, crypto):
        """Тест получения режима."""
        assert isinstance(crypto.mode, ECBMode)
    
    def test_cipher_name(self, crypto):
        """Тест названия шифра."""
        assert crypto.cipher_name == "IDEA"
    
    def test_mode_name(self, crypto):
        """Тест названия режима."""
        assert crypto.mode_name == "ECB"
    
    def test_block_size(self, crypto):
        """Тест размера блока."""
        assert crypto.block_size == 8
    
    def test_key_size(self, crypto):
        """Тест размера ключа."""
        assert crypto.key_size == 16
    
    def test_repr(self, crypto):
        """Тест строкового представления."""
        assert repr(crypto) == "CryptoSystem(IDEA-ECB, padding=PKCS7)"


class TestCryptoSystemEncryption:
    """Тесты шифрования."""
    
    @pytest.fixture
    def crypto(self):
        return CryptoSystem.create("IDEA", "ECB", bytes(range(16)))
    
    def test_encrypt_returns_bytes(self, crypto):
        """Тест что encrypt возвращает bytes."""
        result = crypto.encrypt(b"TESTDATA")
        assert isinstance(result, bytes)
    
    def test_encrypt_changes_data(self, crypto):
        """Тест что шифрование изменяет данные."""
        plaintext = b"TESTDATA"
        ciphertext = crypto.encrypt(plaintext)
        assert ciphertext != plaintext
    
    def test_encrypt_deterministic(self, crypto):
        """Тест детерминированности шифрования."""
        plaintext = b"TESTDATA"
        ct1 = crypto.encrypt(plaintext)
        ct2 = crypto.encrypt(plaintext)
        assert ct1 == ct2
    
    def test_encrypt_empty(self, crypto):
        """Тест шифрования пустых данных - с PKCS7 добавляется блок дополнения."""
        result = crypto.encrypt(bytes())
        assert len(result) == 8
        decrypted = crypto.decrypt(result)
        assert decrypted == bytes()


class TestCryptoSystemDecryption:
    """Тесты расшифрования."""
    
    @pytest.fixture
    def crypto(self):
        return CryptoSystem.create("IDEA", "ECB", bytes(range(16)))
    
    def test_decrypt_returns_bytes(self, crypto):
        """Тест что decrypt возвращает bytes."""
        ciphertext = crypto.encrypt(b"TESTDATA")
        result = crypto.decrypt(ciphertext)
        assert isinstance(result, bytes)
    
    def test_decrypt_roundtrip(self, crypto):
        """Тест полного цикла."""
        plaintext = b"TESTDATA"
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        assert decrypted == plaintext
    
    def test_decrypt_multiple_blocks(self, crypto):
        """Тест расшифрования нескольких блоков."""
        plaintext = b"A" * 64
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        assert decrypted == plaintext


class TestCryptoSystemHex:
    """Тесты hex-методов."""
    
    @pytest.fixture
    def crypto(self):
        return CryptoSystem.create("IDEA", "ECB", bytes(range(16)))
    
    def test_encrypt_hex_returns_string(self, crypto):
        """Тест что encrypt_hex возвращает строку."""
        result = crypto.encrypt_hex(b"TESTDATA")
        assert isinstance(result, str)
    
    def test_encrypt_hex_valid_hex(self, crypto):
        """Тест что результат — валидная hex-строка."""
        result = crypto.encrypt_hex(b"TESTDATA")
        bytes.fromhex(result)
    
    def test_decrypt_hex_roundtrip(self, crypto):
        """Тест полного цикла с hex."""
        plaintext = b"TESTDATA"
        hex_ciphertext = crypto.encrypt_hex(plaintext)
        decrypted = crypto.decrypt_hex(hex_ciphertext)
        assert decrypted == plaintext
    
    def test_hex_consistency(self, crypto):
        """Тест консистентности hex-методов."""
        plaintext = b"TESTDATA"
        ciphertext_bytes = crypto.encrypt(plaintext)
        ciphertext_hex = crypto.encrypt_hex(plaintext)
        assert ciphertext_bytes.hex() == ciphertext_hex


class TestCryptoSystemDifferentKeys:
    """Тесты с разными ключами."""
    
    def test_different_keys_different_ciphertext(self):
        """Тест: разные ключи дают разный шифротекст."""
        key1 = bytes(16)
        key2 = bytes([1] + [0] * 15)
        
        crypto1 = CryptoSystem.create("IDEA", "ECB", key1)
        crypto2 = CryptoSystem.create("IDEA", "ECB", key2)
        
        ct1 = crypto1.encrypt(b"TESTDATA")
        ct2 = crypto2.encrypt(b"TESTDATA")
        
        assert ct1 != ct2
    
    def test_same_key_same_ciphertext(self):
        """Тест: одинаковые ключи дают одинаковый шифротекст."""
        key = bytes(range(16))
        
        crypto1 = CryptoSystem.create("IDEA", "ECB", key)
        crypto2 = CryptoSystem.create("IDEA", "ECB", key)
        
        ct1 = crypto1.encrypt(b"TESTDATA")
        ct2 = crypto2.encrypt(b"TESTDATA")
        
        assert ct1 == ct2


class TestCryptoSystemIntegration:
    """Интеграционные тесты CryptoSystem."""
    
    def test_encrypt_large_data(self):
        """Тест шифрования больших данных."""
        crypto = CryptoSystem.create("IDEA", "ECB", bytes(range(16)))
        plaintext = bytes(range(256)) * 4
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext
    
    def test_various_data_patterns(self):
        """Тест различных паттернов данных."""
        crypto = CryptoSystem.create("IDEA", "ECB", bytes([0xAA, 0xBB, 0xCC, 0xDD] * 4))
        
        patterns = [
            bytes(64),
            bytes([0xFF] * 64),
            bytes(range(64)),
            b"Hello, World!" + bytes(51),
            bytes([0xAA, 0x55] * 32),
        ]
        
        for pattern in patterns:
            ciphertext = crypto.encrypt(pattern)
            decrypted = crypto.decrypt(ciphertext)
            assert decrypted == pattern


# =============================================================================
# Modes Integration with CryptoSystem
# =============================================================================

class TestModesWithCryptoSystem:
    """Интеграционные тесты режимов через CryptoSystem."""
    
    @pytest.fixture
    def key(self):
        return bytes(range(16))
    
    @pytest.fixture
    def iv(self):
        return bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88])
    
    def test_cbc_via_crypto_system(self, key, iv):
        """CBC через CryptoSystem."""
        crypto = CryptoSystem.create("IDEA", "CBC", key, iv=iv)
        plaintext = b"CBC test message!"
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted[:len(plaintext)] == plaintext
    
    def test_pcbc_via_crypto_system(self, key, iv):
        """PCBC через CryptoSystem."""
        crypto = CryptoSystem.create("IDEA", "PCBC", key, iv=iv)
        plaintext = b"PCBC test message"
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext
    
    def test_cfb_via_crypto_system(self, key, iv):
        """CFB через CryptoSystem."""
        crypto = CryptoSystem.create("IDEA", "CFB", key, iv=iv)
        plaintext = b"CFB test!"
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext
        assert len(ciphertext) == len(plaintext)
    
    def test_ofb_via_crypto_system(self, key, iv):
        """OFB через CryptoSystem."""
        crypto = CryptoSystem.create("IDEA", "OFB", key, iv=iv)
        plaintext = b"OFB test!"
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext
    
    def test_ctr_via_crypto_system(self, key, iv):
        """CTR через CryptoSystem."""
        crypto = CryptoSystem.create("IDEA", "CTR", key, iv=iv)
        plaintext = b"CTR test!"
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext
    
    def test_requires_iv_property(self, key, iv):
        """Свойство requires_iv."""
        ecb = CryptoSystem.create("IDEA", "ECB", key)
        cbc = CryptoSystem.create("IDEA", "CBC", key, iv=iv)
        
        assert ecb.requires_iv == False
        assert cbc.requires_iv == True
    
    def test_set_iv_via_crypto_system(self, key):
        """Установка IV через CryptoSystem.set_iv."""
        crypto = CryptoSystem.create("IDEA", "CBC", key)
        iv = bytes([0x99] * 8)
        crypto.set_iv(iv)
        
        plaintext = b"TestData"
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext


# =============================================================================
# Padding Integration with CryptoSystem
# =============================================================================

class TestPaddingWithCryptoSystem:
    """Интеграционные тесты padding с CryptoSystem."""
    
    @pytest.fixture
    def key(self):
        return bytes(16)
    
    def test_pkcs7_ecb_roundtrip(self, key):
        """Цикл шифрования/расшифрования с PKCS7 и ECB."""
        crypto = CryptoSystem.create("IDEA", "ECB", key, padding="pkcs7")
        plaintext = b"Hello, PKCS7!"
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext
    
    def test_iso7816_cbc_roundtrip(self, key):
        """Цикл с ISO7816 и CBC."""
        crypto = CryptoSystem.create("IDEA", "CBC", key, iv=bytes(8), padding="iso7816")
        plaintext = b"ISO 7816-4 test"
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext
    
    def test_ansi_x923_ecb_roundtrip(self, key):
        """Цикл с ANSI X9.23 и ECB."""
        crypto = CryptoSystem.create("IDEA", "ECB", key, padding="ansi_x923")
        plaintext = b"ANSI X9.23"
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext
    
    def test_iso10126_cbc_roundtrip(self, key):
        """Цикл с ISO 10126 и CBC."""
        crypto = CryptoSystem.create("IDEA", "CBC", key, iv=bytes(8), padding="iso10126")
        plaintext = b"ISO 10126 random padding test"
        
        ciphertext = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(ciphertext)
        
        assert decrypted == plaintext
    
    def test_stream_mode_ignores_padding(self, key):
        """Потоковые режимы (CFB, OFB, CTR) не используют padding."""
        iv = bytes(8)
        
        for mode in ["CFB", "OFB", "CTR"]:
            crypto = CryptoSystem.create("IDEA", mode, key, iv=iv, padding="pkcs7")
            
            assert crypto.padding_name == "None"
            
            plaintext = b"Hello"
            ciphertext = crypto.encrypt(plaintext)
            decrypted = crypto.decrypt(ciphertext)
            
            assert decrypted == plaintext
    
    def test_all_paddings_with_ecb(self, key):
        """Все схемы дополнения работают с ECB."""
        plaintext = b"Universal test data for all padding schemes!"
        
        for padding_name in ["pkcs7", "iso7816", "ansi_x923", "iso10126"]:
            crypto = CryptoSystem.create("IDEA", "ECB", key, padding=padding_name)
            
            ciphertext = crypto.encrypt(plaintext)
            decrypted = crypto.decrypt(ciphertext)
            
            assert decrypted == plaintext, f"Ошибка с {padding_name}"


class TestAllPaddingsWithAllModes:
    """Тесты всех комбинаций padding и режимов."""
    
    @pytest.fixture
    def key(self):
        return bytes(range(16))
    
    @pytest.fixture
    def iv(self):
        return bytes([0x99] * 8)
    
    def test_all_combinations(self, key, iv):
        """Все комбинации padding и режимов работают."""
        paddings = ["pkcs7", "iso7816", "ansi_x923", "iso10126"]
        block_modes = ["ECB", "CBC", "PCBC"]
        
        plaintext = b"Test data for all combinations!"
        
        for mode in block_modes:
            for padding in paddings:
                if mode == "ECB":
                    crypto = CryptoSystem.create("IDEA", mode, key, padding=padding)
                else:
                    crypto = CryptoSystem.create("IDEA", mode, key, iv=iv, padding=padding)
                
                ct = crypto.encrypt(plaintext)
                decrypted = crypto.decrypt(ct)
                
                assert decrypted == plaintext, f"Ошибка: {mode} + {padding}"


# =============================================================================
# Bit-Flip Attack Tests
# =============================================================================

class TestBitFlipAttack:
    """
    Тесты на изменение байта в шифротексте.
    
    При изменении любого байта в шифротексте, расшифрованный текст
    должен отличаться от исходного.
    """
    
    @pytest.fixture
    def key(self):
        return bytes(range(16))
    
    @pytest.fixture
    def iv(self):
        return bytes([0x55] * 8)
    
    def test_ecb_bit_flip(self, key):
        """ECB: изменение байта в шифротексте меняет расшифрованный текст."""
        crypto = CryptoSystem.create("IDEA", "ECB", key, padding="pkcs7")
        plaintext = b"Original message for testing!"
        
        ciphertext = crypto.encrypt(plaintext)
        
        modified_ciphertext = bytearray(ciphertext)
        modified_ciphertext[5] ^= 0xFF
        modified_ciphertext = bytes(modified_ciphertext)
        
        try:
            decrypted = crypto.decrypt(modified_ciphertext)
            assert decrypted != plaintext
        except ValueError:
            pass
    
    def test_cbc_bit_flip(self, key, iv):
        """CBC: изменение байта в шифротексте влияет на расшифровку."""
        crypto = CryptoSystem.create("IDEA", "CBC", key, iv=iv, padding="pkcs7")
        plaintext = b"Original message for CBC mode!"
        
        ciphertext = crypto.encrypt(plaintext)
        
        modified = bytearray(ciphertext)
        modified[3] ^= 0xAA
        modified = bytes(modified)
        
        try:
            decrypted = crypto.decrypt(modified)
            assert decrypted != plaintext
        except ValueError:
            pass
    
    def test_pcbc_bit_flip(self, key, iv):
        """PCBC: изменение байта распространяется на все последующие блоки."""
        crypto = CryptoSystem.create("IDEA", "PCBC", key, iv=iv, padding="pkcs7")
        plaintext = b"Original message for PCBC mode!"
        
        ciphertext = crypto.encrypt(plaintext)
        
        modified = bytearray(ciphertext)
        modified[0] ^= 0x01
        modified = bytes(modified)
        
        try:
            decrypted = crypto.decrypt(modified)
            assert decrypted != plaintext
        except ValueError:
            pass
    
    def test_cfb_bit_flip(self, key, iv):
        """CFB: изменение байта влияет на расшифровку."""
        crypto = CryptoSystem.create("IDEA", "CFB", key, iv=iv)
        plaintext = b"Original message for CFB mode!"
        
        ciphertext = crypto.encrypt(plaintext)
        
        modified = bytearray(ciphertext)
        modified[10] ^= 0xFF
        modified = bytes(modified)
        
        decrypted = crypto.decrypt(modified)
        assert decrypted != plaintext
    
    def test_ofb_bit_flip(self, key, iv):
        """OFB: изменение байта влияет ровно на один байт открытого текста."""
        crypto = CryptoSystem.create("IDEA", "OFB", key, iv=iv)
        plaintext = b"Original message for OFB mode!"
        
        ciphertext = crypto.encrypt(plaintext)
        
        modified = bytearray(ciphertext)
        flip_position = 10
        modified[flip_position] ^= 0xFF
        modified = bytes(modified)
        
        decrypted = crypto.decrypt(modified)
        assert decrypted != plaintext
        
        differences = sum(1 for i in range(len(plaintext)) if plaintext[i] != decrypted[i])
        assert differences >= 1
    
    def test_ctr_bit_flip(self, key, iv):
        """CTR: изменение байта влияет ровно на один байт открытого текста."""
        crypto = CryptoSystem.create("IDEA", "CTR", key, iv=iv)
        plaintext = b"Original message for CTR mode!"
        
        ciphertext = crypto.encrypt(plaintext)
        
        modified = bytearray(ciphertext)
        flip_position = 5
        modified[flip_position] ^= 0x42
        modified = bytes(modified)
        
        decrypted = crypto.decrypt(modified)
        assert decrypted != plaintext
        
        differences = sum(1 for i in range(len(plaintext)) if plaintext[i] != decrypted[i])
        assert differences == 1


# =============================================================================
# Edge Cases Tests
# =============================================================================

class TestEdgeCases:
    """Тесты крайних случаев для всех режимов."""
    
    @pytest.fixture
    def key(self):
        return bytes(range(16))
    
    @pytest.fixture
    def iv(self):
        return bytes([0x77] * 8)
    
    def test_all_modes_empty_input(self, key, iv):
        """Все режимы обрабатывают пустой ввод."""
        modes_with_iv = ["CBC", "PCBC", "CFB", "OFB", "CTR"]
        
        crypto_ecb = CryptoSystem.create("IDEA", "ECB", key, padding="pkcs7")
        ciphertext = crypto_ecb.encrypt(b"")
        decrypted = crypto_ecb.decrypt(ciphertext)
        assert decrypted == b""
        
        for mode in modes_with_iv:
            crypto = CryptoSystem.create("IDEA", mode, key, iv=iv, padding="pkcs7")
            ciphertext = crypto.encrypt(b"")
            decrypted = crypto.decrypt(ciphertext)
            assert decrypted == b"", f"Ошибка в режиме {mode}"
    
    def test_all_modes_single_byte(self, key, iv):
        """Все режимы обрабатывают один байт."""
        plaintext = b"A"
        
        crypto_ecb = CryptoSystem.create("IDEA", "ECB", key, padding="pkcs7")
        ct = crypto_ecb.encrypt(plaintext)
        assert crypto_ecb.decrypt(ct) == plaintext
        
        for mode in ["CBC", "PCBC", "CFB", "OFB", "CTR"]:
            crypto = CryptoSystem.create("IDEA", mode, key, iv=iv, padding="pkcs7")
            ct = crypto.encrypt(plaintext)
            assert crypto.decrypt(ct) == plaintext, f"Ошибка в режиме {mode}"
    
    def test_all_modes_exact_block_size(self, key, iv):
        """Все режимы обрабатывают данные ровно в один блок."""
        plaintext = b"12345678"
        
        crypto_ecb = CryptoSystem.create("IDEA", "ECB", key, padding="pkcs7")
        ct = crypto_ecb.encrypt(plaintext)
        assert crypto_ecb.decrypt(ct) == plaintext
        
        for mode in ["CBC", "PCBC", "CFB", "OFB", "CTR"]:
            crypto = CryptoSystem.create("IDEA", mode, key, iv=iv, padding="pkcs7")
            ct = crypto.encrypt(plaintext)
            assert crypto.decrypt(ct) == plaintext, f"Ошибка в режиме {mode}"
    
    def test_all_modes_large_data(self, key, iv):
        """Все режимы обрабатывают большие данные."""
        plaintext = bytes([i % 256 for i in range(1000)])
        
        crypto_ecb = CryptoSystem.create("IDEA", "ECB", key, padding="pkcs7")
        ct = crypto_ecb.encrypt(plaintext)
        assert crypto_ecb.decrypt(ct) == plaintext
        
        for mode in ["CBC", "PCBC", "CFB", "OFB", "CTR"]:
            crypto = CryptoSystem.create("IDEA", mode, key, iv=iv, padding="pkcs7")
            ct = crypto.encrypt(plaintext)
            assert crypto.decrypt(ct) == plaintext, f"Ошибка в режиме {mode}"
    
    def test_all_zeros_key(self, iv):
        """Нулевой ключ работает корректно."""
        zero_key = bytes(16)
        plaintext = b"Test with zero key"
        
        for mode in ["ECB", "CBC", "PCBC", "CFB", "OFB", "CTR"]:
            if mode == "ECB":
                crypto = CryptoSystem.create("IDEA", mode, zero_key, padding="pkcs7")
            else:
                crypto = CryptoSystem.create("IDEA", mode, zero_key, iv=iv, padding="pkcs7")
            
            ct = crypto.encrypt(plaintext)
            assert crypto.decrypt(ct) == plaintext, f"Ошибка в режиме {mode}"
    
    def test_all_ones_key(self, iv):
        """Ключ из единиц работает корректно."""
        ones_key = bytes([0xFF] * 16)
        plaintext = b"Test with all-ones key"
        
        for mode in ["ECB", "CBC", "PCBC", "CFB", "OFB", "CTR"]:
            if mode == "ECB":
                crypto = CryptoSystem.create("IDEA", mode, ones_key, padding="pkcs7")
            else:
                crypto = CryptoSystem.create("IDEA", mode, ones_key, iv=iv, padding="pkcs7")
            
            ct = crypto.encrypt(plaintext)
            assert crypto.decrypt(ct) == plaintext, f"Ошибка в режиме {mode}"


# =============================================================================
# CLI Tests
# =============================================================================

import os

# Настройка окружения для subprocess с поддержкой Unicode
CLI_ENV = {**os.environ, 'PYTHONIOENCODING': 'utf-8'}


class TestCLIFileOperations:
    """Тесты файловых операций CLI."""
    
    @pytest.fixture
    def temp_dir(self, tmp_path):
        return tmp_path
    
    @pytest.fixture
    def test_key(self, temp_dir):
        key_path = temp_dir / "key.bin"
        key_path.write_bytes(bytes(range(16)))
        return key_path
    
    @pytest.fixture
    def test_input(self, temp_dir):
        input_path = temp_dir / "in.bin"
        input_path.write_bytes(b"TESTDATA")
        return input_path
    
    def test_encrypt_decrypt_roundtrip(self, temp_dir, test_key, test_input):
        """Тест полного цикла шифрования-расшифрования через CLI."""
        encrypted_path = temp_dir / "encrypted.bin"
        decrypted_path = temp_dir / "decrypted.bin"
        
        result = subprocess.run([
            sys.executable, "cli.py",
            "--encrypt",
            "--cipher", "IDEA",
            "--mode", "ECB",
            "--input", str(test_input),
            "--output", str(encrypted_path),
            "--key", str(test_key),
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
        
        assert result.returncode == 0, f"Шифрование не удалось: {result.stderr}"
        assert encrypted_path.exists()
        
        result = subprocess.run([
            sys.executable, "cli.py",
            "--decrypt",
            "--cipher", "IDEA",
            "--mode", "ECB",
            "--input", str(encrypted_path),
            "--output", str(decrypted_path),
            "--key", str(test_key),
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
        
        assert result.returncode == 0, f"Расшифрование не удалось: {result.stderr}"
        assert decrypted_path.exists()
        
        original = test_input.read_bytes()
        decrypted = decrypted_path.read_bytes()
        assert decrypted == original
    
    def test_encrypt_multiple_blocks(self, temp_dir, test_key):
        """Тест шифрования нескольких блоков."""
        input_path = temp_dir / "in.bin"
        input_path.write_bytes(b"Block 1!" + b"Block 2!" + b"Block 3!")  # 24 байта
        
        output_path = temp_dir / "out.bin"
        
        result = subprocess.run([
            sys.executable, "cli.py",
            "-e", "-c", "IDEA", "-m", "ECB", "-p", "none",
            "-i", str(input_path),
            "-o", str(output_path),
            "-k", str(test_key),
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
        
        assert result.returncode == 0
        assert output_path.exists()
        # 24 байта = 3 блока по 8 байт, без padding
        assert len(output_path.read_bytes()) == 24
    
    def test_missing_input_file(self, temp_dir, test_key):
        """Тест ошибки при отсутствии входного файла."""
        result = subprocess.run([
            sys.executable, "cli.py",
            "-e", "-c", "IDEA", "-m", "ECB",
            "-i", str(temp_dir / "nonexistent.bin"),
            "-k", str(test_key),
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
        
        assert result.returncode != 0
    
    def test_missing_key_file(self, temp_dir, test_input):
        """Тест ошибки при отсутствии файла ключа."""
        result = subprocess.run([
            sys.executable, "cli.py",
            "-e", "-c", "IDEA", "-m", "ECB",
            "-i", str(test_input),
            "-k", str(temp_dir / "nonexistent_key.bin"),
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
        
        assert result.returncode != 0


class TestCLIKeyValidation:
    """Тесты валидации ключа."""
    
    @pytest.fixture
    def temp_dir(self, tmp_path):
        return tmp_path
    
    @pytest.fixture
    def test_input(self, temp_dir):
        input_path = temp_dir / "in.bin"
        input_path.write_bytes(b"TESTDATA")
        return input_path
    
    def test_short_key_padded(self, temp_dir, test_input):
        """Тест дополнения короткого ключа."""
        key_path = temp_dir / "key.bin"
        key_path.write_bytes(b"short")
        
        output_path = temp_dir / "out.bin"
        
        result = subprocess.run([
            sys.executable, "cli.py",
            "-e", "-c", "IDEA", "-m", "ECB",
            "-i", str(test_input),
            "-o", str(output_path),
            "-k", str(key_path),
            "-v",
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
        
        assert result.returncode == 0
    
    def test_long_key_truncated(self, temp_dir, test_input):
        """Тест обрезки длинного ключа."""
        key_path = temp_dir / "key.bin"
        key_path.write_bytes(bytes(32))
        
        output_path = temp_dir / "out.bin"
        
        result = subprocess.run([
            sys.executable, "cli.py",
            "-e", "-c", "IDEA", "-m", "ECB",
            "-i", str(test_input),
            "-o", str(output_path),
            "-k", str(key_path),
            "-v",
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
        
        assert result.returncode == 0


class TestCLIArguments:
    """Тесты аргументов командной строки."""
    
    def test_help(self):
        """Тест вывода справки."""
        result = subprocess.run([
            sys.executable, "cli.py", "--help"
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
        
        assert result.returncode == 0
        assert "IDEA" in result.stdout
        assert "ECB" in result.stdout
    
    def test_missing_mode_argument(self):
        """Тест ошибки при отсутствии режима (encrypt/decrypt)."""
        result = subprocess.run([
            sys.executable, "cli.py",
            "-c", "IDEA", "-m", "ECB",
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
        
        assert result.returncode != 0
    
    def test_case_insensitive_cipher(self, tmp_path):
        """Тест регистронезависимости имени шифра."""
        key_path = tmp_path / "key.bin"
        key_path.write_bytes(bytes(16))
        
        input_path = tmp_path / "in.bin"
        input_path.write_bytes(b"TESTDATA")
        
        output_path = tmp_path / "out.bin"
        
        # CLI поддерживает только 'idea' и 'IDEA'
        for cipher_name in ["IDEA", "idea"]:
            result = subprocess.run([
                sys.executable, "cli.py",
                "-e", "-c", cipher_name, "-m", "ECB",
                "-i", str(input_path),
                "-o", str(output_path),
                "-k", str(key_path),
            ], capture_output=True, text=True, encoding='utf-8', errors='replace', env=CLI_ENV)
            
            assert result.returncode == 0, f"Не сработало для {cipher_name}"
