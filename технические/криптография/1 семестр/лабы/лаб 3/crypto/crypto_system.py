"""
Главный класс криптосистемы, объединяющий шифр, режим шифрования и дополнение.

Использует паттерн Strategy для взаимозаменяемости компонентов.
"""

from typing import Optional
from crypto.interfaces import BlockCipher, CipherMode
from crypto.factory import CipherFactory, ModeFactory
from crypto.padding import PaddingScheme, PaddingFactory


# Режимы, требующие IV/nonce
MODES_REQUIRING_IV = {"CBC", "PCBC", "CFB", "OFB", "CTR"}

# Потоковые режимы (не требуют padding)
STREAM_MODES = {"CFB", "OFB", "CTR"}


class CryptoSystem:
    """
    Криптографическая система, объединяющая блочный шифр, режим работы и дополнение.
    
    Использует паттерн Strategy: шифр, режим и дополнение могут быть заменены
    без изменения кода криптосистемы.
    
    Примеры использования:
        # Прямое создание
        cipher = IDEACipher(key)
        mode = ECBMode()
        padding = PKCS7Padding()
        crypto = CryptoSystem(cipher, mode, padding)
        
        # Через фабрики
        crypto = CryptoSystem.create("IDEA", "ECB", key, padding="pkcs7")
        
        # С IV для CBC
        crypto = CryptoSystem.create("IDEA", "CBC", key, iv=iv_bytes, padding="iso7816")
    """
    
    def __init__(self, cipher: BlockCipher, mode: CipherMode, 
                 padding: Optional[PaddingScheme] = None):
        """
        Инициализация криптосистемы.
        
        Args:
            cipher: Блочный шифр (Strategy).
            mode: Режим шифрования (Strategy).
            padding: Схема дополнения (Strategy). Если не указана, используется PKCS7.
        """
        self._cipher = cipher
        self._mode = mode
        # Для потоковых режимов дополнение не нужно
        if mode.name.upper() in STREAM_MODES:
            self._padding = PaddingFactory.create("NONE")
        else:
            self._padding = padding or PaddingFactory.create("PKCS7")
    
    @classmethod
    def create(cls, cipher_name: str, mode_name: str, key: bytes, 
               iv: Optional[bytes] = None, padding: str = "pkcs7",
               **mode_kwargs) -> 'CryptoSystem':
        """
        Создать криптосистему используя фабрики.
        
        Args:
            cipher_name: Название шифра (например, "IDEA").
            mode_name: Название режима (например, "ECB", "CBC", "CTR").
            key: Ключ шифрования.
            iv: Вектор инициализации/nonce для режимов CBC, CFB, OFB, CTR.
            padding: Схема дополнения ("pkcs7", "iso7816", "ansi_x923", "iso10126", "none").
            **mode_kwargs: Дополнительные параметры для режима.
            
        Returns:
            Настроенная криптосистема.
        """
        cipher = CipherFactory.create(cipher_name, key)
        
        # Для режимов с IV передаём его при создании
        if mode_name.upper() in MODES_REQUIRING_IV and iv is not None:
            mode_kwargs['iv'] = iv
        
        mode = ModeFactory.create(mode_name, **mode_kwargs)
        padding_scheme = PaddingFactory.create(padding)
        
        return cls(cipher, mode, padding_scheme)
    
    def set_iv(self, iv: bytes) -> None:
        """
        Установить вектор инициализации (IV) для режимов, требующих его.
        
        Args:
            iv: Вектор инициализации (должен равняться размеру блока).
            
        Raises:
            AttributeError: Если режим не поддерживает IV.
        """
        if hasattr(self._mode, 'set_iv'):
            self._mode.set_iv(iv)
        else:
            raise AttributeError(
                f"Режим {self._mode.name} не поддерживает вектор инициализации"
            )
    
    @property
    def requires_iv(self) -> bool:
        """Требует ли текущий режим IV/nonce."""
        return self._mode.name.upper() in MODES_REQUIRING_IV
    
    @property
    def cipher(self) -> BlockCipher:
        """Текущий блочный шифр."""
        return self._cipher
    
    @property
    def mode(self) -> CipherMode:
        """Текущий режим шифрования."""
        return self._mode
    
    @property
    def padding(self) -> PaddingScheme:
        """Текущая схема дополнения."""
        return self._padding
    
    @property
    def padding_name(self) -> str:
        """Название схемы дополнения."""
        return self._padding.name
    
    @property
    def cipher_name(self) -> str:
        """Название шифра."""
        return self._cipher.name
    
    @property
    def mode_name(self) -> str:
        """Название режима."""
        return self._mode.name
    
    @property
    def block_size(self) -> int:
        """Размер блока в байтах."""
        return self._cipher.block_size
    
    @property
    def key_size(self) -> int:
        """Размер ключа в байтах."""
        return self._cipher.key_size
    
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Зашифровать данные.
        
        Args:
            plaintext: Открытый текст.
            
        Returns:
            Зашифрованные данные.
        """
        # Для потоковых режимов дополнение не нужно
        if self._mode.name.upper() in STREAM_MODES:
            return self._mode.encrypt(plaintext, self._cipher)
        
        # Добавляем дополнение для блочных режимов
        padded = self._padding.pad(plaintext, self._cipher.block_size)
        return self._mode.encrypt(padded, self._cipher)
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Расшифровать данные.
        
        Args:
            ciphertext: Зашифрованные данные.
            
        Returns:
            Расшифрованный текст (без дополнения).
        """
        decrypted = self._mode.decrypt(ciphertext, self._cipher)
        
        # Для потоковых режимов дополнение не удаляем
        if self._mode.name.upper() in STREAM_MODES:
            return decrypted
        
        # Удаляем дополнение для блочных режимов
        return self._padding.unpad(decrypted, self._cipher.block_size)
    
    def encrypt_hex(self, plaintext: bytes) -> str:
        """
        Зашифровать данные и вернуть результат в hex-формате.
        
        Args:
            plaintext: Открытый текст.
            
        Returns:
            Зашифрованные данные в виде hex-строки.
        """
        return self.encrypt(plaintext).hex()
    
    def decrypt_hex(self, ciphertext_hex: str) -> bytes:
        """
        Расшифровать данные из hex-формата.
        
        Args:
            ciphertext_hex: Зашифрованные данные в hex-формате.
            
        Returns:
            Расшифрованный текст.
        """
        return self.decrypt(bytes.fromhex(ciphertext_hex))
    
    def __repr__(self) -> str:
        return f"CryptoSystem({self.cipher_name}-{self.mode_name}, padding={self.padding_name})"
