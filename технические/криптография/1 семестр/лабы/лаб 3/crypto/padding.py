"""
Интерфейс и реализации схем дополнения (padding) для блочных шифров.

Схемы дополнения необходимы для режимов ECB и CBC, где длина данных
должна быть кратна размеру блока.

Поддерживаемые схемы (согласно ТЗ):
- PKCS7: стандарт PKCS#7 (каждый байт = количество добавленных)
- ISO7816: bit padding по ISO/IEC 7816-4 (0x80 + нули)
- ANSI_X923: нули + последний байт = количество
- ISO10126: случайные байты + последний байт = количество
- None: без дополнения (данные должны быть кратны блоку)

Ссылки:
- PKCS#7: RFC 5652, Section 6.3
- ISO/IEC 7816-4: https://en.wikipedia.org/wiki/Padding_(cryptography)#ISO/IEC_7816-4
- ANSI X9.23: https://en.wikipedia.org/wiki/Padding_(cryptography)#ANSI_X9.23
- ISO 10126: https://en.wikipedia.org/wiki/Padding_(cryptography)#ISO_10126
"""

from abc import ABC, abstractmethod
from typing import Dict, Type
import secrets


class PaddingScheme(ABC):
    """
    Абстрактный базовый класс для схем дополнения.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Название схемы дополнения."""
        pass
    
    @abstractmethod
    def pad(self, data: bytes, block_size: int) -> bytes:
        """
        Дополнить данные до кратности размеру блока.
        
        Args:
            data: Исходные данные.
            block_size: Размер блока в байтах.
            
        Returns:
            Данные с дополнением.
        """
        pass
    
    @abstractmethod
    def unpad(self, data: bytes, block_size: int) -> bytes:
        """
        Удалить дополнение из данных.
        
        Args:
            data: Данные с дополнением.
            block_size: Размер блока в байтах.
            
        Returns:
            Исходные данные без дополнения.
        """
        pass


class PKCS7Padding(PaddingScheme):
    """
    Дополнение по стандарту PKCS#7 (RFC 5652).
    
    Каждый байт дополнения равен количеству добавленных байтов.
    Если данные уже кратны блоку - добавляется полный блок дополнения.
    
    Пример (блок 8 байт):
        "Hello" (5 байт) -> "Hello\x03\x03\x03" (3 байта дополнения)
        "12345678" (8 байт) -> "12345678\x08\x08\x08\x08\x08\x08\x08\x08"
    
    Это стандартная схема для AES, TLS и многих других протоколов.
    """
    
    @property
    def name(self) -> str:
        return "PKCS7"
    
    def pad(self, data: bytes, block_size: int) -> bytes:
        padding_len = block_size - (len(data) % block_size)
        # В PKCS7 всегда добавляется хотя бы 1 байт (если кратно - полный блок)
        padding = bytes([padding_len] * padding_len)
        return data + padding
    
    def unpad(self, data: bytes, block_size: int) -> bytes:
        if not data:
            return data
        
        # Последний байт указывает длину дополнения
        padding_len = data[-1]
        
        # Валидация
        if padding_len == 0 or padding_len > block_size:
            raise ValueError(
                f"Некорректное PKCS7 дополнение: длина {padding_len} "
                f"(должна быть 1-{block_size})"
            )
        
        if len(data) < padding_len:
            raise ValueError(
                f"Данные ({len(data)} байт) короче дополнения ({padding_len})"
            )
        
        # Проверяем что все байты дополнения корректны
        padding = data[-padding_len:]
        if not all(b == padding_len for b in padding):
            raise ValueError("Некорректное PKCS7 дополнение: байты не совпадают")
        
        return data[:-padding_len]


class ISO7816Padding(PaddingScheme):
    """
    Дополнение по стандарту ISO/IEC 7816-4 (bit padding).
    
    Добавляется байт 0x80 (10000000 в бинарном виде), затем нули.
    Если данные кратны блоку - добавляется полный блок.
    
    Пример (блок 8 байт):
        "Hello" (5 байт) -> "Hello\x80\x00\x00"
        "12345678" (8 байт) -> "12345678\x80\x00\x00\x00\x00\x00\x00\x00"
    
    Используется в смарт-картах и некоторых криптопротоколах.
    """
    
    @property
    def name(self) -> str:
        return "ISO7816"
    
    def pad(self, data: bytes, block_size: int) -> bytes:
        padding_len = block_size - (len(data) % block_size)
        # Всегда добавляем 0x80 + нули
        padding = b'\x80' + bytes(padding_len - 1)
        return data + padding
    
    def unpad(self, data: bytes, block_size: int) -> bytes:
        if not data:
            return data
        
        # Ищем 0x80 с конца, пропуская нули
        i = len(data) - 1
        while i >= 0 and data[i] == 0:
            i -= 1
        
        if i < 0 or data[i] != 0x80:
            raise ValueError("Некорректное ISO7816 дополнение: маркер 0x80 не найден")
        
        return data[:i]


