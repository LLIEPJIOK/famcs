"""
Реализация режима CFB (Cipher Feedback).

CFB — режим обратной связи по шифротексту, превращающий блочный шифр
в самосинхронизирующийся потоковый шифр.

Характеристики:
- Шифрование параллелизуемо: Нет
- Расшифрование параллелизуемо: Да
- Произвольный доступ для чтения: Да
- Поддержка неполного последнего блока: Да

Формулы:
- Шифрование: C_i = E_K(C_{i-1}) ⊕ P_i, C_0 = IV
- Расшифрование: P_i = E_K(C_{i-1}) ⊕ C_i, C_0 = IV

ВАЖНО: 
- Используется ТОЛЬКО шифрование (не расшифрование) блочного шифра!
- Требуется уникальный IV для каждого шифрования!

Источник: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_feedback_(CFB)
"""

from crypto.interfaces import CipherMode, BlockCipher


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR двух байтовых строк (до минимальной длины)."""
    return bytes(x ^ y for x, y in zip(a, b))


class CFBMode(CipherMode):
    """
    Режим шифрования CFB (Cipher Feedback).
    
    Превращает блочный шифр в потоковый. Шифрует предыдущий блок шифротекста
    (или IV для первого блока) и XOR'ит результат с открытым текстом.
    
    Особенности:
    - Использует только шифрование блочного шифра (не расшифрование)
    - Не требует паддинга — работает с произвольной длиной данных
    - Ошибка в одном бите шифротекста влияет на расшифрование нескольких блоков
    
    Attributes:
        iv: Вектор инициализации (initialization vector).
    """
    
    def __init__(self, iv: bytes = None):
        """
        Инициализация режима CFB.
        
        Args:
            iv: Вектор инициализации. Если None, должен быть установлен
                через set_iv() перед использованием.
        """
        self._iv = iv
    
    @property
    def name(self) -> str:
        return "CFB"
    
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
    
    def encrypt(self, plaintext: bytes, cipher: BlockCipher) -> bytes:
        """
        Зашифровать данные в режиме CFB.
        
        C_i = E_K(C_{i-1}) ⊕ P_i, где C_0 = IV
        
        Работает с произвольной длиной данных (потоковый режим).
        
        Args:
            plaintext: Открытый текст.
            cipher: Блочный шифр.
            
        Returns:
            Зашифрованные данные (той же длины, что и plaintext).
            
        Raises:
            ValueError: Если IV не установлен или имеет неверный размер.
        """
        if not plaintext:
            return bytes()
        
        block_size = cipher.block_size
        self._validate_iv(block_size)
        
        ciphertext = bytes()
        feedback = self._iv
        
        for i in range(0, len(plaintext), block_size):
            # Берём блок открытого текста (может быть неполным)
            block = plaintext[i:i + block_size]
            # Шифруем feedback (предыдущий шифротекст или IV)
            keystream = cipher.encrypt_block(feedback)
            # XOR с открытым текстом (только нужное количество байт)
            encrypted_block = xor_bytes(block, keystream[:len(block)])
            ciphertext += encrypted_block
            # Обновляем feedback
            # Для полного блока — используем весь шифротекст
            # Для неполного — дополняем из предыдущего feedback
            if len(encrypted_block) == block_size:
                feedback = encrypted_block
            else:
                # Сдвигаем feedback и добавляем новые байты шифротекста
                feedback = feedback[len(encrypted_block):] + encrypted_block
        
        return ciphertext
    
    def decrypt(self, ciphertext: bytes, cipher: BlockCipher) -> bytes:
        """
        Расшифровать данные в режиме CFB.
        
        P_i = E_K(C_{i-1}) ⊕ C_i, где C_0 = IV
        
        ВАЖНО: Используется E_K (шифрование), а не D_K!
        
        Args:
            ciphertext: Зашифрованные данные.
            cipher: Блочный шифр.
            
        Returns:
            Расшифрованные данные (той же длины, что и ciphertext).
            
        Raises:
            ValueError: Если IV не установлен или имеет неверный размер.
        """
        if not ciphertext:
            return bytes()
        
        block_size = cipher.block_size
        self._validate_iv(block_size)
        
        plaintext = bytes()
        feedback = self._iv
        
        for i in range(0, len(ciphertext), block_size):
            # Берём блок шифротекста (может быть неполным)
            block = ciphertext[i:i + block_size]
            # Шифруем feedback (предыдущий шифротекст или IV)
            keystream = cipher.encrypt_block(feedback)
            # XOR с шифротекстом (только нужное количество байт)
            decrypted_block = xor_bytes(block, keystream[:len(block)])
            plaintext += decrypted_block
            # Обновляем feedback (используем ШИФРОТЕКСТ, не открытый текст!)
            if len(block) == block_size:
                feedback = block
            else:
                feedback = feedback[len(block):] + block
        
        return plaintext
