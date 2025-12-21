# CryptoCore API Documentation

## Оглавление
- [Обзор](#обзор)
- [Быстрый старт](#быстрый-старт)
- [Основные модули](#основные-модули)
- [CLI Интерфейс](#cli-интерфейс)
- [Программный API](#программный-api)
- [Примеры использования](#примеры-использования)
- [Безопасность](#безопасность)
- [Обработка ошибок](#обработка-ошибок)
- [Производительность](#производительность)

## Обзор

CryptoCore - это криптографическая библиотека на Python с поддержкой:
- Шифрование/дешифрование AES (ECB, CBC, CTR, CFB, OFB, GCM)
- Хеш-функции (SHA-256, SHA3-256)
- Аутентификация (HMAC-SHA256)
- Функции вывода ключей (PBKDF2, Key Hierarchy)
- AEAD режимы (GCM, Encrypt-then-MAC)
- Генерация криптографических материалов

## Быстрый старт

### Установка
```bash
# Клонирование репозитория
git clone <repository-url>
cd CryptoCore

# Установка зависимостей
pip install -r requirements.txt
Базовое использование CLI
bash
# Шифрование файла
python cryptocore.py encrypt --algorithm aes --mode cbc --encrypt \
  --key 00112233445566778899aabbccddeeff \
  --input document.txt --output document.enc

# Дешифрование файла
python cryptocore.py encrypt --algorithm aes --mode cbc --decrypt \
  --key 00112233445566778899aabbccddeeff \
  --input document.enc --output document_decrypted.txt

# Вычисление хеша
python cryptocore.py dgst --algorithm sha256 --input file.txt

# Вывод ключа из пароля
python cryptocore.py derive --password "MySecurePassword" \
  --iterations 100000 --length 32
Основные модули
1. Шифрование (crypto/cipher_core.py)
python
from crypto.cipher_core import CipherCore

# Инициализация шифра
cipher = CipherCore(key=key_bytes, mode='cbc')  # Поддерживаемые режимы: ecb, cbc, ctr, cfb, ofb

# Шифрование
encrypted = cipher.encrypt(plaintext_bytes)

# Дешифрование
decrypted = cipher.decrypt(ciphertext_bytes)

# Информация о ключе
key_info = cipher.get_key_info()
2. Хеш-функции (hash/ директория)
python
from hash.sha256 import sha256, sha256_file
from hash.sha3_256 import sha3_256, sha3_256_file

# Однократное хеширование
hash_value = sha256(b"data to hash")

# Хеширование файла
file_hash = sha256_file("path/to/file.txt")

# SHA3-256
sha3_hash = sha3_256(b"data")
3. HMAC (mac/hmac.py)
python
from mac.hmac import HMAC, hmac_sha256, verify_hmac

# Использование класса
hmac = HMAC(key=key_bytes, hash_func_name='sha256')
mac_value = hmac.compute(message_bytes)
mac_hex = hmac.compute_hex(message_bytes)

# Удобные функции
mac = hmac_sha256(key_bytes, message_bytes)
is_valid = verify_hmac(key_bytes, message_bytes, expected_mac_hex)
4. AEAD Режимы (crypto/aead/)
python
# GCM (Galois/Counter Mode)
from crypto.aead.gcm import GCM

gcm = GCM(key=key_bytes, nonce=nonce_bytes)  # nonce генерируется автоматически если не указан
encrypted_with_tag = gcm.encrypt(plaintext_bytes, aad=aad_bytes)
decrypted = gcm.decrypt(encrypted_data, aad=aad_bytes)

# Encrypt-then-MAC
from crypto.aead.encrypt_then_mac import EncryptThenMAC

etm = EncryptThenMAC(enc_key=enc_key_bytes, mac_key=mac_key_bytes)
encrypted = etm.encrypt(plaintext_bytes, aad=aad_bytes)
decrypted = etm.decrypt(encrypted_data, aad=aad_bytes)
5. Функции вывода ключей (kdf/)
python
from kdf.pbkdf2 import pbkdf2_hmac_sha256, generate_salt
from kdf.key_hierarchy import derive_key, derive_keys

# PBKDF2
salt = generate_salt(16)  # 16 байт случайной соли
derived_key = pbkdf2_hmac_sha256(
    password="MyPassword",
    salt=salt,
    iterations=100000,
    dklen=32
)

# Иерархия ключей
master_key = os.urandom(32)
encryption_key = derive_key(master_key, "encryption", 32)
auth_key = derive_key(master_key, "authentication", 32)

# Множественное выведение ключей
keys = derive_keys(master_key, ["encryption", "mac", "iv"], 32)
6. Генерация случайных данных (csprng.py, generator.py)
python
from csprng import generate_key, generate_iv, generate_random_bytes
from generator import Generator

# Криптографически безопасная генерация
key = generate_key(16)  # AES-128 ключ
iv = generate_iv(16)    # Вектор инициализации
random_bytes = generate_random_bytes(64)

# Генерация тестовых файлов
Generator.generate_test_file("test.bin", size=1024*1024)  # 1MB файл
7. Обработка файлов (crypto/file_processor.py)
python
from crypto.file_processor import FileProcessor

# Шифрование файла
FileProcessor.process_file(
    input_path="plain.txt",
    output_path="encrypted.bin",
    key=key_bytes,
    mode="cbc",
    encrypt=True
)

# Дешифрование файла
FileProcessor.process_file(
    input_path="encrypted.bin",
    output_path="decrypted.txt",
    key=key_bytes,
    mode="cbc",
    encrypt=False,
    iv=iv_bytes  # опционально
)

# Проверка целостности
is_identical = FileProcessor.verify_file_integrity(
    "original.txt",
    "restored.txt"
)
8. Логирование (crypto/crypto_logger.py)
python
from crypto.crypto_logger import CryptoLogger

# Автоматическая инициализация при первом вызове
CryptoLogger.log("Operation started")
CryptoLogger.log("Error occurred", is_error=True)
CryptoLogger.log_performance("Encryption", bytes_processed=1024, start_time=time.time())
CLI Интерфейс
Команды
1. Шифрование/Дешифрование
bash
# Новый синтаксис
python cryptocore.py encrypt --algorithm aes --mode cbc --encrypt \
  --key 00112233445566778899aabbccddeeff \
  --input plain.txt --output encrypted.bin

# Старый синтаксис (обратная совместимость)
python cryptocore.py --algorithm aes --mode cbc --encrypt \
  --key 00112233445566778899aabbccddeeff \
  --input plain.txt --output encrypted.bin
2. Хеширование/HMAC
bash
# Обычное хеширование
python cryptocore.py dgst --algorithm sha256 --input file.txt

# HMAC
python cryptocore.py dgst --algorithm sha256 --hmac \
  --key 00112233445566778899aabbccddeeff \
  --input message.txt

# Верификация HMAC
python cryptocore.py dgst --algorithm sha256 --hmac \
  --key 00112233445566778899aabbccddeeff \
  --input message.txt --verify expected_hmac.txt
3. Вывод ключей
bash
# Базовый вывод с указанной солью
python cryptocore.py derive --password "MyPassword" \
  --salt a1b2c3d4e5f601234567890123456789 \
  --iterations 100000 --length 32

# Автоматическая генерация соли
python cryptocore.py derive --password "AnotherPassword" \
  --iterations 500000 --length 16

# Сохранение ключа в файл
python cryptocore.py derive --password "app_key" \
  --output derived_key.bin
Параметры командной строки
Общие параметры
--input - Входной файл (обязательный)

--output - Выходной файл (опционально, генерируется автоматически)

--key - Ключ в hex-формате (16, 24 или 32 байта для AES)

--iv / --nonce - Вектор инициализации (hex, опционально)

Параметры шифрования
--algorithm - Алгоритм шифрования (aes)

--mode - Режим работы (ecb, cbc, ctr, cfb, ofb, gcm)

--encrypt / --decrypt - Операция (взаимоисключающие)

--aad - Дополнительные аутентифицированные данные для GCM (hex)

Параметры хеширования
--algorithm - Алгоритм хеширования (sha256, sha3-256)

--hmac - Включить режим HMAC

--verify - Файл с ожидаемым хешем/HMAC для проверки

Параметры вывода ключей
--password - Пароль для вывода ключа (обязательный)

--salt - Соль в hex-формате (опционально, генерируется автоматически)

--iterations - Количество итераций (по умолчанию: 100000)

--length - Длина ключа в байтах (по умолчанию: 32)

--algorithm - Алгоритм KDF (pbkdf2)

Программный API
Базовые функции
python
import os
from crypto.cipher_core import CipherCore
from mac.hmac import hmac_sha256
from kdf.pbkdf2 import pbkdf2_hmac_sha256

class CryptoCoreAPI:
    """Упрощенный API для общих операций"""
    
    @staticmethod
    def encrypt_file(input_file: str, output_file: str, key: bytes, mode: str = 'cbc') -> bool:
        """Шифрование файла"""
        from crypto.file_processor import FileProcessor
        try:
            FileProcessor.process_file(input_file, output_file, key, mode, encrypt=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def decrypt_file(input_file: str, output_file: str, key: bytes, mode: str = 'cbc') -> bool:
        """Дешифрование файла"""
        from crypto.file_processor import FileProcessor
        try:
            FileProcessor.process_file(input_file, output_file, key, mode, encrypt=False)
            return True
        except Exception:
            return False
    
    @staticmethod
    def derive_key_from_password(password: str, salt: bytes = None, 
                                iterations: int = 100000, length: int = 32) -> tuple:
        """Вывод ключа из пароля"""
        from kdf.pbkdf2 import generate_salt, pbkdf2_hmac_sha256
        
        if salt is None:
            salt = generate_salt(16)
        
        key = pbkdf2_hmac_sha256(password, salt, iterations, length)
        return key, salt
    
    @staticmethod
    def create_key_hierarchy(master_key: bytes, purposes: list) -> dict:
        """Создание иерархии ключей"""
        from kdf.key_hierarchy import derive_keys
        return derive_keys(master_key, purposes, 32)
Расширенное использование
python
# Потоковое шифрование больших файлов
def stream_encrypt_large_file(input_path: str, output_path: str, key: bytes, mode: str = 'ctr'):
    """Потоковое шифрование файла по блокам"""
    cipher = CipherCore(key, mode)
    block_size = 64 * 1024  # 64KB блоки
    
    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        while True:
            chunk = infile.read(block_size)
            if not chunk:
                break
            encrypted = cipher.encrypt(chunk)
            outfile.write(encrypted)

# Создание защищенного контейнера
def create_secure_container(data: bytes, password: str) -> dict:
    """Создание защищенного контейнера с метаданными"""
    import json
    from base64 import b64encode
    
    # Вывод ключа
    salt = os.urandom(16)
    key = pbkdf2_hmac_sha256(password, salt, 100000, 32)
    
    # Шифрование данных
    cipher = CipherCore(key, 'gcm')
    iv = cipher.iv
    encrypted = cipher.encrypt(data)
    
    # HMAC для целостности
    hmac_value = hmac_sha256(key, encrypted)
    
    # Формирование контейнера
    container = {
        'version': '1.0',
        'algorithm': 'AES-GCM',
        'salt': b64encode(salt).decode('utf-8'),
        'iv': b64encode(iv).decode('utf-8'),
        'hmac': b64encode(hmac_value).decode('utf-8'),
        'data': b64encode(encrypted).decode('utf-8'),
        'timestamp': time.time()
    }
    
    return container
Примеры использования
Пример 1: Защищенное хранение конфигурации
python
import json
from CryptoCoreAPI import CryptoCoreAPI

class SecureConfig:
    def __init__(self, password: str):
        self.password = password
        self.master_key, self.salt = CryptoCoreAPI.derive_key_from_password(password)
    
    def encrypt_config(self, config: dict) -> bytes:
        """Шифрование конфигурации"""
        config_json = json.dumps(config).encode('utf-8')
        cipher = CipherCore(self.master_key, 'cbc')
        return cipher.encrypt(config_json)
    
    def decrypt_config(self, encrypted_config: bytes) -> dict:
        """Дешифрование конфигурации"""
        cipher = CipherCore(self.master_key, 'cbc')
        decrypted = cipher.decrypt(encrypted_config)
        return json.loads(decrypted.decode('utf-8'))
Пример 2: Многоуровневая защита файлов
python
def multi_layer_encrypt(input_file: str, output_file: str, passwords: list):
    """Многоуровневое шифрование с разными паролями"""
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Несколько уровней шифрования
    for i, password in enumerate(passwords):
        key, salt = CryptoCoreAPI.derive_key_from_password(password)
        cipher = CipherCore(key, 'ctr')
        data = cipher.encrypt(data)
        
        # Сохранение метаданных
        metadata = {
            'layer': i,
            'salt': salt.hex(),
            'iv': cipher.iv.hex() if cipher.iv else None
        }
        # Можно добавить metadata в заголовок файла
    
    with open(output_file, 'wb') as f:
        f.write(data)
Пример 3: Аутентифицированное шифрование для API
python
class SecureAPICommunicator:
    def __init__(self, shared_secret: bytes):
        self.shared_secret = shared_secret
        # Вывод ключей для разных целей
        self.keys = derive_keys(shared_secret, ['encryption', 'authentication', 'nonce'], 32)
    
    def encrypt_message(self, message: dict) -> dict:
        """Шифрование и аутентификация сообщения"""
        import json
        import time
        
        # Подготовка сообщения
        message['timestamp'] = time.time()
        message_json = json.dumps(message).encode('utf-8')
        
        # Шифрование
        cipher = CipherCore(self.keys['encryption'], 'gcm')
        encrypted = cipher.encrypt(message_json, aad=b'api_communication')
        
        # Создание MAC
        mac = hmac_sha256(self.keys['authentication'], encrypted)
        
        return {
            'data': encrypted.hex(),
            'nonce': cipher.iv.hex(),
            'mac': mac.hex()
        }
    
    def decrypt_message(self, package: dict) -> dict:
        """Верификация и дешифрование сообщения"""
        import json
        
        # Верификация MAC
        encrypted = bytes.fromhex(package['data'])
        expected_mac = bytes.fromhex(package['mac'])
        computed_mac = hmac_sha256(self.keys['authentication'], encrypted)
        
        if computed_mac != expected_mac:
            raise AuthenticationError("MAC verification failed")
        
        # Дешифрование
        nonce = bytes.fromhex(package['nonce'])
        cipher = CipherCore(self.keys['encryption'], 'gcm')
        cipher.iv = nonce
        decrypted = cipher.decrypt(encrypted, aad=b'api_communication')
        
        return json.loads(decrypted.decode('utf-8'))
Безопасность
Рекомендации
Ключи

Используйте ключи длиной не менее 256 бит (32 байта)

Никогда не используйте статические ключи в коде

Регулярно обновляйте ключи

Пароли

Минимальная длина: 12 символов

Используйте PBKDF2 с ≥100,000 итераций

Всегда используйте уникальную соль

Режимы шифрования

Избегайте ECB режима для защищенных данных

Используйте GCM для аутентифицированного шифрования

Для файлов предпочтительны CBC или CTR

Векторы инициализации

Никогда не используйте статические IV

IV должен быть уникальным для каждого шифрования

Для GCM используйте 12-байтные nonce

Практики безопасности
python
# ПРАВИЛЬНО: Безопасная инициализация
def secure_encryption_setup():
    from csprng import generate_key, generate_iv
    
    # Генерация криптографических материалов
    key = generate_key(32)  # AES-256
    iv = generate_iv(16)    # Случайный IV
    
    return CipherCore(key, 'cbc')

# НЕПРАВИЛЬНО: Небезопасные практики
def insecure_encryption_setup():
    # Статический ключ (НЕДОПУСТИМО!)
    static_key = b'\x00' * 16
    # Статический IV (НЕДОПУСТИМО!)
    static_iv = b'\x00' * 16
    
    return CipherCore(static_key, 'ecb')  # ECB режим (НЕДОПУСТИМО!)
Обработка ошибок
Базовые исключения
python
from crypto.crypto_exception import CryptoException

try:
    cipher = CipherCore(key, mode)
    encrypted = cipher.encrypt(data)
except ValueError as e:
    # Некорректные параметры (длина ключа, режим и т.д.)
    print(f"Validation error: {e}")
except Exception as e:
    # Общая ошибка
    crypto_ex = CryptoException("Encryption failed", e)
    crypto_ex.log_error()  # Запись в лог
Классы исключений
CryptoException - Базовое исключение криптосистемы

AuthenticationError (из gcm.py) - Ошибка аутентификации GCM

ValueError - Некорректные параметры

IOError - Ошибки ввода/вывода файлов

Рекомендации по обработке ошибок
python
def safe_file_operation(func, *args, **kwargs):
    """Безопасное выполнение файловых операций с обработкой ошибок"""
    from crypto.crypto_logger import CryptoLogger
    
    try:
        CryptoLogger.log(f"Starting {func.__name__}")
        result = func(*args, **kwargs)
        CryptoLogger.log(f"Completed {func.__name__} successfully")
        return result
    except FileNotFoundError as e:
        CryptoLogger.log(f"File not found: {e}", is_error=True)
        raise
    except IOError as e:
        CryptoLogger.log(f"IO error: {e}", is_error=True)
        raise
    except Exception as e:
        CryptoLogger.log(f"Unexpected error in {func.__name__}: {e}", is_error=True)
        raise CryptoException(f"Operation failed: {func.__name__}", e)
Производительность
Бенчмаркинг
python
from generator import Generator

# Бенчмарк генератора случайных чисел
benchmark_results = Generator.benchmark_generation(
    iterations=10,
    size_per_iteration=1024*1024  # 1MB на итерацию
)

print(f"Average speed: {benchmark_results['avg_speed_mb_s']:.2f} MB/s")
print(f"Average entropy: {benchmark_results['avg_entropy']:.2f} bits/byte")
Оптимизации
Размер блоков

Для файловых операций используйте блоки 64KB-1MB

Для сетевой передачи используйте блоки 4KB-16KB

Кэширование ключей

python
class KeyCache:
    def __init__(self):
        self._cache = {}
    
    def get_cipher(self, key: bytes, mode: str) -> CipherCore:
        cache_key = (key, mode)
        if cache_key not in self._cache:
            self._cache[cache_key] = CipherCore(key, mode)
        return self._cache[cache_key]
Параллельная обработка

python
from concurrent.futures import ThreadPoolExecutor

def parallel_encrypt_files(files: list, key: bytes, mode: str):
    """Параллельное шифрование файлов"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for input_file, output_file in files:
            future = executor.submit(
                FileProcessor.process_file,
                input_file, output_file, key, mode, True
            )
            futures.append(future)
        
        # Ожидание завершения
        for future in futures:
            future.result()
Заключение
CryptoCore предоставляет полный набор криптографических примитивов для безопасной разработки приложений. Библиотека спроектирована с акцентом на безопасность, производительность и простоту использования.

Дополнительные ресурсы
README.md - Основная документация

Требования спринтов - Детальные требования

Примеры использования - Практические примеры

Тесты - Модульные и интеграционные тесты

Поддержка
Вопросы и баги: Issues в репозитории

Предложения: Pull requests

Безопасность: Сообщения о уязвимостях через security email