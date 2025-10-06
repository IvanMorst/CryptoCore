CryptoCore - Криптографическая система для шифрования и дешифрования файлов с использованием AES-256 в режиме ECB.

Структура проекта
````text
CryptoCore/
├── cryptocore.py # Главный исполняемый файл CLI
├── main.py # Устаревший интерфейс (для обратной совместимости)
├── setup.py # Конфигурация установки пакета
├── requirements.txt # Зависимости Python
├── README.md # Документация
└── crypto/ # Пакет с ядром криптосистемы
    ├── init.py
    ├── cipher_core.py # AES шифрование/дешифрование
    ├── crypto_core.py # Интеграция кастомного генератора
    ├── crypto_exception.py # Обработка исключений
    ├── crypto_logger.py # Система логирования
    ├── file_processor.py # Обработка файлов
    ├── generator.py # Генератор случайных данных
    ├── key_generator.py # Кастомный генератор ключей
    └── modes # Директория с режимами шифрования
        ├── init.py
        ├── base_mode.py # Базовый класс режимов
        ├── cbc_mode.py # Режим CBC
        ├── cfb_mode.py # Режим CFB
        ├── ofb_mode.py # Режим OFB
        └── ctr_mode.py # Режим CTR
    
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
## Дешифрование PDF документа

```bash 

python cryptocore.py --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input document.pdf.enc --output document_restored.pdf
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

# Дешифрование архива
python cryptocore.py --algorithm aes --mode ecb --decrypt --key aabbccddeeff00112233445566778899 --input archive.zip.enc
````
##Генерация тестовых ключей

##Генерация ключей AES

# AES-128 (16 байт, 32 hex символа)
```bash
python -c "import os; print('AES-128 key:', os.urandom(16).hex())"
````

## Примеры валидных ключей для тестирования

### AES-128 ключи
00112233445566778899aabbccddeeff
000102030405060708090a0b0c0d0e0f
a0a1a2a3a4a5a6a7a8a9aaabacadaeaf



## Тестирование и проверка целостности



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


```bash

diff test_original.txt decrypted_test.txt
```

### Проверка справки

```bash
python cryptocore.py --help
````


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

python cryptocore.py --algorithm aes --mode ecb --encrypt --key 00112233445566778899aabbccddeeff --input test_original.txt --output test_encrypted.bin
````
### Дешифрование файла в режиме

```bash

python cryptocore.py --algorithm aes --mode ecb --decrypt --key 00112233445566778899aabbccddeeff --input test_encrypted.bin --output test_decrypted.txt
````


## Шифрование и дешифрование в режиме CBC


### Шифрование файла в режиме CBC (IV генерируется автоматически)

```bash

python cryptocore.py --algorithm aes --mode cbc --encrypt --key 00112233445566778899aabbccddeeff --input document.pdf --output document.pdf.cbc.enc
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

python cryptocore.py --algorithm aes --mode cfb --encrypt --key 00112233445566778899aabbccddeeff --input image.jpg --output image.jpg.cfb.enc
```

### Дешифрование файла в режиме CFB

```bash

python cryptocore.py --algorithm aes --mode cfb --decrypt --key 00112233445566778899aabbccddeeff --input image.jpg.cfb.enc --output image_restored.jpg
```


## Шифрование и дешифрование в режиме OFB

### Шифрование файла в режиме OFB

```bash

python cryptocore.py --algorithm aes --mode ofb --encrypt --key 00112233445566778899aabbccddeeff --input data.bin --output data.bin.ofb.enc
````
### Дешифрование файла в режиме OFB

```bash

python cryptocore.py --algorithm aes --mode ofb --decrypt --key 00112233445566778899aabbccddeeff --input data.bin.ofb.enc --output data_restored.bin
```


## Шифрование и дешифрование в режиме CTR

### Шифрование файла в режиме CTR

```bash

python cryptocore.py --algorithm aes --mode ctr --encrypt --key 00112233445566778899aabbccddeeff --input archive.zip --output archive.zip.ctr.enc
````
### Дешифрование файла в режиме CTR

```bash

python cryptocore.py --algorithm aes --mode ctr --decrypt --key 00112233445566778899aabbccddeeff --input archive.zip.ctr.enc --output archive_restored.zip
```





Совместимость с OpenSSL

Шифрование нашим инструментом - дешифрование OpenSSL

bash
# 1. Шифрование CBC нашим инструментом
python cryptocore.py --algorithm aes --mode cbc --encrypt \
    --key 000102030405060708090a0b0c0d0e0f \
    --input plaintext.bin --output cryptocore_cipher.bin

# 2. Извлечение IV и шифртекста
dd if=cryptocore_cipher.bin of=iv.bin bs=16 count=1
dd if=cryptocore_cipher.bin of=ciphertext_only.bin bs=16 skip=1

# 3. Дешифрование OpenSSL
openssl enc -aes-128-cbc -d \
    -K 000102030405060708090a0b0c0d0e0f \
    -iv $(xxd -p iv.bin | tr -d '\n') \
    -in ciphertext_only.bin \
    -out openssl_decrypted.bin

Шифрование OpenSSL - дешифрование нашим инструментом
bash
# 1. Шифрование CBC OpenSSL
openssl enc -aes-128-cbc \
    -K 000102030405060708090a0b0c0d0e0f \
    -iv 00112233445566778899aabbccddeeff \
    -in plaintext.bin \
    -out openssl_cipher.bin

# 2. Дешифрование нашим инструментом с явным IV
python cryptocore.py --algorithm aes --mode cbc --decrypt \
    --key 000102030405060708090a0b0c0d0e0f \
    --iv 00112233445566778899aabbccddeeff \
    --input openssl_cipher.bin \
    --output cryptocore_decrypted.bin
