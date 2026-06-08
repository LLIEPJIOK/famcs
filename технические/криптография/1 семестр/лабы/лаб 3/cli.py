"""
Интерфейс командной строки для криптографической системы.

Входные данные:
- in.bin: открытый текст / шифротекст
- key.bin: ключ шифрования
- sync.bin: синхропосылка (IV) для режимов CBC, CFB, OFB, CTR

Выходные данные:
- out.bin: шифротекст / открытый текст

Использование:
    python cli.py --encrypt --cipher IDEA --mode ECB
    python cli.py --decrypt --cipher IDEA --mode CBC
    python cli.py -e -c IDEA -m CTR --input data.bin --output result.bin
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from crypto import CryptoSystem, CipherFactory, ModeFactory
from crypto.crypto_system import MODES_REQUIRING_IV


def read_file(filepath: Path) -> bytes:
    """Прочитать бинарный файл."""
    if not filepath.exists():
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    return filepath.read_bytes()


def write_file(filepath: Path, data: bytes) -> None:
    """Записать бинарный файл."""
    filepath.write_bytes(data)


def get_cipher_key_size(cipher_name: str) -> int:
    """Получить требуемый размер ключа для шифра."""
    key_sizes = {
        "IDEA": 16,  # 128 бит
    }
    return key_sizes.get(cipher_name.upper(), 16)


def validate_key(key: bytes, cipher_name: str) -> bytes:
    """
    Валидация и подготовка ключа.
    
    Если ключ короче требуемого — дополняется нулями.
    Если длиннее — обрезается.
    """
    required_size = get_cipher_key_size(cipher_name)
    
    if len(key) < required_size:
        print(f"⚠️  Ключ ({len(key)} байт) короче требуемого ({required_size} байт), дополнен нулями")
        key = key + bytes(required_size - len(key))
    elif len(key) > required_size:
        print(f"⚠️  Ключ ({len(key)} байт) длиннее требуемого ({required_size} байт), обрезан")
        key = key[:required_size]
    
    return key


def get_block_size(cipher_name: str) -> int:
    """Получить размер блока для шифра (= размер IV)."""
    block_sizes = {
        "IDEA": 8,  # 64 бит
    }
    return block_sizes.get(cipher_name.upper(), 8)


def validate_iv(iv: bytes, cipher_name: str, mode_name: str) -> bytes:
    """
    Валидация и подготовка IV (синхропосылки).
    
    Если IV короче требуемого — дополняется нулями.
    Если длиннее — обрезается.
    """
    required_size = get_block_size(cipher_name)
    
    if len(iv) < required_size:
        print(f"⚠️  IV ({len(iv)} байт) короче требуемого ({required_size} байт), дополнен нулями")
        iv = iv + bytes(required_size - len(iv))
    elif len(iv) > required_size:
        print(f"⚠️  IV ({len(iv)} байт) длиннее требуемого ({required_size} байт), обрезан")
        iv = iv[:required_size]
    
    return iv


def create_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Криптографическая система IDEA с различными режимами шифрования",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s --encrypt --cipher IDEA --mode ECB
  %(prog)s --decrypt --cipher IDEA --mode CBC
  %(prog)s -e -c IDEA -m CTR --input data.bin --output result.bin
  %(prog)s -d -c IDEA -m OFB --key mykey.bin --sync iv.bin

Режимы шифрования:
  ECB  - Electronic Codebook (не требует IV, НЕ рекомендуется)
  CBC  - Cipher Block Chaining (требует IV)
  PCBC - Propagating CBC (требует IV, ошибка распространяется)
  CFB  - Cipher Feedback (требует IV, потоковый)
  OFB  - Output Feedback (требует IV, потоковый)
  CTR  - Counter (требует nonce, потоковый, параллелизуемый)

Режимы дополнения (padding):
  pkcs7     - PKCS#7 (каждый байт = количество добавленных)
  iso7816   - ISO/IEC 7816-4 (0x80 + нули)
  ansi_x923 - ANSI X9.23 (нули + последний байт = количество)
  iso10126  - ISO 10126 (случайные байты + последний байт = количество)
  none      - Без дополнения (данные должны быть кратны блоку)

Доступные шифры: """ + ", ".join(CipherFactory.get_available()) + """
Доступные режимы: """ + ", ".join(ModeFactory.get_available())
    )
    
    # Режим работы (шифрование/расшифрование)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "-e", "--encrypt",
        action="store_true",
        help="Зашифровать данные"
    )
    mode_group.add_argument(
        "-d", "--decrypt",
        action="store_true",
        help="Расшифровать данные"
    )
    
    # Параметры шифрования
    parser.add_argument(
        "-c", "--cipher",
        type=str,
        default="IDEA",
        choices=[c.lower() for c in CipherFactory.get_available()] + CipherFactory.get_available(),
        help="Алгоритм шифрования (по умолчанию: IDEA)"
    )
    parser.add_argument(
        "-m", "--mode",
        type=str,
        default="ECB",
        choices=[m.lower() for m in ModeFactory.get_available()] + ModeFactory.get_available(),
        help="Режим шифрования (по умолчанию: ECB)"
    )
    parser.add_argument(
        "-p", "--padding",
        type=str,
        default="pkcs7",
        choices=["pkcs7", "iso7816", "ansi_x923", "iso10126", "none"],
        help="Режим дополнения (по умолчанию: pkcs7)"
    )
    
    # Файлы
    parser.add_argument(
        "-i", "--input",
        type=Path,
        default=Path("in.bin"),
        help="Входной файл (по умолчанию: in.bin)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("out.bin"),
        help="Выходной файл (по умолчанию: out.bin)"
    )
    parser.add_argument(
        "-k", "--key",
        type=Path,
        default=Path("key.bin"),
        help="Файл с ключом (по умолчанию: key.bin)"
    )
    parser.add_argument(
        "-s", "--sync",
        type=Path,
        default=Path("sync.bin"),
        help="Файл с синхропосылкой/IV (по умолчанию: sync.bin)"
    )
    
    # Дополнительные опции
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Подробный вывод"
    )
    
    return parser


