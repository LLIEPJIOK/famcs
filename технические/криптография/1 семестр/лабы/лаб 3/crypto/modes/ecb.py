"""
Реализация режима ECB (Electronic Codebook).

ECB — простейший режим шифрования, где каждый блок шифруется независимо.

Характеристики:
- Шифрование параллелизуемо: Да
- Расшифрование параллелизуемо: Да
- Произвольный доступ для чтения: Да
- Поддержка неполного последнего блока: Нет (требуется паддинг)

ВНИМАНИЕ: ECB НЕ рекомендуется для криптографических протоколов!
Одинаковые блоки открытого текста дают одинаковые блоки шифротекста,
что раскрывает паттерны в данных.

Источник: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)
"""

from typing import List
from crypto.interfaces import CipherMode, BlockCipher


class ECBMode(CipherMode):
    """
    Режим шифрования ECB (Electronic Codebook).
    
    Простейший режим, где каждый блок обрабатывается независимо.
    В данной реализации последний неполный блок НЕ обрабатывается корректно
    (просто отбрасывается или дополняется нулями) согласно требованиям задания.
    """
    
    @property
    def name(self) -> str:
        return "ECB"
    
    def _split_into_blocks(self, data: bytes, block_size: int) -> List[bytes]:
        """
        Разбиение данных на блоки заданного размера.
        
        Последний блок дополняется нулями если его размер меньше block_size.
        Это упрощённая реализация без корректного паддинга.
        
        Args:
            data: Данные для разбиения.
            block_size: Размер блока в байтах.
            
        Returns:
            Список блоков.
        """
        blocks: List[bytes] = []
        
        for i in range(0, len(data), block_size):
            block = data[i:i + block_size]
            # Дополнение последнего блока нулями (упрощённый подход)
            if len(block) < block_size:
                block = block + bytes(block_size - len(block))
            blocks.append(block)
        
        return blocks
    
    def encrypt(self, plaintext: bytes, cipher: BlockCipher) -> bytes:
        """
        Зашифровать данные в режиме ECB.
        
        Каждый блок открытого текста шифруется независимо.
        Формула: C_i = E_K(P_i)
        
        Args:
            plaintext: Открытый текст.
            cipher: Блочный шифр.
            
        Returns:
            Зашифрованные данные.
        """
        if not plaintext:
            return bytes()
        
        block_size = cipher.block_size
        blocks = self._split_into_blocks(plaintext, block_size)
        
        ciphertext = bytes()
        for block in blocks:
            encrypted_block = cipher.encrypt_block(block)
            ciphertext += encrypted_block
        
        return ciphertext
    
    def decrypt(self, ciphertext: bytes, cipher: BlockCipher) -> bytes:
        """
        Расшифровать данные в режиме ECB.
        
        Каждый блок шифротекста расшифровывается независимо.
        Формула: P_i = D_K(C_i)
        
        Args:
            ciphertext: Зашифрованные данные.
            cipher: Блочный шифр.
            
        Returns:
            Расшифрованные данные.
            
        Raises:
            ValueError: Если длина шифротекста не кратна размеру блока.
        """
        if not ciphertext:
            return bytes()
        
        block_size = cipher.block_size
        
        if len(ciphertext) % block_size != 0:
            raise ValueError(
                f"Длина шифротекста ({len(ciphertext)}) должна быть "
                f"кратна размеру блока ({block_size})"
            )
        
        plaintext = bytes()
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i + block_size]
            decrypted_block = cipher.decrypt_block(block)
            plaintext += decrypted_block
        
        return plaintext
