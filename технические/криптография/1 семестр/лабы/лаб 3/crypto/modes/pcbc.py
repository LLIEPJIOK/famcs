"""
Режим PCBC (Propagating Cipher Block Chaining).

В отличие от CBC, для XOR используется комбинация открытого текста
и шифротекста предыдущего блока.

Шифрование: C_i = E_K(P_i XOR (P_{i-1} XOR C_{i-1}))
Расшифрование: P_i = D_K(C_i) XOR (P_{i-1} XOR C_{i-1})

Для первого блока используется IV вместо (P_0 XOR C_0).

Особенности:
- Ошибка в одном блоке распространяется на все последующие блоки
  (как при шифровании, так и при расшифровании)
- Параллельное шифрование/расшифрование невозможно
- Используется в Kerberos v4, AFS
"""

from typing import Optional
from crypto.interfaces import CipherMode, BlockCipher


class PCBCMode(CipherMode):
    """
    Режим Propagating Cipher Block Chaining (PCBC).
    
    Требует вектор инициализации (IV) размером равным блоку шифра.
    """
    
    def __init__(self, iv: Optional[bytes] = None):
        """
        Инициализация PCBC режима.
        
        Args:
            iv: Вектор инициализации (должен быть равен размеру блока).
        """
        self._iv = iv
    
    @property
    def name(self) -> str:
        return "PCBC"
    
    def set_iv(self, iv: bytes) -> None:
        """Установить вектор инициализации."""
        self._iv = iv
    
    def _xor_bytes(self, a: bytes, b: bytes) -> bytes:
        """XOR двух байтовых последовательностей."""
        return bytes(x ^ y for x, y in zip(a, b))
    
    def encrypt(self, plaintext: bytes, cipher: BlockCipher) -> bytes:
        """
        Зашифровать данные в режиме PCBC.
        
        Args:
            plaintext: Открытый текст (должен быть кратен размеру блока).
            cipher: Блочный шифр.
            
        Returns:
            Зашифрованные данные.
        """
        if self._iv is None:
            raise ValueError("PCBC режим требует вектор инициализации (IV)")
        
        block_size = cipher.block_size
        
        if len(self._iv) != block_size:
            raise ValueError(
                f"Размер IV ({len(self._iv)}) должен быть равен "
                f"размеру блока ({block_size})"
            )
        
        if not plaintext:
            return bytes()
        
        if len(plaintext) % block_size != 0:
            raise ValueError(
                f"Длина открытого текста ({len(plaintext)}) должна быть "
                f"кратна размеру блока ({block_size})"
            )
        
        ciphertext = bytearray()
        
        # Для первого блока используем IV
        prev_xor = self._iv
        
        for i in range(0, len(plaintext), block_size):
            plaintext_block = plaintext[i:i + block_size]
            
            # XOR с предыдущим (P XOR C) или IV для первого блока
            xored = self._xor_bytes(plaintext_block, prev_xor)
            
            # Шифруем
            ciphertext_block = cipher.encrypt_block(xored)
            ciphertext.extend(ciphertext_block)
            
            # Обновляем prev_xor = P_i XOR C_i
            prev_xor = self._xor_bytes(plaintext_block, ciphertext_block)
        
        return bytes(ciphertext)
    
    def decrypt(self, ciphertext: bytes, cipher: BlockCipher) -> bytes:
        """
        Расшифровать данные в режиме PCBC.
        
        Args:
            ciphertext: Зашифрованные данные.
            cipher: Блочный шифр.
            
        Returns:
            Расшифрованные данные.
        """
        if self._iv is None:
            raise ValueError("PCBC режим требует вектор инициализации (IV)")
        
        block_size = cipher.block_size
        
        if len(self._iv) != block_size:
            raise ValueError(
                f"Размер IV ({len(self._iv)}) должен быть равен "
                f"размеру блока ({block_size})"
            )
        
        if not ciphertext:
            return bytes()
        
        if len(ciphertext) % block_size != 0:
            raise ValueError(
                f"Длина шифротекста ({len(ciphertext)}) должна быть "
                f"кратна размеру блока ({block_size})"
            )
        
        plaintext = bytearray()
        
        # Для первого блока используем IV
        prev_xor = self._iv
        
        for i in range(0, len(ciphertext), block_size):
            ciphertext_block = ciphertext[i:i + block_size]
            
            # Расшифровываем
            decrypted = cipher.decrypt_block(ciphertext_block)
            
            # XOR с предыдущим (P XOR C) или IV для первого блока
            plaintext_block = self._xor_bytes(decrypted, prev_xor)
            plaintext.extend(plaintext_block)
            
            # Обновляем prev_xor = P_i XOR C_i
            prev_xor = self._xor_bytes(plaintext_block, ciphertext_block)
        
        return bytes(plaintext)
