"""
Реализация режима CBC (Cipher Block Chaining).

CBC — режим сцепления блоков шифротекста, где каждый блок открытого текста
XOR'ится с предыдущим блоком шифротекста перед шифрованием.

Характеристики:
- Шифрование параллелизуемо: Нет
- Расшифрование параллелизуемо: Да
- Произвольный доступ для чтения: Да
- Поддержка неполного последнего блока: Нет (требуется паддинг)

Формулы:
- Шифрование: C_i = E_K(P_i ⊕ C_{i-1}), C_0 = IV
- Расшифрование: P_i = D_K(C_i) ⊕ C_{i-1}, C_0 = IV

ВАЖНО: Требуется уникальный непредсказуемый IV для каждого шифрования!

Источник: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)
"""

from typing import List
from crypto.interfaces import CipherMode, BlockCipher


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR двух байтовых строк одинаковой длины."""
    return bytes(x ^ y for x, y in zip(a, b))


class CBCMode(CipherMode):
    """
    Режим шифрования CBC (Cipher Block Chaining).
    
    Каждый блок открытого текста XOR'ится с предыдущим блоком шифротекста
    перед шифрованием. Первый блок XOR'ится с IV (вектором инициализации).
    
    Attributes:
        iv: Вектор инициализации (initialization vector).
    """
    
    def __init__(self, iv: bytes = None):
        """
        Инициализация режима CBC.
        
        Args:
            iv: Вектор инициализации. Если None, должен быть установлен
                через set_iv() перед использованием.
        """
        self._iv = iv
    
    @property
    def name(self) -> str:
        return "CBC"
    
    @property
    def iv(self) -> bytes:
        """Текущий вектор инициализации."""
        return self._iv
    
    def set_iv(self, iv: bytes) -> None:
        """
        Установить вектор инициализации.
        
        Args:
            iv: Новый вектор инициализации.
        """
        self._iv = iv
    
    def _validate_iv(self, block_size: int) -> None:
        """
        Проверить, что IV установлен и имеет правильный размер.
        
        Args:
            block_size: Ожидаемый размер IV в байтах.
            
        Raises:
            ValueError: Если IV не установлен или имеет неверный размер.
        """
        if self._iv is None:
            raise ValueError("IV (вектор инициализации) не установлен")
        if len(self._iv) != block_size:
            raise ValueError(
                f"Размер IV ({len(self._iv)}) должен быть равен "
                f"размеру блока ({block_size})"
            )
    
    def _split_into_blocks(self, data: bytes, block_size: int) -> List[bytes]:
        """
        Разбиение данных на блоки заданного размера.
        
        Последний блок дополняется нулями если его размер меньше block_size.
        
        Args:
            data: Данные для разбиения.
            block_size: Размер блока в байтах.
            
        Returns:
            Список блоков.
        """
        blocks: List[bytes] = []
        
        for i in range(0, len(data), block_size):
            block = data[i:i + block_size]
            if len(block) < block_size:
                block = block + bytes(block_size - len(block))
            blocks.append(block)
        
        return blocks
    
    def encrypt(self, plaintext: bytes, cipher: BlockCipher) -> bytes:
        """
        Зашифровать данные в режиме CBC.
        
        C_i = E_K(P_i ⊕ C_{i-1}), где C_0 = IV
        
        Args:
            plaintext: Открытый текст.
            cipher: Блочный шифр.
            
        Returns:
            Зашифрованные данные.
            
        Raises:
            ValueError: Если IV не установлен или имеет неверный размер.
        """
        if not plaintext:
            return bytes()
        
        block_size = cipher.block_size
        self._validate_iv(block_size)
        
        blocks = self._split_into_blocks(plaintext, block_size)
        
        ciphertext = bytes()
        previous_block = self._iv
        
        for block in blocks:
            # XOR с предыдущим блоком шифротекста (или IV для первого блока)
            xored = xor_bytes(block, previous_block)
            # Шифруем результат
            encrypted_block = cipher.encrypt_block(xored)
            ciphertext += encrypted_block
            # Сохраняем для следующей итерации
            previous_block = encrypted_block
        
        return ciphertext
    
    def decrypt(self, ciphertext: bytes, cipher: BlockCipher) -> bytes:
        """
        Расшифровать данные в режиме CBC.
        
        P_i = D_K(C_i) ⊕ C_{i-1}, где C_0 = IV
        
        Args:
            ciphertext: Зашифрованные данные.
            cipher: Блочный шифр.
            
        Returns:
            Расшифрованные данные.
            
        Raises:
            ValueError: Если IV не установлен, имеет неверный размер,
                       или длина шифротекста не кратна размеру блока.
        """
        if not ciphertext:
            return bytes()
        
        block_size = cipher.block_size
        self._validate_iv(block_size)
        
        if len(ciphertext) % block_size != 0:
            raise ValueError(
                f"Длина шифротекста ({len(ciphertext)}) должна быть "
                f"кратна размеру блока ({block_size})"
            )
        
        plaintext = bytes()
        previous_block = self._iv
        
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i + block_size]
            # Расшифровываем блок
            decrypted = cipher.decrypt_block(block)
            # XOR с предыдущим блоком шифротекста (или IV для первого блока)
            plaintext_block = xor_bytes(decrypted, previous_block)
            plaintext += plaintext_block
            # Сохраняем текущий блок шифротекста для следующей итерации
            previous_block = block
        
        return plaintext
