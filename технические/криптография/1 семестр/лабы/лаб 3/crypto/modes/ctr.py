"""
Реализация режима CTR (Counter).

CTR — режим счётчика, превращающий блочный шифр в потоковый шифр
путём шифрования последовательных значений счётчика.

Характеристики:
- Шифрование параллелизуемо: Да
- Расшифрование параллелизуемо: Да
- Произвольный доступ для чтения: Да
- Поддержка неполного последнего блока: Да

Формулы:
- Генерация ключевого потока: O_i = E_K(IV + i) или E_K(Nonce || Counter_i)
- Шифрование: C_i = P_i ⊕ O_i
- Расшифрование: P_i = C_i ⊕ O_i

Особенности:
- Параллелизуемость — блоки можно обрабатывать независимо
- Симметричность — шифрование и расшифрование идентичны
- Произвольный доступ — можно расшифровать любой блок независимо

ВАЖНО: 
- НИКОГДА не используйте один и тот же nonce/IV с одним ключом дважды!
- Это приведёт к повторению ключевого потока и катастрофической потере безопасности!

Источник: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR)
"""

from crypto.interfaces import CipherMode, BlockCipher


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR двух байтовых строк (до минимальной длины)."""
    return bytes(x ^ y for x, y in zip(a, b))


def increment_counter(counter: bytes) -> bytes:
    """
    Инкрементировать счётчик (big-endian).
    
    Args:
        counter: Текущее значение счётчика.
        
    Returns:
        Счётчик + 1 (с переполнением).
    """
    counter_int = int.from_bytes(counter, 'big')
    counter_int = (counter_int + 1) % (2 ** (len(counter) * 8))
    return counter_int.to_bytes(len(counter), 'big')


class CTRMode(CipherMode):
    """
    Режим шифрования CTR (Counter).
    
    Генерирует ключевой поток, шифруя последовательные значения счётчика.
    Затем XOR'ит ключевой поток с открытым текстом.
    
    Особенности:
    - Полностью параллелизуемый (в отличие от CBC, CFB, OFB)
    - Использует только шифрование блочного шифра
    - Шифрование и расшифрование идентичны (симметрия XOR)
    - Не требует паддинга — работает с произвольной длиной данных
    - Поддерживает произвольный доступ к блокам
    
    Реализация счётчика:
    - Используется простой инкремент nonce как целого числа (big-endian)
    - Можно также использовать конкатенацию nonce и отдельного счётчика
    
    Attributes:
        nonce: Уникальное значение для каждого сообщения (аналог IV).
    """
    
    def __init__(self, nonce: bytes = None, iv: bytes = None):
        """
        Инициализация режима CTR.
        
        Args:
            nonce: Уникальное значение (number used once). Если None, 
                   должен быть установлен через set_nonce() перед использованием.
            iv: Алиас для nonce (для совместимости с другими режимами).
        """
        self._nonce = nonce if nonce is not None else iv
    
    @property
    def name(self) -> str:
        return "CTR"
    
    @property
    def iv(self) -> bytes:
        """Текущий nonce (для совместимости с интерфейсом)."""
        return self._nonce
    
    @property
    def nonce(self) -> bytes:
        """Текущий nonce."""
        return self._nonce
    
    def set_iv(self, iv: bytes) -> None:
        """
        Установить nonce (синоним set_nonce для совместимости).
        
        Args:
            iv: Новый nonce.
        """
        self._nonce = iv
    
    def set_nonce(self, nonce: bytes) -> None:
        """
        Установить nonce.
        
        Args:
            nonce: Новый nonce.
        """
        self._nonce = nonce
    
    def _validate_nonce(self, block_size: int) -> None:
        """
        Проверить, что nonce установлен и имеет правильный размер.
        
        Args:
            block_size: Ожидаемый размер nonce в байтах.
            
        Raises:
            ValueError: Если nonce не установлен или имеет неверный размер.
        """
        if self._nonce is None:
            raise ValueError("Nonce (синхропосылка) не установлен")
        if len(self._nonce) != block_size:
            raise ValueError(
                f"Размер nonce ({len(self._nonce)}) должен быть равен "
                f"размеру блока ({block_size})"
            )
    
    def _process(self, data: bytes, cipher: BlockCipher) -> bytes:
        """
        Обработка данных (шифрование или расшифрование — идентичны в CTR).
        
        C_i = P_i ⊕ E_K(Nonce + i)
        
        Args:
            data: Входные данные.
            cipher: Блочный шифр.
            
        Returns:
            Обработанные данные (той же длины, что и data).
            
        Raises:
            ValueError: Если nonce не установлен или имеет неверный размер.
        """
        if not data:
            return bytes()
        
        block_size = cipher.block_size
        self._validate_nonce(block_size)
        
        result = bytes()
        counter = self._nonce
        
        for i in range(0, len(data), block_size):
            # Берём блок данных (может быть неполным)
            block = data[i:i + block_size]
            # Генерируем блок ключевого потока из счётчика
            keystream = cipher.encrypt_block(counter)
            # XOR с данными (только нужное количество байт)
            processed_block = xor_bytes(block, keystream[:len(block)])
            result += processed_block
            # Инкрементируем счётчик
            counter = increment_counter(counter)
        
        return result
    
    def encrypt(self, plaintext: bytes, cipher: BlockCipher) -> bytes:
        """
        Зашифровать данные в режиме CTR.
        
        C_i = P_i ⊕ E_K(Nonce + i)
        
        Args:
            plaintext: Открытый текст.
            cipher: Блочный шифр.
            
        Returns:
            Зашифрованные данные (той же длины, что и plaintext).
            
        Raises:
            ValueError: Если nonce не установлен или имеет неверный размер.
        """
        return self._process(plaintext, cipher)
    
    def decrypt(self, ciphertext: bytes, cipher: BlockCipher) -> bytes:
        """
        Расшифровать данные в режиме CTR.
        
        P_i = C_i ⊕ E_K(Nonce + i)
        
        Идентично шифрованию благодаря симметрии XOR.
        
        Args:
            ciphertext: Зашифрованные данные.
            cipher: Блочный шифр.
            
        Returns:
            Расшифрованные данные (той же длины, что и ciphertext).
            
        Raises:
            ValueError: Если nonce не установлен или имеет неверный размер.
        """
        return self._process(ciphertext, cipher)
    
    def encrypt_block_at(self, plaintext_block: bytes, block_index: int, 
                         cipher: BlockCipher) -> bytes:
        """
        Зашифровать блок по указанному индексу (произвольный доступ).
        
        Args:
            plaintext_block: Блок открытого текста.
            block_index: Индекс блока (начиная с 0).
            cipher: Блочный шифр.
            
        Returns:
            Зашифрованный блок.
            
        Raises:
            ValueError: Если nonce не установлен или имеет неверный размер.
        """
        block_size = cipher.block_size
        self._validate_nonce(block_size)
        
        # Вычисляем значение счётчика для данного индекса
        counter_int = int.from_bytes(self._nonce, 'big') + block_index
        counter_int = counter_int % (2 ** (block_size * 8))
        counter = counter_int.to_bytes(block_size, 'big')
        
        # Генерируем ключевой поток и XOR'им
        keystream = cipher.encrypt_block(counter)
        return xor_bytes(plaintext_block, keystream[:len(plaintext_block)])
    
    def decrypt_block_at(self, ciphertext_block: bytes, block_index: int,
                         cipher: BlockCipher) -> bytes:
        """
        Расшифровать блок по указанному индексу (произвольный доступ).
        
        Args:
            ciphertext_block: Блок шифротекста.
            block_index: Индекс блока (начиная с 0).
            cipher: Блочный шифр.
            
        Returns:
            Расшифрованный блок.
        """
        # Идентично шифрованию в режиме CTR
        return self.encrypt_block_at(ciphertext_block, block_index, cipher)
