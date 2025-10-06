CryptoCore - Криптографическая система с кастомным генератором ключей
```О проекте
CryptoCore - это консольная утилита для шифрования и дешифрования файлов с использованием кастомного генератора ключей и соли, адаптированного из Java реализации. Система использует AES-256 в режиме ECB с PKCS7 паддингом.

Возможности
 Шифрование/дешифрование любых типов файлов

 Кастомная генерация ключей на основе пароля и соли

 Генерация криптографически безопасных случайных данных

 Поддержка различных форматов файлов

 Проверка целостности данных

Логирование операций

 Установка 
```bash
# Клонирование репозитория
git clone <repository-url>
cd cryptocore
```
# Создание виртуального окружения
```bash

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
````
# или
```bash

.venv\Scripts\activate     # Windows
````
# Установка зависимостей
```bash

pip install -r requirements.txt
````
 ## Зависимости
```bash

pip install pycryptodome>=3.20.0 psutil>=5.8.0
````
 # Структура проекта

```cryptocore```

    ├── crypto/
    │   ├── __init__.py
    │   ├── cipher_core.py      # AES шифрование
    │   ├── crypto_core.py      # Интеграция кастомного генератора
    │   ├── crypto_exception.py # Исключения
    │   ├── crypto_logger.py    # Логирование
    │   ├── file_processor.py   # Обработка файлов
    │   ├── generator.py        # Генератор случайных данных
    │   └── key_generator.py    # Кастомный генератор ключей
    ├── main.py                 # Основной скрипт
    ├── requirements.txt        # Зависимости
    └── crypto.log             # Файл логов (создается автоматически)
 ## Команды CLI
 ## Базовые команды

# Показать помощь
```bash

python main.py --help
```

# Запустить тест системы
```bash

python main.py test
```
# Сгенерировать тестовый файл

```bash

python main.py gen-file -o test.bin -s 1048576
```

# Шифрование и дешифрование
## Общий формат:

# Шифрование
## python main.py encrypt -i input_file -o output_file -p password


# Дешифрование  
## python main.py decrypt -i input_file -o output_file -p password

 1. Текстовые файлы

# Шифрование текстового файла
```bash

python main.py encrypt -i test.txt -o document.enc -p "MySecret123"
```
# Дешифрование текстового файла
```bash

python main.py decrypt -i document.enc -o test_decrypted.txt -p "MySecret123"
```
# Проверка целостности
```bash

diff -s test.txt test_decrypted.txt 
```
2. PDF документы
bash
# Шифрование PDF
python main.py encrypt -i report.pdf -o report.enc -p "PdfSecure456"

# Дешифрование PDF
python main.py decrypt -i report.enc -o report_decrypted.pdf -p "PdfSecure456"

# Проверка PDF
file report_decrypted.pdf
ls -la report.pdf report_decrypted.pdf
 3. ZIP архивы
bash
# Шифрование архива
python main.py encrypt -i data.zip -o data.enc -p "Archive789"

# Дешифрование архива
python main.py decrypt -i data.enc -o data_decrypted.zip -p "Archive789"

# Проверка архива
unzip -t data_decrypted.zip
cmp data.zip data_decrypted.zip
 4. Папки (через архивирование)
bash
# Создание и шифрование архива папки
zip -r myfolder.zip myfolder/
python main.py encrypt -i myfolder.zip -o myfolder.enc -p "FolderPass"

# Дешифрование и распаковка
python main.py decrypt -i myfolder.enc -o myfolder_decrypted.zip -p "FolderPass"
unzip myfolder_decrypted.zip -d restored_folder/
 5. Изображения
bash
# Шифрование изображения
python main.py encrypt -i photo.jpg -o photo.enc -p "ImageKey999"

# Дешифрование изображения
python main.py decrypt -i photo.enc -o photo_decrypted.jpg -p "ImageKey999"

# Проверка изображения
file photo_decrypted.jpg
identify photo_decrypted.jpg  # для ImageMagick
 6. Аудио и видео файлы
bash
# Шифрование MP3
python main.py encrypt -i song.mp3 -o song.enc -p "AudioSecret"

# Дешифрование MP4
python main.py decrypt -i video.enc -o video_decrypted.mp4 -p "VideoSecret"

# Проверка медиафайлов
file video_decrypted.mp4
mpv video_decrypted.mp4  # проигрывание видео
 7. Базы данных и бинарные файлы
bash
# Шифрование SQLite базы
python main.py encrypt -i database.db -o database.enc -p "DbPassword123"

# Дешифрование бинарного файла
python main.py decrypt -i binary.enc -o binary_decrypted.bin -p "BinaryPass"

# Проверка бинарных файлов
cmp database.db database_decrypted.db
md5sum binary.bin binary_decrypted.bin
 Тестирование и проверка
Тестирование генератора ключей
bash
python main.py test
Полный тестовый цикл
bash
# Создание тестового файла
python main.py gen-file -o test.bin -s 4096

# Шифрование
python main.py encrypt -i test.bin -o test.enc -p "testpassword"

# Дешифрование
python main.py decrypt -i test.enc -o test_dec.bin -p "testpassword"

# Проверка целостности
cmp test.bin test_dec.bin
echo $?  # Должно вернуть 0 (успех)

# Проверка хешей
sha256sum test.bin test_dec.bin
Тестирование разных размеров файлов
bash
# Маленький файл (1KB)
python main.py gen-file -o small.bin -s 1024
python main.py encrypt -i small.bin -o small.enc -p "pass"
python main.py decrypt -i small.enc -o small_dec.bin -p "pass"

# Большой файл (10MB)
python main.py gen-file -o large.bin -s 10485760
python main.py encrypt -i large.bin -o large.enc -p "pass"
python main.py decrypt -i large.enc -o large_dec.bin -p "pass"
📊 Мониторинг и логи
Просмотр логов

# Просмотр всех логов
```bash

cat crypto.log
```
# Мониторинг логов в реальном времени
tail -f crypto.log

# Поиск ошибок
grep -i error crypto.log

# Поиск операций шифрования
grep -i encryption crypto.log

# Просмотр производительности
grep -i mbps crypto.log
Проверка файлов
bash
# Проверка размеров файлов
ls -la *.enc *.decrypted

# Проверка типов файлов
file encrypted_file.enc

# Проверка хешей
sha256sum original.file encrypted.file decrypted.file

# Побайтовое сравнение
cmp original.file decrypted.file