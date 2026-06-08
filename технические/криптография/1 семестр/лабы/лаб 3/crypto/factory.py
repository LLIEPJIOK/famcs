"""
Фабрики для создания шифров и режимов шифрования (паттерн Factory).

Позволяют создавать объекты шифров и режимов по их имени,
что упрощает расширение системы новыми алгоритмами.
"""

from typing import Dict, Type, Optional
from crypto.interfaces import BlockCipher, CipherMode
from crypto.ciphers.idea import IDEACipher
from crypto.modes.ecb import ECBMode
from crypto.modes.cbc import CBCMode
from crypto.modes.pcbc import PCBCMode
from crypto.modes.cfb import CFBMode
from crypto.modes.ofb import OFBMode
from crypto.modes.ctr import CTRMode


class CipherFactory:
    """
    Фабрика блочных шифров.
    
    Позволяет регистрировать новые шифры и создавать их по имени.
    Упрощает добавление новых криптосистем (DES, AES и т.д.).
    """
    
    _ciphers: Dict[str, Type[BlockCipher]] = {}
    
    @classmethod
    def register(cls, name: str, cipher_class: Type[BlockCipher]) -> None:
        """
        Зарегистрировать новый класс шифра.
        
        Args:
            name: Уникальное имя шифра (например, "IDEA", "AES").
            cipher_class: Класс шифра, реализующий BlockCipher.
        """
        cls._ciphers[name.upper()] = cipher_class
    
    @classmethod
    def create(cls, name: str, key: bytes) -> BlockCipher:
        """
        Создать экземпляр шифра по имени.
        
        Args:
            name: Имя шифра.
            key: Ключ шифрования.
            
        Returns:
            Экземпляр шифра.
            
        Raises:
            ValueError: Если шифр с таким именем не зарегистрирован.
        """
        name_upper = name.upper()
        if name_upper not in cls._ciphers:
            available = ", ".join(cls._ciphers.keys()) or "нет зарегистрированных"
            raise ValueError(
                f"Шифр '{name}' не найден. Доступные: {available}"
            )
        return cls._ciphers[name_upper](key)
    
    @classmethod
    def get_available(cls) -> list:
        """Получить список доступных шифров."""
        return list(cls._ciphers.keys())
    
    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Проверить, зарегистрирован ли шифр."""
        return name.upper() in cls._ciphers


class ModeFactory:
    """
    Фабрика режимов шифрования.
    
    Позволяет регистрировать новые режимы и создавать их по имени.
    Упрощает добавление новых режимов (CBC, CTR и т.д.).
    """
    
    _modes: Dict[str, Type[CipherMode]] = {}
    
    @classmethod
    def register(cls, name: str, mode_class: Type[CipherMode]) -> None:
        """
        Зарегистрировать новый класс режима.
        
        Args:
            name: Уникальное имя режима (например, "ECB", "CBC").
            mode_class: Класс режима, реализующий CipherMode.
        """
        cls._modes[name.upper()] = mode_class
    
    @classmethod
    def create(cls, name: str, **kwargs) -> CipherMode:
        """
        Создать экземпляр режима по имени.
        
        Args:
            name: Имя режима.
            **kwargs: Дополнительные параметры для режима (например, IV для CBC).
            
        Returns:
            Экземпляр режима.
            
        Raises:
            ValueError: Если режим с таким именем не зарегистрирован.
        """
        name_upper = name.upper()
        if name_upper not in cls._modes:
            available = ", ".join(cls._modes.keys()) or "нет зарегистрированных"
            raise ValueError(
                f"Режим '{name}' не найден. Доступные: {available}"
            )
        return cls._modes[name_upper](**kwargs)
    
    @classmethod
    def get_available(cls) -> list:
        """Получить список доступных режимов."""
        return list(cls._modes.keys())
    
    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Проверить, зарегистрирован ли режим."""
        return name.upper() in cls._modes


# Регистрация встроенных шифров и режимов
CipherFactory.register("IDEA", IDEACipher)
ModeFactory.register("ECB", ECBMode)
ModeFactory.register("CBC", CBCMode)
ModeFactory.register("PCBC", PCBCMode)
ModeFactory.register("CFB", CFBMode)
ModeFactory.register("OFB", OFBMode)
ModeFactory.register("CTR", CTRMode)
