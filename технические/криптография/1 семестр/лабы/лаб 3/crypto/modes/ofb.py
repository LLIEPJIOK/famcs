"""
Реализация режима OFB (Output Feedback).

OFB — режим обратной связи по выходу, превращающий блочный шифр
в синхронный потоковый шифр.

Характеристики:
- Шифрование параллелизуемо: Нет
- Расшифрование параллелизуемо: Нет
- Произвольный доступ для чтения: Нет
- Поддержка неполного последнего блока: Да

Формулы:
- Генерация ключевого потока: O_j = E_K(I_j), I_j = O_{j-1}, I_0 = IV
- Шифрование: C_j = P_j ⊕ O_j
- Расшифрование: P_j = C_j ⊕ O_j

Особенности:
- Симметричность: шифрование и расшифрование идентичны
- Ключевой поток можно предвычислить заранее
- Ошибка в одном бите влияет только на соответствующий бит

ВАЖНО: Повторное использование IV приводит к повторению ключевого потока!

Источник: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Output_feedback_(OFB)
"""

from crypto.interfaces import CipherMode, BlockCipher


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR двух байтовых строк (до минимальной длины)."""
    return bytes(x ^ y for x, y in zip(a, b))


class OFBMode(CipherMode):
    """
    Режим шифрования OFB (Output Feedback).
    
    Генерирует ключевой поток, последовательно шифруя предыдущий выход
    блочного шифра. Затем XOR'ит ключевой поток с открытым текстом.
    
    Особенности:
    - Использует только шифрование блочного шифра
    - Шифрование и расшифрование идентичны (симметрия XOR)
    - Не требует паддинга — работает с произвольной длиной данных
    - Ошибка в одном бите шифротекста влияет только на один бит открытого текста
    - Ключевой поток можно вычислить заранее (до получения данных)
    
    Attributes:
        iv: Вектор инициализации (initialization vector).
    """
    
    def __init__(self, iv: bytes = None):
        """
        Инициализация режима OFB.
        
        Args:
            iv: Вектор инициализации. Если None, должен быть установлен
                через set_iv() перед использованием.
        """
        self._iv = iv
    
    @property
    def name(self) -> str:
        return "OFB"
    
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
    
    def _process(self, data: bytes, cipher: BlockCipher) -> bytes:
        """
        Обработка данных (шифрование или расшифрование — идентичны в OFB).
        
        C_j = P_j ⊕ O_j, где O_j = E_K(O_{j-1}), O_0 = E_K(IV)
        
        Args:
            data: Входные данные.
            cipher: Блочный шифр.
            
        Returns:
            Обработанные данные (той же длины, что и data).
            
        Raises:
            ValueError: Если IV не установлен или имеет неверный размер.
        """
        if not data:
            return bytes()
        
        block_size = cipher.block_size
        self._validate_iv(block_size)
        
        result = bytes()
        output_block = self._iv
        
        for i in range(0, len(data), block_size):
            # Берём блок данных (может быть неполным)
            block = data[i:i + block_size]
            # Генерируем следующий блок ключевого потока
            output_block = cipher.encrypt_block(output_block)
            # XOR с данными (только нужное количество байт)
            processed_block = xor_bytes(block, output_block[:len(block)])
            result += processed_block
        
        return result
    
    def encrypt(self, plaintext: bytes, cipher: BlockCipher) -> bytes:
        """
        Зашифровать данные в режиме OFB.
        
        C_j = P_j ⊕ O_j
        
        Args:
            plaintext: Открытый текст.
            cipher: Блочный шифр.
            
        Returns:
            Зашифрованные данные (той же длины, что и plaintext).
            
        Raises:
            ValueError: Если IV не установлен или имеет неверный размер.
        """
        return self._process(plaintext, cipher)
    
    def decrypt(self, ciphertext: bytes, cipher: BlockCipher) -> bytes:
        """
        Расшифровать данные в режиме OFB.
        
        P_j = C_j ⊕ O_j
        
        Идентично шифрованию благодаря симметрии XOR.
        
        Args:
            ciphertext: Зашифрованные данные.
            cipher: Блочный шифр.
            
        Returns:
            Расшифрованные данные (той же длины, что и ciphertext).
            
        Raises:
            ValueError: Если IV не установлен или имеет неверный размер.
        """
        return self._process(ciphertext, cipher)
