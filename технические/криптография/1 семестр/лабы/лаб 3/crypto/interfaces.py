"""
Интерфейсы (абстрактные базовые классы) для паттерна Strategy.

Определяют контракты для:
- BlockCipher: блочные шифры (IDEA, DES, AES и т.д.)
- CipherMode: режимы шифрования (ECB, CBC, CTR и т.д.)
"""

from abc import ABC, abstractmethod
from typing import List


class BlockCipher(ABC):
    """
    Абстрактный базовый класс для блочных шифров (Strategy).
    
    Каждый блочный шифр должен реализовать:
    - encrypt_block: шифрование одного блока
    - decrypt_block: расшифрование одного блока
    - block_size: размер блока в байтах
    - key_size: размер ключа в байтах
    """
    
    @property
    @abstractmethod
    def block_size(self) -> int:
        """Размер блока в байтах."""
        pass
    
    @property
    @abstractmethod
    def key_size(self) -> int:
        """Размер ключа в байтах."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Название алгоритма шифрования."""
        pass
    
    @abstractmethod
    def encrypt_block(self, block: bytes) -> bytes:
        """
        Зашифровать один блок данных.
        
        Args:
            block: Блок открытого текста размером block_size байт.
            
        Returns:
            Зашифрованный блок того же размера.
        """
        pass
    
    @abstractmethod
    def decrypt_block(self, block: bytes) -> bytes:
        """
        Расшифровать один блок данных.
        
        Args:
            block: Зашифрованный блок размером block_size байт.
            
        Returns:
            Расшифрованный блок того же размера.
        """
        pass


class CipherMode(ABC):
    """
    Абстрактный базовый класс для режимов шифрования (Strategy).
    
    Каждый режим должен реализовать:
    - encrypt: шифрование произвольных данных
    - decrypt: расшифрование произвольных данных
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Название режима шифрования."""
        pass
    
    @abstractmethod
    def encrypt(self, plaintext: bytes, cipher: BlockCipher) -> bytes:
        """
        Зашифровать данные используя заданный блочный шифр.
        
        Args:
            plaintext: Открытый текст.
            cipher: Блочный шифр для шифрования отдельных блоков.
            
        Returns:
            Зашифрованные данные.
        """
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: bytes, cipher: BlockCipher) -> bytes:
        """
        Расшифровать данные используя заданный блочный шифр.
        
        Args:
            ciphertext: Зашифрованный текст.
            cipher: Блочный шифр для расшифрования отдельных блоков.
            
        Returns:
            Расшифрованные данные.
        """
        pass
