CryptoCore - Криптографическая система для шифрования и дешифрования файлов с использованием AES-256 в режиме ECB.

Структура проекта
````text
CryptoCore/
├── cryptocore.py              # Главный исполняемый файл CLI
├── main.py                    # Устаревший интерфейс (для обратной совместимости)
├── setup.py                   # Конфигурация установки пакета
├── requirements.txt           # Зависимости Python
├── README.md                  # Документация
└── crypto/                    # Пакет с ядром криптосистемы
    ├── __init__.py
    ├── cipher_core.py         # AES шифрование/дешифрование
    ├── crypto_core.py         # Интеграция кастомного генератора
    ├── crypto_exception.py    # Обработка исключений
    ├── crypto_logger.py       # Система логирования
    ├── file_processor.py      # Обработка файлов
    ├── generator.py           # Генератор случайных данных
    └── key_generator.py       # Кастомный генератор ключей
````
Зависимости
Обязательные зависимости
Python 3.7+

pycryptodome>=3.20.0 - криптографические алгоритмы

psutil>=5.8.0 - системная информация для генерации энтропии

Установка зависимостей
```bash

pip install -r requirements.txt
````
Инструкции по сборке и установке
Способ 1: Запуск напрямую 
bash
## Клонирование репозитория
git clone <repository-url>
cd CryptoCore

## Перезапись удалённой версии на локальную
git push --force-with-lease origin master

## Создание виртуального окружения (опционально)
python -m venv .venv
.venv\Scripts\activate  # Windows
## source .venv/bin/activate  # Linux/Mac

## Установка зависимостей
pip install -r requirements.txt

## Проверка установки
python cryptocore.py --help
Способ 2: Установка как пакета
bash
## Установка в режиме разработки
pip install -e .

## Проверка установки
cryptocore --help
Инструкции по использованию

## Базовый синтаксис команды
bash
python cryptocore.py --algorithm aes --mode ecb --encrypt/--decrypt --key <hex_key> --input <input_file> [--output <output_file>]
Генерация тестовых файлов
Создание текстового тестового файла
bash
## Создание простого текстового файла
echo "This is a test file for CryptoCore encryption" > test_document.txt

## Создание бинарного тестового файла
python -c "import os; open('test_binary.bin', 'wb').write(os.urandom(1024))"


## Шифрование с явным указанием выходного файла
```bash

python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input document.txt --output document.enc
```

# Шифрование с автоматическим именем выходного файла

```bash
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input data.csv
```

## Шифрование PDF документа

```bash
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input document.pdf --output document.pdf.enc
````
# Шифрование ZIP архива
python cryptocore.py --algorithm aes --mode ecb --encrypt --key aabbccddeeff00112233445566778899 --input archive.zip
Шифрование изображений
bash
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
# Дешифрование PDF документа
python cryptocore.py --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input document.pdf.enc --output document_restored.pdf

# Дешифрование архива
python cryptocore.py --algorithm aes --mode ecb --decrypt --key aabbccddeeff00112233445566778899 --input archive.zip.enc
````
Генерация тестовых ключей
Генерация ключей AES
```bash
# AES-128 (16 байт, 32 hex символа)
python -c "import os; print('AES-128 key:', os.urandom(16).hex())"

# AES-192 (24 байта, 48 hex символов)
python -c "import os; print('AES-192 key:', os.urandom(24).hex())"

# AES-256 (32 байта, 64 hex символа)
python -c "import os; print('AES-256 key:', os.urandom(32).hex())"
Примеры валидных ключей для тестирования
bash
# AES-128 ключи
00112233445566778899aabbccddeeff
000102030405060708090a0b0c0d0e0f
a0a1a2a3a4a5a6a7a8a9aaabacadaeaf

# AES-256 ключи
000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff
````
Тестирование и проверка целостности
# Полный цикл тестирования



# 1. Создание тестового файла
```bash

echo "Test data for encryption verification" > test_original.txt
```
# 2. Шифрование
```bash
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input test_original.txt --output test_encrypted.bin
````
# 3. Дешифрование
```bash
python cryptocore.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input test_encrypted.bin --output test_decrypted.txt
````
# 4. Проверка целостности
fc /B test_original.txt test_decrypted.txt  # Windows
# cmp test_original.txt test_decrypted.txt  # Linux/Mac
```
```bash
python -c "print('Files are identical' if open('test_original.txt', 'rb').read() == open('test_decrypted.txt', 'rb').read() else 'Files are different')"
```
# 5. Проверка хешей

### certutil -hashfile test_original.txt SHA256  # Windows
### sha256sum test_original.txt test_decrypted.txt  # Linux/Mac

Тестирование с разными размерами файлов
bash
# Маленький файл (1 байт)
echo "A" > small.txt
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input small.txt --output small.enc
python cryptocore.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input small.enc --output small_dec.txt

# Средний файл (1KB)
python -c "import os; open('medium.bin', 'wb').write(os.urandom(1024))"
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input medium.bin --output medium.enc
python cryptocore.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input medium.enc --output medium_dec.bin

# Большой файл (1MB)
python -c "import os; open('large.bin', 'wb').write(os.urandom(1048576))"
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input large.bin --output large.enc
python cryptocore.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input large.enc --output large_dec.bin
Проверка работы программы
Проверка аргументов командной строки
bash
# Проверка справки
python cryptocore.py --help

# Проверка валидации аргументов (должны вызвать ошибки)
python cryptocore.py --algorithm des --mode ecb --encrypt --key 001122 --input test.txt  # Неверный алгоритм
python cryptocore.py --algorithm aes --mode cbc --encrypt --key 001122 --input test.txt  # Неверный режим
python cryptocore.py --algorithm aes --mode ecb --key 001122 --input test.txt           # Отсутствует операция
python cryptocore.py --algorithm aes --mode ecb --encrypt --decrypt --key 001122 --input test.txt  # Конфликт операций
python cryptocore.py --algorithm aes --mode ecb --encrypt --key invalid_key --input test.txt      # Неверный ключ
Проверка обработки ошибок
bash
# Несуществующий входной файл
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input nonexistent.txt --output test.enc

# Неверная длина ключа
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 001122 --input test.txt --output test.enc

# Неhex-символы в ключе
python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeefg --input test.txt --output test.enc
Форматы ключей
Поддерживаемые размеры ключей AES
AES-128: 16 байт (32 hex символа) - пример: 00112233445566778899aabbccddeeff

AES-192: 24 байта (48 hex символов) - пример: 00112233445566778899aabbccddeeff00112233445566778899aabb

AES-256: 32 байта (64 hex символа) - пример: 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff

