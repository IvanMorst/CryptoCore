import os
import time
import hashlib
from crypto.cipher_core import CipherCore

# Импорт для логирования
try:
    from crypto.crypto_logger import CryptoLogger

    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    print("Warning: CryptoLogger not available, logging disabled")


class FileProcessor:

    @staticmethod
    def _init_logging():
        """Инициализация логирования"""
        if LOGGING_AVAILABLE:
            CryptoLogger.setup_logging()

    @staticmethod
    def process_file(input_path: str, output_path: str, key: bytes,
                     mode: str, encrypt: bool, iv: bytes = None):
        """
        Обработка файла с поддержкой разных режимов шифрования

        Args:
            input_path: путь к входному файлу
            output_path: путь к выходному файлу
            key: ключ шифрования
            mode: режим работы
            encrypt: True для шифрования, False для дешифрования
            iv: вектор инициализации (для дешифрования)
        """
        # Инициализация логирования
        FileProcessor._init_logging()

        if not os.path.exists(input_path):
            error_msg = f"Input file not found: {input_path}"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise FileNotFoundError(error_msg)

        file_size = os.path.getsize(input_path)
        operation = "encryption" if encrypt else "decryption"

        # Логирование начала операции
        if LOGGING_AVAILABLE:
            CryptoLogger.log_file_operation(
                operation=f"{operation} ({mode})",
                input_file=input_path,
                output_file=output_path,
                key_info={
                    'hex': key.hex() if key else 'N/A',
                    'algorithm': 'AES',
                    'mode': mode.upper(),
                    'key_size': len(key) * 8
                }
            )

            CryptoLogger.log(
                f"Starting file {operation}: "
                f"input={input_path}, "
                f"output={output_path}, "
                f"size={file_size} bytes, "
                f"mode={mode}"
            )

        start_time = time.time()

        try:
            if encrypt:
                if LOGGING_AVAILABLE:
                    CryptoLogger.log(f"Encrypting {file_size} bytes")
                FileProcessor._encrypt_file(input_path, output_path, key, mode)
            else:
                if LOGGING_AVAILABLE:
                    CryptoLogger.log(f"Decrypting {file_size} bytes")
                    if iv:
                        CryptoLogger.log(f"Using provided IV: {iv.hex()}")
                FileProcessor._decrypt_file(input_path, output_path, key, mode, iv)

            elapsed = time.time() - start_time

            # Логирование производительности
            if LOGGING_AVAILABLE:
                CryptoLogger.log_performance(
                    f"File {operation}",
                    file_size,
                    start_time
                )

                # Детальное логирование завершения
                CryptoLogger.log(
                    f"{operation.capitalize()} completed successfully: "
                    f"{input_path} -> {output_path} "
                    f"({file_size} bytes in {elapsed:.2f}s)"
                )

                # Проверка целостности выходного файла
                if os.path.exists(output_path):
                    output_size = os.path.getsize(output_path)
                    CryptoLogger.log(f"Output file created: {output_path} ({output_size} bytes)")

        except Exception as e:
            error_msg = f"Error during {operation}: {str(e)}"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)

            # Очистка частично созданного файла
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                    if LOGGING_AVAILABLE:
                        CryptoLogger.log(f"Removed partial output file: {output_path}")
                except Exception as cleanup_error:
                    if LOGGING_AVAILABLE:
                        CryptoLogger.log(f"Failed to remove partial file: {cleanup_error}", is_error=True)

            raise e

    @staticmethod
    def _encrypt_file(input_path: str, output_path: str, key: bytes, mode: str):
        """Шифрование файла"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Reading file for encryption: {input_path}")

        with open(input_path, 'rb') as infile:
            plaintext = infile.read()

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"File read: {len(plaintext)} bytes")

            # Вычисление хеша исходного файла
            input_hash = hashlib.sha256(plaintext).hexdigest()[:16]
            CryptoLogger.log(f"Input file SHA-256 (first 16 chars): {input_hash}")

        # Создание шифра
        cipher_start = time.time()
        cipher = CipherCore(key, mode)
        cipher_creation_time = time.time() - cipher_start

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Cipher created in {cipher_creation_time:.3f}s")

        # Шифрование
        encrypt_start = time.time()
        encrypted = cipher.encrypt(plaintext)
        encrypt_time = time.time() - encrypt_start

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"Encryption time: {encrypt_time:.3f}s, "
                f"throughput: {len(plaintext) / encrypt_time / 1024 / 1024:.2f} MB/s"
            )
            CryptoLogger.log(
                f"Size change: {len(plaintext)} -> {len(encrypted)} bytes "
                f"(+{len(encrypted) - len(plaintext)} bytes)"
            )

        with open(output_path, 'wb') as outfile:
            outfile.write(encrypted)

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"Encryption completed: {len(plaintext)} -> {len(encrypted)} bytes "
                f"(mode: {mode}, iv: {cipher.iv.hex() if cipher.iv else 'N/A'})"
            )

            # Проверка записи
            if os.path.exists(output_path):
                written_size = os.path.getsize(output_path)
                if written_size == len(encrypted):
                    CryptoLogger.log(f"File written successfully: {written_size} bytes")
                else:
                    CryptoLogger.log(
                        f"File size mismatch: expected {len(encrypted)}, got {written_size}",
                        is_error=True
                    )

    @staticmethod
    def _decrypt_file(input_path: str, output_path: str, key: bytes,
                      mode: str, iv: bytes = None):
        """Дешифрование файла"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Reading file for decryption: {input_path}")

        with open(input_path, 'rb') as infile:
            if mode != 'ecb':
                # Читаем IV из файла если не предоставлен
                if iv is None:
                    file_iv = infile.read(16)
                    if len(file_iv) != 16:
                        error_msg = f"Invalid IV in file: expected 16 bytes, got {len(file_iv)}"
                        if LOGGING_AVAILABLE:
                            CryptoLogger.log(error_msg, is_error=True)
                        raise ValueError(error_msg)
                    if LOGGING_AVAILABLE:
                        CryptoLogger.log(f"Read IV from file: {file_iv.hex()}")
                else:
                    file_iv = iv
                    if LOGGING_AVAILABLE:
                        CryptoLogger.log(f"Using provided IV: {file_iv.hex()}")
                ciphertext = infile.read()
            else:
                file_iv = None
                ciphertext = infile.read()

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"File read: {len(ciphertext)} bytes (mode: {mode})")

        # Создание шифра
        cipher_start = time.time()
        cipher = CipherCore(key, mode)
        cipher_creation_time = time.time() - cipher_start

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Cipher created in {cipher_creation_time:.3f}s")

        # Дешифрование
        decrypt_start = time.time()
        decrypted = cipher.decrypt(ciphertext)
        decrypt_time = time.time() - decrypt_start

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"Decryption time: {decrypt_time:.3f}s, "
                f"throughput: {len(ciphertext) / decrypt_time / 1024 / 1024:.2f} MB/s"
            )
            CryptoLogger.log(
                f"Size change: {len(ciphertext)} -> {len(decrypted)} bytes "
                f"(-{len(ciphertext) - len(decrypted)} bytes)"
            )

        with open(output_path, 'wb') as outfile:
            outfile.write(decrypted)

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"Decryption completed: {len(ciphertext)} -> {len(decrypted)} bytes "
                f"(mode: {mode}, iv: {file_iv.hex() if file_iv else 'N/A'})"
            )

            # Вычисление хеша дешифрованного файла
            output_hash = hashlib.sha256(decrypted).hexdigest()[:16]
            CryptoLogger.log(f"Output file SHA-256 (first 16 chars): {output_hash}")

            # Проверка записи
            if os.path.exists(output_path):
                written_size = os.path.getsize(output_path)
                if written_size == len(decrypted):
                    CryptoLogger.log(f"File written successfully: {written_size} bytes")
                else:
                    CryptoLogger.log(
                        f"File size mismatch: expected {len(decrypted)}, got {written_size}",
                        is_error=True
                    )

    @staticmethod
    def verify_file_integrity(original_path: str, restored_path: str) -> bool:
        """
        Проверка целостности файла после шифрования/дешифрования

        Args:
            original_path: путь к оригинальному файлу
            restored_path: путь к восстановленному файлу

        Returns:
            bool: True если файлы идентичны
        """
        FileProcessor._init_logging()

        if not os.path.exists(original_path):
            error_msg = f"Original file not found: {original_path}"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise FileNotFoundError(error_msg)

        if not os.path.exists(restored_path):
            error_msg = f"Restored file not found: {restored_path}"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise FileNotFoundError(error_msg)

        # Сравнение размеров
        original_size = os.path.getsize(original_path)
        restored_size = os.path.getsize(restored_path)

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"Verifying integrity: "
                f"original={original_path} ({original_size} bytes), "
                f"restored={restored_path} ({restored_size} bytes)"
            )

        if original_size != restored_size:
            if LOGGING_AVAILABLE:
                CryptoLogger.log(
                    f"Size mismatch: original={original_size}, restored={restored_size}",
                    is_error=True
                )
            return False

        # Сравнение содержимого по блокам
        block_size = 65536  # 64KB
        identical = True
        differences = 0

        with open(original_path, 'rb') as f1, open(restored_path, 'rb') as f2:
            block_num = 0
            while True:
                block1 = f1.read(block_size)
                block2 = f2.read(block_size)

                if not block1 and not block2:
                    break

                if block1 != block2:
                    identical = False
                    differences += 1

                    if LOGGING_AVAILABLE and differences <= 3:  # Логируем только первые 3 различия
                        CryptoLogger.log(
                            f"Difference at block {block_num} (offset: {block_num * block_size})",
                            is_error=True
                        )

                block_num += 1

        if LOGGING_AVAILABLE:
            if identical:
                CryptoLogger.log(f"Files are identical: {original_path} == {restored_path}")
            else:
                CryptoLogger.log(
                    f"Files differ: {differences} block(s) different",
                    is_error=True
                )

        return identical


# Удобные функции для работы с файлами
def encrypt_file(input_path: str, output_path: str, key: bytes, mode: str = 'ecb') -> bool:
    """
    Удобная функция для шифрования файла

    Returns:
        bool: True если операция успешна
    """
    try:
        FileProcessor.process_file(input_path, output_path, key, mode, encrypt=True)
        return True
    except Exception as e:
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"File encryption failed: {e}", is_error=True)
        return False


def decrypt_file(input_path: str, output_path: str, key: bytes, mode: str = 'ecb') -> bool:
    """
    Удобная функция для дешифрования файла

    Returns:
        bool: True если операция успешна
    """
    try:
        FileProcessor.process_file(input_path, output_path, key, mode, encrypt=False)
        return True
    except Exception as e:
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"File decryption failed: {e}", is_error=True)
        return False