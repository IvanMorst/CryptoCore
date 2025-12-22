## CryptoCore — учебный проект, реализующий полный набор криптографических операций для защиты данных. 

# Содержание

##  Быстрый старт
- [Структура проекта](#структура-проекта)
- [Зависимости](#зависимости)
- [Установка зависимостей](#установка-зависимостей)
- [Инструкции по сборке и установке](#инструкции-по-сборке-и-установке)

##  Тестирование и проверка
- [Генерация тестовых файлов](#генерация-тестовых-файлов)
- [Тестирование шифрования](#тестирование-шифрования)
- [Тестирование](#тестирование)
- [Тестирование с NIST Statistical Test Suite](#тестирование-с-nist-statistical-test-suite)
- [Проверка целостности](#проверка-целостности)

## Режимы шифрования AES
- [Режим ECB](#шифрование-и-дешифрование-в-режиме-ecb)
- [Режим CBC](#шифрование-и-дешифрование-в-режиме-cbc)
- [Режим CFB](#шифрование-и-дешифрование-в-режиме-cfb)
- [Режим OFB](#шифрование-и-дешифрование-в-режиме-ofb)
- [Режим CTR](#шифрование-и-дешифрование-в-режиме-ctr)

##  Совместимость
- [Совместимость с OpenSSL](#совместимость-с-openssl)

##  Хеш-функции
- [Хэш-функции](#хэш---функции)
- [Вычисление SHA-256](#вычисление-sha-256-хеша-файла)
- [Вычисление SHA3-256](#вычисление-sha3-256-хеша-файла)

##  HMAC
- [Что такое HMAC?](#что-такое-hmac)
- [Тестирование HMAC](#тест-hmac-функциональности)

##  AEAD (Аутентифицированное шифрование)
- [GCM режим](#аутентифицированное-шифрование-aead)
- [Тестирование GCM](#скрипт-для-проверки-gcm)

##  KDF (Функции вывода ключей)
- [Функции вывода ключей](#key-derivation-functions-kdf)
- [Команда derive](#команда-derive-для-вывода-ключей)
- [Примеры использования KDF](#примеры-использования)

##  Проверка ошибок
- [Проверка валидации аргументов](#проверка-валидации-аргументов-должны-вызвать-ошибки)
- [Проверка обработки ошибок](#проверка-обработки-ошибок)

##  Работа с файлами
- [Шифрование PDF документов](#шифрование-pdf-документа)
- [Шифрование ZIP архивов](#шифрование-zip-архива)
- [Шифрование изображений](#шифрование-изображений)
- [Дешифрование файлов](#дешифрование-файлов)

##  Управление ключами
- [Генерация тестовых ключей](#генерация-тестовых-ключей)
- [Примеры валидных ключей](#примеры-валидных-ключей-для-тестирования)

## Структура проекта
````text
CryptoCore/
├── cryptocore.py # Главный исполняемый файл CLI
├── main.py # Интерфейс 
├── setup.py # Конфигурация установки пакета
├── requirements.txt # Зависимости Python
├── pyproject.toml            # Конфигурация проекта
├── README.md                 # Основной README
├── docs/                     # Документация
│   ├── API.md               # API документация
│   ├── USERGUIDE.md         # Руководство пользователя
│   └── DEVELOPMENT.md       # Руководство разработчика
├── hash/                      # папка для хеш-функций
│   ├── __init__.py
│   ├── sha256.py              # Реализация SHA-256 
│   └── sha3_256.py            # Реализация SHA3-256
├── mac/                      # MAC
│   ├── __init__.py
│   └── hmac.py            # Реализация HMAC
├──tests/                        # Пакет тестов
│   ├── __init__.py
│   ├── test_all_cipher_modes.py      # Тесты для всех режимов шифрования
│   ├── test_sha256.py            # Тесты для реализации SHA-256
│   ├── test_sha3_256.py          # Тесты для реализации SHA3-256
│   ├── test_hmac.py          # Тесты для реализации HMAC
│   ├── test_pbkdf2.py            # Тесты для PBKDF2
│   ├── test_gcm.py           # Тесты для GSM
│   ├── test_key_hierarchy.py     # Тесты для иерархии ключей
│   └── test_csprng.py            # Тесты для CSPRNG модуля
└── crypto/ # Пакет с ядром криптосистемы
    ├── init.py
    ├── cipher_core.py # AES шифрование/дешифрование
    ├── crypto_core.py # Интеграция кастомного генератора
    ├── crypto_exception.py # Обработка исключений
    ├── crypto_logger.py # Система логирования
    ├── file_processor.py # Обработка файлов
    ├── generator.py # Генератор случайных данных
    ├── key_generator.py # Кастомный генератор ключей
    ├── kdf/                          #  Новый модуль
    │   ├── __init__.py
    │   ├── pbkdf2.py                 # Реализация PBKDF2-HMAC-SHA256
    │   └── key_hierarchy.py          # Функция иерархии ключей
    ├── aead/   # Новый модуль для AEAD
    │    ├── __init__.py
    │    ├── encrypt_then_mac.py  # Encrypt-then-MAC реализация
    │    └──  gcm.py  # GCM реализация
    └── modes # Директория с режимами шифрования
        ├── init.py
        ├── base_mode.py # Базовый класс режимов
        ├── gcm_mode.py  # Адаптер GCM для CLI
        ├── cbc_mode.py # Режим CBC
        ├── cfb_mode.py # Режим CFB
        ├── ofb_mode.py # Режим OFB
        └── ctr_mode.py # Режим CTR
    
````
## Зависимости
### Обязательные зависимости

#### Python 3.7+

#### pycryptodome>=3.20.0 - криптографические алгоритмы

#### psutil>=5.8.0 - системная информация для генерации энтропии

### pytest==8.4.2

## Установка зависимостей
```bash

pip install -r requirements.txt
````
## Инструкции по сборке и установке


## Клонирование репозитория

```bash
git clone https://github.com/IvanMorst/CryptoCore.git
```
```bash
cd CryptoCore
````

## Создаем виртуальное окружение в папке проекта

```bash

python3 -m .venv venv
````

### Активируем виртуальное окружение

```bash

source .venv/bin/activate
```


### Установка зависимостей

```bash

pip install -r requirements.txt
````


### Справка

```bash

python cryptocore.py --help
````


## Генерация тестовых файлов

### Создание простого текстового файла
```bash

echo "This is a test file for CryptoCore encryption" > plaintext.txt
````

### Создание бинарного тестового файла

```bash

python -c "import os; open('test_binary.bin', 'wb').write(os.urandom(1024))"
````

## Тестирование шифрования

### Шифрование с явным указанием выходного файла
```bash

python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input document.txt --output document.enc
```

### Шифрование с автоматическим именем выходного файла

```bash

python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input data.csv
```


### Шифрование с автоматической генерацией ключа

```bash

python cryptocore.py --algorithm aes --mode ctr --encrypt --input plaintext.txt --output ciphertext.bin
```

### Шифрование с явным ключом

```bash

python cryptocore.py --algorithm aes --mode cbc --encrypt --key 00112233445566778899aabbccddeeff --input document.pdf --output document.pdf.enc
````
### Дешифрование (ключ обязателен)

```bash

python cryptocore.py --algorithm aes --mode cbc --decrypt --key 00112233445566778899aabbccddeeff --input document.pdf.enc --output document_decrypted.pdf
```

### Генерация тестового ключа

```bash

python -c "from csprng import generate_key; print('Random key:', generate_key(16).hex())"
```

## Тестирование

### Запуск всех тестов через Pytest

```bash
pytest tests/ -v
```
### Тестирование функции иерархии ключей

```bash

python tests/test_key_hierarchy.py
````
### Тестирование производительности различных алгоритмов

```bash

python tests/performance_comparison.py
````
### Комплексное тестирование GCM (Galois/Counter Mode) 

```bash

python tests/test_gcm.py
````
### Тестирование HMAC-SHA256 реализации

```bash

python tests/test_hmac.py
````
### Тестирование PBKDF2-HMAC-SHA256

```bash

python tests/test_pbkdf2.py
````
### Тестирование SHA3-256 хеш-функции

```bash

python tests/test_sha3_256.py
````
### Тестирование SHA-256 хеш-функции 

```bash

python tests/test_sha256.py
````
### Комплексное тестирование всех режимов шифрования
### Проверяет все поддерживаемые режимы AES: ECB, CBC, CTR, CFB, OFB, GCM,
### включая производительность, безопасность и обработку ошибок

```bash

python tests/test_all_cipher_modes.py
````



## Тестирование с NIST Statistical Test Suite

### 1. Установка NIST STS

### Скачайте с официального сайта NIST

```bash
wget https://csrc.nist.gov/CSRC/media/Projects/Random-Bit-Generation/documents/sts-2_1_2.zip
````
```bash
unzip sts-2_1_2.zip
````
```bash
cd sts-2_1_2
````
```bash
make
````
### 2. Генерация тестовых данных

```bash
python tests/test_csprng.py
```
### 3. Запуск тестов NIST

```bash
./assess 10000000
```

### Следуйте инструкциям для указания файла nist_test_data.bin
#### адрес файла
#### /home/morst/PycharmProjects/CryptoCore_3/tests/nist_test_data.bin
## Шифрование PDF документа

```bash

python cryptocore.py --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input document.pdf --output document.pdf.enc
````
## Дешифрование PDF документа

```bash 

python cryptocore.py --algorithmsource .venv/bin/activate aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input document.pdf.enc --output document_restored.pdf
````
## Шифрование ZIP архива

```bash
python cryptocore.py --algorithm aes --mode ecb --encrypt --key aabbccddeeff00112233445566778899 --input archive.zip
````

## Шифрование изображений
```bash
# Шифрование JPEG изображения
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 11223344556677889900aabbccddeeff --input image.jpg --output image.jpg.enc

# Шифрование PNG изображения
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 223344556677889900aabbccddeeff11 --input photo.png
````
Дешифрование файлов
Дешифрование текстовых файлов
```bash
# Дешифрование с явным указанием выходного файла
python cryptocore.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input document.enc --output document_decrypted.txt

# Дешифрование с автоматическим именем выходного файла
python cryptocore.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input data.csv.enc
# Создается файл: data.csv.enc.dec
Дешифрование бинарных файлов
bash

# Дешифрование архива
python cryptocore.py --algorithm aes --mode ecb --decrypt --key aabbccddeeff00112233445566778899 --input archive.zip.enc
````
##Генерация тестовых ключей

##Генерация ключей AES

# AES-128 (16 байт, 32 hex символа)
```bash
python -c "import os; print('AES-128 key:', os.urandom(16).hex())"
```

## Примеры валидных ключей для тестирования

### AES-128 ключи
00112233445566778899aabbccddeeff
000102030405060708090a0b0c0d0e0f
a0a1a2a3a4a5a6a7a8a9aaabacadaeaf







### Создание тестового файла

```bash

echo "Test data for encryption verification" > test_original.txt
```

# 4. Проверка целостности

```bash

python -c "print('Files are identical' if open('test_original.txt', 'rb').read() == open('test_decrypted.txt', 'rb').read() else 'Files are different')"
```

# 5. Проверка хешей

### certutil -hashfile test_original.txt SHA256  # Windows

### sha256sum test_original.txt test_decrypted.txt  # Linux/Mac



## Проверка валидации аргументов (должны вызвать ошибки)
### Неверный алгоритм

```bash

python cryptocore.py --algorithm des --mode ecb --encrypt --key 001122 --input test.txt
```
### Неверный режим

```bash

python cryptocore.py --algorithm aes --mode cbc --encrypt --key 001122 --input test.txt 
```
### Отсутствует операция

```bash

python cryptocore.py --algorithm aes --mode ecb --key 001122 --input test.txt 
```
### Конфликт операций

```bash

python cryptocore.py --algorithm aes --mode ecb --encrypt --decrypt --key 001122 --input test.txt
```
### Неверный ключ

```bash

python cryptocore.py --algorithm aes --mode ecb --encrypt --key invalid_key --input test.txt
```


## Проверка обработки ошибок

### Несуществующий входной файл

```bash
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input nonexistent.txt --output test.enc
```
### Неверная длина ключа

```bash
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 001122 --input test.txt --output test.enc
```
### Неhex-символы в ключе

```bash
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeefg --input test.txt --output test.enc
```


## Шифрование и дешифрование в режиме ECB

### Шифрование файла в режиме

```bash

python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output document_encrypted.bin
````
### Дешифрование файла в режиме

```bash

python cryptocore.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input document_encrypted.bin --output document_decrypted.pdf
````


## Шифрование и дешифрование в режиме CBC


### Шифрование файла в режиме CBC (IV генерируется автоматически)

```bash

python cryptocore.py --algorithm aes --mode cbc --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output document.pdf.cbc.enc
````
### Дешифрование файла (IV читается из файла автоматически)

```bash

python cryptocore.py --algorithm aes --mode cbc --decrypt --key 00112233445566778899aabbccddeeff --input document.pdf.cbc.enc --output document_decrypted.pdf
````
### Дешифрование с явным указанием IV

```bash

python cryptocore.py --algorithm aes --mode cbc --decrypt --key 00112233445566778899aabbccddeeff --iv AABBCCDDEEFF00112233445566778899 --input document.pdf.cbc.enc --output document_decrypted.pdf
```


## Шифрование и дешифрование в режиме CFB

### Шифрование файла в режиме CFB

```bash

python cryptocore.py --algorithm aes --mode cfb --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output document_encrypted.pdf.cfb.enc
```

### Дешифрование файла в режиме CFB

```bash

python cryptocore.py --algorithm aes --mode cfb --decrypt --key 00112233445566778899aabbccddeeff --input document_encrypted.pdf.cfb.enc --output document_encrypted.pdf
```


## Шифрование и дешифрование в режиме OFB

### Шифрование файла в режиме OFB

```bash

python cryptocore.py --algorithm aes --mode ofb --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output data.bin.ofb.enc
````
### Дешифрование файла в режиме OFB

```bash

python cryptocore.py --algorithm aes --mode ofb --decrypt --key 00112233445566778899aabbccddeeff --input data.bin.ofb.enc --output data_restored.bin
```


## Шифрование и дешифрование в режиме CTR

### Шифрование файла в режиме CTR

```bash

python cryptocore.py --algorithm aes --mode ctr --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output archive.zip.ctr.enc
````
### Дешифрование файла в режиме CTR

```bash

python cryptocore.py --algorithm aes --mode ctr --decrypt --key 00112233445566778899aabbccddeeff --input archive.zip.ctr.enc --output archive_restored.zip
```


## Совместимость с OpenSSL

### Шифрование CryptoCore - дешифрование OpenSSL

```bash

# 1. Шифрование CBC нашим инструментом
python cryptocore.py --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.bin --output cryptocore_cipher.bin

# 2. Извлечение IV и шифртекста
dd if=cryptocore_cipher.bin of=iv.bin bs=16 count=1
dd if=cryptocore_cipher.bin of=ciphertext_only.bin bs=16 skip=1

# 3. Дешифрование OpenSSL
openssl enc -aes-128-cbc -d -K 000102030405060708090a0b0c0d0e0f -iv $(xxd -p iv.bin | tr -d '\n') -in ciphertext_only.bin -out openssl_decrypted.bin

cmp plaintext.bin openssl_decrypted.bin && echo "✓ Files are identical" || echo "✗ Files differ"

```
### Шифрование OpenSSL - дешифрование CryptoCore
```bash

# 1. Шифрование CBC OpenSSL


openssl enc -aes-128-cbc -K 000102030405060708090a0b0c0d0e0f -iv 00112233445566778899aabbccddeeff -in plaintext.bin -out openssl_cipher.bin

# 2. Дешифрование нашим инструментом с явным IV
python cryptocore.py --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv 00112233445566778899aabbccddeeff --input openssl_cipher.bin --output cryptocore_decrypted.bin

cmp plaintext.bin cryptocore_decrypted.bin && echo "✓ Files are identical" || echo "✗ Files differ"
```



## Хэш - функции

### Вычисление SHA-256 хеша файла
```bash

python cryptocore.py dgst --algorithm sha256 --input document.pdf
```
### Вычисление SHA3-256 хеша файла

```bash

python cryptocore.py dgst --algorithm sha3-256 --input backup.tar
```
### Сохранение хеша в файл

```bash

python cryptocore.py dgst --algorithm sha256 --input file.txt --output file.sha256
```
### Хеширование с выводом только хеш-значения (для скриптов)

```bash

python cryptocore.py dgst --algorithm sha256 --input data.bin | cut -d' ' -f1
```

### Проверка известных тестовых векторов
```bash

echo -n "abc" | python -c "
import sys
from hash.sha256 import sha256
from hash.sha3_256 import sha3_256
data = sys.stdin.buffer.read()
print('SHA256:', sha256(data))
print('SHA3-256:', sha3_256(data))
"
echo "test" > plaintext.txt
python cryptocore.py dgst --algorithm sha256 --input plaintext.txt
sha256sum plaintext.txt  
```

### Тестирование

```bash
python tests/performance_comparison.py
```
### Help

```bash

python cryptocore.py dgst --help
```


## HMAC

###  Что такое HMAC?

**HMAC (Hash-based Message Authentication Code)** - это механизм для проверки 
аутентичности и целостности сообщений с использованием криптографических хеш-функций 
и секретного ключа. Реализация соответствует **RFC 2104** и использует SHA-256 в 
качестве базовой хеш-функции.

### Базовый синтаксис:
```bash

# Для HMAC операций используется подкоманда dgst с флагом --hmac
cryptocore dgst --algorithm sha256 --hmac --key <HEX_KEY> --input <FILE> [опции]
```
### ТЕСТ HMAC ФУНКЦИОНАЛЬНОСТИ

```bash
#!/bin/bash
echo " КОМПЛЕКСНЫЙ ТЕСТ HMAC ФУНКЦИОНАЛЬНОСТИ"
echo "=========================================="

# 1. Создание тестовых файлов
echo "1. Создание тестовых файлов..."
echo "Тестовый документ 1" > doc1.tmp
echo "Тестовый документ 2" > doc2.tmp
python3 -c "import os; open('binary.tmp', 'wb').write(os.urandom(1024))"

# 2. Генерация HMAC
echo -e "\n2. Генерация HMAC для файлов..."
KEY="746573745f6b65795f31323334353637383930616263646566"  # hex версия "test_key_1234567890abcdef"
python cryptocore.py dgst --algorithm sha256 --hmac --key $KEY --input doc1.tmp > doc1.hmac
python cryptocore.py dgst --algorithm sha256 --hmac --key $KEY --input doc2.tmp > doc2.hmac
python cryptocore.py dgst --algorithm sha256 --hmac --key $KEY --input binary.tmp > binary.hmac

# 3. Верификация
echo -e "\n3. Верификация HMAC..."
python cryptocore.py dgst --algorithm sha256 --hmac --key $KEY --input doc1.tmp --verify doc1.hmac && echo "  ✅ doc1.tmp: OK"
python cryptocore.py dgst --algorithm sha256 --hmac --key $KEY --input doc2.tmp --verify doc2.hmac && echo "  ✅ doc2.tmp: OK"
python cryptocore.py dgst --algorithm sha256 --hmac --key $KEY --input binary.tmp --verify binary.hmac && echo "  ✅ binary.tmp: OK"

# 4. Тест обнаружения изменений
echo -e "\n4. Тест обнаружения изменений..."
echo "Измененное содержимое" > doc1.tmp
python cryptocore.py dgst --algorithm sha256 --hmac --key $KEY --input doc1.tmp --verify doc1.hmac || echo "  ✅ Обнаружено изменение doc1.tmp"

# 5. Очистка
echo -e "\n5. Очистка тестовых файлов..."
rm -f *.tmp *.hmac
echo "✅ Тестирование завершено"
```


## Аутентифицированное Шифрование (AEAD)

1. **GCM (Galois/Counter Mode)** - Аутентифицированный режим шифрования AES
2. **Encrypt-then-MAC** - Композитный подход (шифрование + HMAC)

**AEAD (Authenticated Encryption with Associated Data)** - это криптографический примитив, который одновременно обеспечивает:
- **Конфиденциальность** - данные зашифрованы
- **Целостность** - данные не были изменены
- **Аутентичность** - данные созданы отправителем с секретным ключом
- **Аутентичность дополнительных данных** - метаданные также защищены

#### Базовый синтаксис GCM:
```bash
# Шифрование с AAD
python cryptocore.py encrypt --algorithm aes --mode gcm --encrypt \
  --key 00112233445566778899aabbccddeeff \
  --input plaintext.txt --output ciphertext.bin \
  --aad aabbccddeeff
```

```bash
# Дешифрование с AAD
python cryptocore.py encrypt --algorithm aes --mode gcm --decrypt \
  --key 00112233445566778899aabbccddeeff \
  --input ciphertext.bin --output decrypted.txt \
  --aad aabbccddeeff
```


python -m unittest discover tests -v


### Комплексное тестирование GSM

```bash

python -m unittest tests.test_gcm.TestGCM -v
```

### Cкрипт для проверки GCM

```bash
#!/bin/bash
echo "ТЕСТИРОВАНИЕ GCM РЕАЛИЗАЦИИ"
echo "==============================="

# 1. Создаем тестовые файлы
echo "1. Создание тестовых файлов..."
echo "Тестовые данные" > test_input.txt
echo "Аутентификационные данные" > aad_content.txt

# 2. Конвертируем AAD в hex
AAD_HEX=$(python -c "with open('aad_content.txt', 'rb') as f: print(f.read().hex())")

# 3. Шифрование
echo -e "\n2. Шифрование GCM..."
python cryptocore.py encrypt --algorithm aes --mode gcm --encrypt \
  --key 00112233445566778899aabbccddeeff \
  --input test_input.txt --output encrypted.gcm \
  --aad $AAD_HEX

# 4. Дешифрование
echo -e "\n3. Дешифрование GCM..."
python cryptocore.py encrypt --algorithm aes --mode gcm --decrypt \
  --key 00112233445566778899aabbccddeeff \
  --input encrypted.gcm --output decrypted.txt \
  --aad $AAD_HEX

# 5. Проверка
echo -e "\n4. Проверка целостности..."
if diff test_input.txt decrypted.txt > /dev/null; then
    echo "✅ GCM работает корректно"
else
    echo "❌ Ошибка: файлы отличаются"
fi

# 6. Проверка ошибок аутентификации
echo -e "\n5. Тест ошибок аутентификации..."
WRONG_AAD="00000000000000000000000000000000"
python cryptocore.py encrypt --algorithm aes --mode gcm --decrypt \
  --key 00112233445566778899aabbccddeeff \
  --input encrypted.gcm --output should_fail.txt \
  --aad $WRONG_AAD 2>/dev/null || echo "✅ Аутентификация провалена (ожидаемо)"

# 7. Очистка
echo -e "\n6. Очистка..."
rm -f test_input.txt aad_content.txt encrypted.gcm decrypted.txt should_fail.txt 2>/dev/null
echo "✅ Тестирование завершено"
```


##  Key Derivation Functions (KDF)

### Реализация функций для безопасного вывода ключей из паролей и создания иерархии ключей.

### Новые возможности

#### 1. Команда `derive` для вывода ключей

### Базовый вывод ключа с указанной солью
```bash

python cryptocore.py derive --password "MySecurePassword123!" \
  --salt a1b2c3d4e5f601234567890123456789 \
  --iterations 1000 \
  --length 32
```

### Вывод ключа с автоматической генерацией соли
```bash

python cryptocore.py derive --password "AnotherPassword" \
  --iterations 5000 \
  --length 16
````

### Вывод ключа и сохранение в файл
```bash

python cryptocore.py derive --password "app_key" \
  --output derived_key.bin
  ```
### Поддерживаемые алгоритмы
```
PBKDF2-HMAC-SHA256 - RFC 2898 совместимая реализация

Key Hierarchy Function - детерминированный вывод ключей из мастер-ключа
```
### Параметры команды derive
```
Параметр	Описание	По умолчанию
--password	Пароль для вывода ключа	Обязательный
--salt	Соль в hex-формате	Автогенерация (16 байт)
--iterations	Количество итераций	100000
--length	Длина ключа в байтах	32
--algorithm	Алгоритм KDF	pbkdf2
--output	Файл для сохранения ключа	Необязательный
```

### Тестирование
Тестовые векторы RFC 6070

### Запуск тестов PBKDF2
```bash

python tests/test_pbkdf2.py
```
### Запуск тестов иерархии ключей
```bash
python tests/test_key_hierarchy.py
```


### Интероперабельность с OpenSSL
```bash
python cryptocore.py derive --password "test" \
  --salt 1234567890abcdef \
  --iterations 1000 \
  --length 32
```

### Совместимость c OpenSSL
```bash
# Сравнение с OpenSSL
python cryptocore.py derive --password "test" \
  --salt 1234567890abcdef \
  --iterations 1000 \
  --length 32 > my_key.txt

openssl kdf -keylen 32 \
  -kdfopt pass:test \
  -kdfopt salt:1234567890abcdef \
  -kdfopt iter:1000 \
  PBKDF2 > openssl_key.txt

diff my_key.txt openssl_key.txt

```

### Примеры использования
Пример 1: Защищенный вывод ключа приложения
```bash
# Генерация мастер-ключа приложения
python cryptocore.py derive \
  --password "$(cat /etc/machine-id)-$(date +%s)" \
  --iterations 500 \
  --length 64 \
  --output app_master.key
  ```


