"""
Реализация алгоритма IDEA (International Data Encryption Algorithm).

IDEA — симметричный блочный шифр, разработанный Xuejia Lai и James Massey (1991).

Характеристики:
- Размер блока: 64 бита (8 байт)
- Размер ключа: 128 бит (16 байт)
- Число раундов: 8 полных + 1 выходное преобразование (8.5 раундов)
- Использует операции из разных алгебраических групп:
  - XOR (⊕)
  - Сложение по модулю 2^16 (⊞)
  - Умножение по модулю 2^16 + 1 (⊙)

Источник: https://en.wikipedia.org/wiki/International_Data_Encryption_Algorithm
"""

from typing import List, Tuple
from crypto.interfaces import BlockCipher


class IDEACipher(BlockCipher):
    """
    Реализация блочного шифра IDEA.
    
    Алгоритм использует структуру Lai-Massey с 8 полными раундами
    и финальным полураундом (выходное преобразование).
    """
    
    _BLOCK_SIZE = 8   # 64 бита
    _KEY_SIZE = 16    # 128 бит
    _ROUNDS = 8
    _MODULO_ADD = 0x10000        # 2^16 для сложения
    _MODULO_MUL = 0x10001        # 2^16 + 1 для умножения
    
    def __init__(self, key: bytes):
        """
        Инициализация шифра с заданным ключом.
        
        Args:
            key: Ключ шифрования (16 байт / 128 бит).
            
        Raises:
            ValueError: Если длина ключа не равна 16 байт.
        """
        if len(key) != self._KEY_SIZE:
            raise ValueError(f"Ключ IDEA должен быть {self._KEY_SIZE} байт, получено {len(key)}")
        
        self._key = key
        self._encrypt_subkeys = self._generate_encryption_subkeys()
        self._decrypt_subkeys = self._generate_decryption_subkeys()
    
    @property
    def block_size(self) -> int:
        return self._BLOCK_SIZE
    
    @property
    def key_size(self) -> int:
        return self._KEY_SIZE
    
    @property
    def name(self) -> str:
        return "IDEA"
    
    @staticmethod
    def mul_mod(a: int, b: int) -> int:
        """
        Умножение по модулю 2^16 + 1 с особой обработкой нуля.
        
        В IDEA 0x0000 интерпретируется как 2^16 на входе,
        а 2^16 на выходе заменяется на 0x0000.
        
        Источник: https://en.wikipedia.org/wiki/International_Data_Encryption_Algorithm#Operation
        
        Args:
            a: Первый операнд (16-битное число).
            b: Второй операнд (16-битное число).
            
        Returns:
            Результат умножения по модулю 2^16 + 1.
        """
        if a == 0:
            a = 0x10000  # 2^16
        if b == 0:
            b = 0x10000
        
        result = (a * b) % 0x10001  # mod (2^16 + 1)
        
        if result == 0x10000:
            return 0
        return result
    
    @staticmethod
    def add_mod(a: int, b: int) -> int:
        """
        Сложение по модулю 2^16.
        
        Args:
            a: Первый операнд (16-битное число).
            b: Второй операнд (16-битное число).
            
        Returns:
            Сумма по модулю 2^16.
        """
        return (a + b) & 0xFFFF
    
    @staticmethod
    def sub_mod(a: int, b: int) -> int:
        """
        Вычитание по модулю 2^16 (аддитивная инверсия).
        
        Args:
            a: Первый операнд.
            b: Второй операнд (вычитаемое).
            
        Returns:
            Разность по модулю 2^16.
        """
        return (a - b) & 0xFFFF
    
    @staticmethod
    def mul_inv(a: int) -> int:
        """
        Мультипликативная инверсия по модулю 2^16 + 1.
        
        Использует расширенный алгоритм Евклида.
        
        Args:
            a: Число для инвертирования.
            
        Returns:
            Мультипликативная инверсия a по модулю 2^16 + 1.
        """
        if a == 0:
            return 0
        
        modulo = 0x10001  # 2^16 + 1
        
        # Расширенный алгоритм Евклида
        t, new_t = 0, 1
        r, new_r = modulo, a
        
        while new_r != 0:
            quotient = r // new_r
            t, new_t = new_t, t - quotient * new_t
            r, new_r = new_r, r - quotient * new_r
        
        if t < 0:
            t += modulo
            
        return t if t != 0x10000 else 0
    
    @staticmethod
    def add_inv(a: int) -> int:
        """
        Аддитивная инверсия по модулю 2^16.
        
        Args:
            a: Число для инвертирования.
            
        Returns:
            Аддитивная инверсия: (-a) mod 2^16.
        """
        return (0x10000 - a) & 0xFFFF
    
    def _generate_encryption_subkeys(self) -> List[int]:
        """
        Генерация подключей для шифрования.
        
        Алгоритм:
        1. Первые 8 подключей — 16-битные слова из исходного ключа.
        2. Далее ключ циклически сдвигается влево на 25 бит,
           и извлекаются следующие 8 подключей.
        3. Процесс повторяется до получения 52 подключей.
        
        Источник: https://en.wikipedia.org/wiki/International_Data_Encryption_Algorithm#Key_schedule
        
        Returns:
            Список из 52 16-битных подключей.
        """
        # Преобразование ключа в 128-битное число
        key_int = int.from_bytes(self._key, byteorder='big')
        
        subkeys: List[int] = []
        
        # Нужно 52 подключа: 8 раундов × 6 + 4 для выходного преобразования
        for i in range(52):
            # Позиция 16-битного слова в текущем состоянии ключа
            position = (i % 8) * 16
            
            # Извлечение 16-битного слова
            subkey = (key_int >> (128 - 16 - position)) & 0xFFFF
            subkeys.append(subkey)
            
            # После каждых 8 подключей - циклический сдвиг влево на 25 бит
            if (i + 1) % 8 == 0:
                key_int = ((key_int << 25) | (key_int >> (128 - 25))) & ((1 << 128) - 1)
        
        return subkeys
    
    def _generate_decryption_subkeys(self) -> List[int]:
        """
        Генерация подключей для расшифрования.
        
        Подключи для расшифрования — это инвертированные и переставленные
        подключи шифрования.
        
        Источник: https://en.wikipedia.org/wiki/International_Data_Encryption_Algorithm#Decryption
        
        Returns:
            Список из 52 16-битных подключей для расшифрования.
        """
        enc = self._encrypt_subkeys
        dec: List[int] = [0] * 52
        
        # Выходное преобразование (индексы 48-51 для шифрования -> 0-3 для расшифрования)
        dec[0] = self.mul_inv(enc[48])
        dec[1] = self.add_inv(enc[49])
        dec[2] = self.add_inv(enc[50])
        dec[3] = self.mul_inv(enc[51])
        dec[4] = enc[46]
        dec[5] = enc[47]
        
        # Раунды 1-7 (в обратном порядке)
        for r in range(1, 8):
            base_enc = (8 - r) * 6
            base_dec = r * 6
            
            dec[base_dec + 0] = self.mul_inv(enc[base_enc + 0])
            dec[base_dec + 1] = self.add_inv(enc[base_enc + 2])  # Порядок меняется!
            dec[base_dec + 2] = self.add_inv(enc[base_enc + 1])
            dec[base_dec + 3] = self.mul_inv(enc[base_enc + 3])
            dec[base_dec + 4] = enc[base_enc - 2]
            dec[base_dec + 5] = enc[base_enc - 1]
        
        # Последний раунд расшифрования (соответствует первому раунду шифрования)
        dec[48] = self.mul_inv(enc[0])
        dec[49] = self.add_inv(enc[1])
        dec[50] = self.add_inv(enc[2])
        dec[51] = self.mul_inv(enc[3])
        
        return dec
    
    def _idea_round(self, x1: int, x2: int, x3: int, x4: int, 
                    subkeys: List[int], round_num: int) -> Tuple[int, int, int, int]:
        """
        Один раунд IDEA.
        
        Args:
            x1, x2, x3, x4: 16-битные слова входного блока.
            subkeys: Список подключей.
            round_num: Номер раунда (0-7).
            
        Returns:
            Кортеж из 4 16-битных слов после раунда.
        """
        base = round_num * 6
        k1, k2, k3, k4, k5, k6 = subkeys[base:base + 6]
        
        # Шаг 1: применение подключей
        y1 = self.mul_mod(x1, k1)
        y2 = self.add_mod(x2, k2)
        y3 = self.add_mod(x3, k3)
        y4 = self.mul_mod(x4, k4)
        
        # Шаг 2: MA (Multiplication-Addition) структура
        t1 = y1 ^ y3
        t2 = y2 ^ y4
        
        t3 = self.mul_mod(t1, k5)
        t4 = self.add_mod(t2, t3)
        t5 = self.mul_mod(t4, k6)
        t6 = self.add_mod(t3, t5)
        
        # Шаг 3: финальные XOR
        r1 = y1 ^ t5
        r2 = y3 ^ t5
        r3 = y2 ^ t6
        r4 = y4 ^ t6
        
        return r1, r2, r3, r4
    
    def _output_transformation(self, x1: int, x2: int, x3: int, x4: int,
                               subkeys: List[int]) -> Tuple[int, int, int, int]:
        """
        Выходное преобразование (половина раунда).
        
        Args:
            x1, x2, x3, x4: 16-битные слова.
            subkeys: Список подключей (используются индексы 48-51).
            
        Returns:
            Кортеж из 4 16-битных слов после преобразования.
        """
        k1, k2, k3, k4 = subkeys[48:52]
        
        y1 = self.mul_mod(x1, k1)
        y2 = self.add_mod(x2, k2)
        y3 = self.add_mod(x3, k3)
        y4 = self.mul_mod(x4, k4)
        
        return y1, y2, y3, y4
    
    def _process_block(self, block: bytes, subkeys: List[int]) -> bytes:
        """
        Обработка одного 64-битного блока.
        
        Args:
            block: 8-байтовый блок данных.
            subkeys: Подключи (шифрования или расшифрования).
            
        Returns:
            Обработанный 8-байтовый блок.
        """
        # Разбиение блока на 4 16-битных слова (big-endian)
        x1 = (block[0] << 8) | block[1]
        x2 = (block[2] << 8) | block[3]
        x3 = (block[4] << 8) | block[5]
        x4 = (block[6] << 8) | block[7]
        
        # 8 полных раундов
        for r in range(self._ROUNDS):
            x1, x2, x3, x4 = self._idea_round(x1, x2, x3, x4, subkeys, r)
        
        # Выходное преобразование (с учётом отмены последнего swap)
        # После 8 раунда x2 и x3 поменяны местами, поэтому меняем их обратно
        y1, y2, y3, y4 = self._output_transformation(x1, x3, x2, x4, subkeys)
        
        # Сборка результата
        return bytes([
            (y1 >> 8) & 0xFF, y1 & 0xFF,
            (y2 >> 8) & 0xFF, y2 & 0xFF,
            (y3 >> 8) & 0xFF, y3 & 0xFF,
            (y4 >> 8) & 0xFF, y4 & 0xFF,
        ])
    
    def encrypt_block(self, block: bytes) -> bytes:
        """
        Зашифровать один 64-битный блок.
        
        Args:
            block: Блок открытого текста (8 байт).
            
        Returns:
            Зашифрованный блок (8 байт).
            
        Raises:
            ValueError: Если размер блока не равен 8 байт.
        """
        if len(block) != self._BLOCK_SIZE:
            raise ValueError(f"Размер блока должен быть {self._BLOCK_SIZE} байт")
        
        return self._process_block(block, self._encrypt_subkeys)
    
    def decrypt_block(self, block: bytes) -> bytes:
        """
        Расшифровать один 64-битный блок.
        
        Args:
            block: Зашифрованный блок (8 байт).
            
        Returns:
            Расшифрованный блок (8 байт).
            
        Raises:
            ValueError: Если размер блока не равен 8 байт.
        """
        if len(block) != self._BLOCK_SIZE:
            raise ValueError(f"Размер блока должен быть {self._BLOCK_SIZE} байт")
        
        return self._process_block(block, self._decrypt_subkeys)
