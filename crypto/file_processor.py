import os
import time
from typing import Optional
from .cipher_core import CipherCore
from .key_generator import KeyGenerator
from .crypto_logger import CryptoLogger


class FileProcessor:
    SALT_SIZE = 16

    @staticmethod
    def generate_test_file(path: str, size: int):
        """Генерация тестового файла"""
        start_time = time.time()

        with open(path, 'wb') as f:
            f.write(os.urandom(size))

        elapsed = time.time() - start_time
        speed = (size * 8) / elapsed / 1e6  # Mbps

        CryptoLogger.log(
            f"Generated test file: {path} "
            f"(size: {size} bytes, speed: {speed:.2f} Mbps)",
            False
        )

    @staticmethod
    def process_file(input_path: str, output_path: str,
                     password: str, encrypt: bool):
        """Обработка файла (шифрование/дешифрование)"""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        file_size = os.path.getsize(input_path)
        CryptoLogger.log(
            f"Processing {'encryption' if encrypt else 'decryption'}: "
            f"{input_path} -> {output_path} (size: {file_size} bytes)",
            False
        )

        start_time = time.time()

        try:
            if encrypt:
                # Читаем исходный файл
                with open(input_path, 'rb') as infile:
                    plaintext = infile.read()

                # Генерируем соль и ключ с помощью кастомного генератора
                salt = KeyGenerator.generate_salt()
                key = KeyGenerator.derive_key(password, salt)

                # Шифруем
                cipher = CipherCore(key)
                encrypted = cipher.encrypt(plaintext)

                # Записываем соль и зашифрованные данные
                with open(output_path, 'wb') as outfile:
                    outfile.write(salt)
                    outfile.write(encrypted)

                CryptoLogger.log(
                    f"Encryption: {len(plaintext)} -> {len(encrypted)} bytes "
                    f"+ {len(salt)} bytes salt ",
                    False
                )

            else:
                # Читаем зашифрованный файл
                with open(input_path, 'rb') as infile:
                    salt = infile.read(FileProcessor.SALT_SIZE)
                    if len(salt) != FileProcessor.SALT_SIZE:
                        raise ValueError(f"Invalid salt size: {len(salt)} bytes, expected {FileProcessor.SALT_SIZE}")

                    ciphertext = infile.read()

                # Генерируем ключ с помощью кастомного генератора
                key = KeyGenerator.derive_key(password, salt)
                cipher = CipherCore(key)
                decrypted = cipher.decrypt(ciphertext)

                # Записываем расшифрованные данные
                with open(output_path, 'wb') as outfile:
                    outfile.write(decrypted)

                CryptoLogger.log(
                    f"Decryption: {len(ciphertext)} -> {len(decrypted)} bytes "
                    f"",
                    False
                )

            elapsed = time.time() - start_time
            speed = (file_size * 8) / elapsed / 1e6
            CryptoLogger.log(
                f"{'Encryption' if encrypt else 'Decryption'} completed: "
                f"{speed:.2f} Mbps, {elapsed:.2f} seconds",
                False
            )

        except Exception as e:
            # Удаляем частично созданный файл при ошибке
            if os.path.exists(output_path):
                os.remove(output_path)
            CryptoLogger.log(f"Error details: {str(e)}", True)
            raise e