# IDEA Cipher - Криптографическая система

Реализация блочного шифра **IDEA** (International Data Encryption Algorithm) с поддержкой различных режимов шифрования и дополнения.

## Возможности

### Режимы шифрования

| Режим | Описание              | IV/Nonce   |
| ----- | --------------------- | ---------- |
| ECB   | Electronic Codebook   | Не требует |
| CBC   | Cipher Block Chaining | Требует    |
| PCBC  | Propagating CBC       | Требует    |
| CFB   | Cipher Feedback       | Требует    |
| OFB   | Output Feedback       | Требует    |
| CTR   | Counter               | Требует    |

### Режимы дополнения (padding)

| Режим     | Описание                                          |
| --------- | ------------------------------------------------- |
| pkcs7     | PKCS#7 - каждый байт равен количеству добавленных |
| iso7816   | ISO/IEC 7816-4 - 0x80 + нули                      |
| ansi_x923 | ANSI X9.23 - нули + последний байт = количество   |
| iso10126  | ISO 10126 - случайные байты + количество          |

## Быстрый старт

### Шифрование (режим ECB)

```bash
# Подготовка файлов
echo "Secret message" > in.bin
echo "1234567890123456" > key.bin

# Шифрование
python cli.py --encrypt --cipher IDEA --mode ECB --padding pkcs7

# Результат в out.bin
```

### Расшифрование

```bash
python cli.py --decrypt --cipher IDEA --mode ECB --padding pkcs7 --input out.bin --output decrypted.bin
```

### Шифрование с IV (режим CBC)

```bash
# Создаём IV (8 байт для IDEA)
echo "12345678" > sync.bin

# Шифрование
python cli.py -e -m CBC -p pkcs7

# Расшифрование
python cli.py -d -m CBC -p pkcs7
```

## Использование CLI

```
python cli.py [опции]
```

### Обязательные параметры

| Параметр        | Описание            |
| --------------- | ------------------- |
| `-e, --encrypt` | Зашифровать данные  |
| `-d, --decrypt` | Расшифровать данные |

### Основные параметры

| Параметр        | По умолчанию | Описание            |
| --------------- | ------------ | ------------------- |
| `-c, --cipher`  | IDEA         | Алгоритм шифрования |
| `-m, --mode`    | ECB          | Режим шифрования    |
| `-p, --padding` | pkcs7        | Режим дополнения    |

### Файлы

| Параметр       | По умолчанию | Описание                 |
| -------------- | ------------ | ------------------------ |
| `-i, --input`  | in.bin       | Входной файл             |
| `-o, --output` | out.bin      | Выходной файл            |
| `-k, --key`    | key.bin      | Файл с ключом (16 байт)  |
| `-s, --sync`   | sync.bin     | Файл с IV/nonce (8 байт) |

### Дополнительно

| Параметр        | Описание        |
| --------------- | --------------- |
| `-v, --verbose` | Подробный вывод |
| `-h, --help`    | Справка         |

## Примеры

### 1. Простое шифрование (ECB)

```bash
python cli.py -e -m ECB -p pkcs7
```

### 2. CBC с указанием файлов

```bash
python cli.py -e -m CBC -p iso7816 -i message.txt -o encrypted.bin -k mykey.bin -s iv.bin
```

### 3. Потоковый режим CTR

```bash
python cli.py -e -m CTR -i data.bin -o encrypted.bin -v
```

### 4. Все режимы с подробным выводом

```bash
# ECB (без IV)
python cli.py -e -m ECB -p pkcs7 -v

# CBC
python cli.py -e -m CBC -p pkcs7 -v

# PCBC
python cli.py -e -m PCBC -p ansi_x923 -v

# CFB (потоковый)
python cli.py -e -m CFB -v

# OFB (потоковый)
python cli.py -e -m OFB -v

# CTR (потоковый)
python cli.py -e -m CTR -v
```

## Требования к файлам

### key.bin

- **Размер**: 16 байт (128 бит)
- Если меньше — дополняется нулями
- Если больше — обрезается

### sync.bin (IV/Nonce)

- **Размер**: 8 байт (64 бита = размер блока IDEA)
- Требуется для режимов: CBC, PCBC, CFB, OFB, CTR
- Не используется для ECB

### in.bin / out.bin

- Бинарные файлы любого размера

## Особенности реализации

1. **Padding всегда добавляется** даже если данные кратны блоку (позволяет однозначно определить размер исходных данных)

2. **Потоковые режимы** (CFB, OFB, CTR) не используют padding — размер шифротекста = размер открытого текста

3. **CTR счётчик**: `counter[i] = (nonce + i) mod 2^64`

## Запуск тестов

```bash
# Все тесты (225 тестов)
pytest tests/ -v

# Тесты шифра IDEA
pytest tests/test_ciphers.py -v

# Тесты режимов шифрования (ECB, CBC, PCBC, CFB, OFB, CTR)
pytest tests/test_modes.py -v

# Тесты режимов дополнения (PKCS7, ISO7816, ANSI_X923, ISO10126)
pytest tests/test_paddings.py -v

# Интеграционные тесты (CLI, фабрики, edge cases)
pytest tests/test_integration.py -v
```

## Структура проекта

```
├── cli.py                 # Интерфейс командной строки
├── crypto/
│   ├── ciphers/
│   │   └── idea.py        # Реализация IDEA
│   ├── modes/
│   │   ├── ecb.py         # Electronic Codebook
│   │   ├── cbc.py         # Cipher Block Chaining
│   │   ├── pcbc.py        # Propagating CBC
│   │   ├── cfb.py         # Cipher Feedback
│   │   ├── ofb.py         # Output Feedback
│   │   └── ctr.py         # Counter
│   ├── padding.py         # Схемы дополнения
│   ├── crypto_system.py   # Главный класс системы
│   └── factory.py         # Фабрики шифров и режимов
└── tests/                 # 225 тестов
    ├── test_ciphers.py    # Тесты шифра IDEA (29)
    ├── test_modes.py      # Тесты режимов шифрования (65)
    ├── test_paddings.py   # Тесты дополнений (44)
    └── test_integration.py # Интеграционные тесты (87)
```

## Автор

Лабораторная работа №3 по криптографии