def main() -> int:
    """Главная функция CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Чтение входных данных
        if args.verbose:
            print(f"📂 Чтение входного файла: {args.input}")
        input_data = read_file(args.input)
        
        if args.verbose:
            print(f"   Размер: {len(input_data)} байт")
        
        # Чтение ключа
        if args.verbose:
            print(f"🔑 Чтение ключа: {args.key}")
        key = read_file(args.key)
        key = validate_key(key, args.cipher)
        
        # Чтение синхропосылки (IV/nonce для режимов CBC, CFB, OFB, CTR)
        iv: Optional[bytes] = None
        mode_upper = args.mode.upper()
        
        if mode_upper in MODES_REQUIRING_IV:
            if args.sync.exists():
                if args.verbose:
                    print(f"🔄 Чтение синхропосылки (IV): {args.sync}")
                iv = read_file(args.sync)
                iv = validate_iv(iv, args.cipher, args.mode)
            else:
                raise FileNotFoundError(
                    f"Режим {mode_upper} требует синхропосылку (IV), "
                    f"но файл {args.sync} не найден"
                )
        elif args.sync.exists():
            if args.verbose:
                print(f"ℹ️  Режим {mode_upper} не использует синхропосылку, файл {args.sync} игнорируется")
        
        # Создание криптосистемы
        if args.verbose:
            print(f"\n⚙️  Настройка: {args.cipher.upper()}-{args.mode.upper()}")
            print(f"   Режим дополнения: {args.padding}")
            if iv:
                print(f"   IV: {iv.hex()}")
        
        crypto = CryptoSystem.create(args.cipher, args.mode, key, iv=iv, padding=args.padding)
        
        # Выполнение операции
        if args.encrypt:
            if args.verbose:
                print(f"\n🔒 Шифрование...")
            output_data = crypto.encrypt(input_data)
            operation = "Зашифровано"
        else:
            if args.verbose:
                print(f"\n🔓 Расшифрование...")
            output_data = crypto.decrypt(input_data)
            operation = "Расшифровано"
        
        # Запись результата
        if args.verbose:
            print(f"\n💾 Запись в файл: {args.output}")
            print(f"   Размер: {len(output_data)} байт")
        
        write_file(args.output, output_data)
        
        print(f"✅ {operation} успешно: {args.input} → {args.output}")
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"❌ Ошибка параметров: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