class ANSIX923Padding(PaddingScheme):
    """
    Дополнение по стандарту ANSI X9.23.
    
    Добавляются нулевые байты, последний байт = количество добавленных.
    Если данные кратны блоку - добавляется полный блок.
    
    Пример (блок 8 байт):
        "Hello" (5 байт) -> "Hello\x00\x00\x03"
        "12345678" (8 байт) -> "12345678\x00\x00\x00\x00\x00\x00\x00\x08"
    """
    
    @property
    def name(self) -> str:
        return "ANSI_X923"
    
    def pad(self, data: bytes, block_size: int) -> bytes:
        padding_len = block_size - (len(data) % block_size)
        # Нули + последний байт = длина
        padding = bytes(padding_len - 1) + bytes([padding_len])
        return data + padding
    
    def unpad(self, data: bytes, block_size: int) -> bytes:
        if not data:
            return data
        
        padding_len = data[-1]
        
        if padding_len == 0 or padding_len > block_size:
            raise ValueError(
                f"Некорректное ANSI X9.23 дополнение: длина {padding_len}"
            )
        
        if len(data) < padding_len:
            raise ValueError(
                f"Данные ({len(data)} байт) короче дополнения ({padding_len})"
            )
        
        # Проверяем что все байты кроме последнего - нули
        padding = data[-(padding_len):-1]
        if not all(b == 0 for b in padding):
            raise ValueError("Некорректное ANSI X9.23 дополнение: не все байты нулевые")
        
        return data[:-padding_len]


class ISO10126Padding(PaddingScheme):
    """
    Дополнение по стандарту ISO 10126 (withdrawn в 2007).
    
    Добавляются случайные байты, последний байт = количество добавленных.
    Если данные кратны блоку - добавляется полный блок.
    
    Пример (блок 8 байт):
        "Hello" (5 байт) -> "Hello\x81\xA6\x03" (случайные + 03)
        "12345678" (8 байт) -> "12345678" + 7 случайных + "\x08"
    
    Преимущество: случайные данные усложняют криптоанализ.
    """
    
    @property
    def name(self) -> str:
        return "ISO10126"
    
    def pad(self, data: bytes, block_size: int) -> bytes:
        padding_len = block_size - (len(data) % block_size)
        # Случайные байты + последний байт = длина
        random_bytes = secrets.token_bytes(padding_len - 1)
        padding = random_bytes + bytes([padding_len])
        return data + padding
    
    def unpad(self, data: bytes, block_size: int) -> bytes:
        if not data:
            return data
        
        padding_len = data[-1]
        
        if padding_len == 0 or padding_len > block_size:
            raise ValueError(
                f"Некорректное ISO 10126 дополнение: длина {padding_len}"
            )
        
        if len(data) < padding_len:
            raise ValueError(
                f"Данные ({len(data)} байт) короче дополнения ({padding_len})"
            )
        
        # При ISO 10126 не проверяем содержимое (там случайные байты)
        return data[:-padding_len]


class NonePadding(PaddingScheme):
    """
    Без дополнения.
    
    Данные должны быть кратны размеру блока.
    Используется когда дополнение обрабатывается внешним кодом
    или для потоковых режимов (CFB, OFB, CTR).
    """
    
    @property
    def name(self) -> str:
        return "None"
    
    def pad(self, data: bytes, block_size: int) -> bytes:
        if len(data) % block_size != 0:
            raise ValueError(
                f"Режим 'None': длина данных ({len(data)}) "
                f"должна быть кратна размеру блока ({block_size})"
            )
        return data
    
    def unpad(self, data: bytes, block_size: int) -> bytes:
        return data  # Ничего не делаем


class PaddingFactory:
    """
    Фабрика для создания схем дополнения по имени.
    """
    
    _schemes: Dict[str, Type[PaddingScheme]] = {}
    
    @classmethod
    def register(cls, name: str, scheme_class: Type[PaddingScheme]) -> None:
        """Зарегистрировать схему дополнения."""
        cls._schemes[name.upper()] = scheme_class
    
    @classmethod
    def create(cls, name: str) -> PaddingScheme:
        """
        Создать экземпляр схемы дополнения.
        
        Args:
            name: Название схемы (zeros, pkcs7, iso7816, ansi_x923, none).
            
        Returns:
            Экземпляр схемы дополнения.
        """
        name_upper = name.upper()
        if name_upper not in cls._schemes:
            available = ", ".join(cls._schemes.keys())
            raise ValueError(f"Схема дополнения '{name}' не найдена. Доступные: {available}")
        return cls._schemes[name_upper]()
    
    @classmethod
    def get_available(cls) -> list:
        """Получить список доступных схем."""
        return list(cls._schemes.keys())
    
    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Проверить, зарегистрирована ли схема."""
        return name.upper() in cls._schemes


# Регистрация встроенных схем (согласно ТЗ)
PaddingFactory.register("PKCS7", PKCS7Padding)
PaddingFactory.register("PKCS5", PKCS7Padding)  # Алиас (PKCS5 = PKCS7 для блоков ≤8 байт)
PaddingFactory.register("ISO7816", ISO7816Padding)
PaddingFactory.register("ISO_7816", ISO7816Padding)  # Алиас с подчеркиванием
PaddingFactory.register("ANSI_X923", ANSIX923Padding)
PaddingFactory.register("X923", ANSIX923Padding)  # Алиас
PaddingFactory.register("ISO10126", ISO10126Padding)
PaddingFactory.register("ISO_10126", ISO10126Padding)  # Алиас с подчеркиванием
PaddingFactory.register("NONE", NonePadding)
