import os
import time
from typing import Optional
from .cipher_core import CipherCore
from .crypto_logger import CryptoLogger


class FileProcessor:
    """
    Обработчик файлов для нового CLI интерфейса
    Работает с готовыми ключами, а не паролями
    """

    @staticmethod
    def process_file_direct_key(input_path: str, output_path: str,
                                key: bytes, encrypt: bool):
        """
        Обработка файла с использованием прямого ключа (для CLI)

        :param input_path: путь к входному файлу
        :param output_path: путь к выходному файлу
        :param key: готовый ключ в байтах
        :param encrypt: True для шифрования, False для дешифрования
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        file_size = os.path.getsize(input_path)
        operation = "encryption" if encrypt else "decryption"

        CryptoLogger.log(
            f"Processing {operation}: {input_path} -> {output_path} "
            f"(size: {file_size} bytes, key: {key.hex()[:16]}...)",
            False
        )

        start_time = time.time()

        try:
            # Читаем файл
            with open(input_path, 'rb') as infile:
                file_data = infile.read()

            # Создаем cipher с прямым ключом
            cipher = CipherCore(key)

            # Выполняем операцию
            if encrypt:
                processed_data = cipher.encrypt(file_data)
            else:
                processed_data = cipher.decrypt(file_data)

            # Записываем результат
            with open(output_path, 'wb') as outfile:
                outfile.write(processed_data)

            # Логируем результаты
            elapsed = time.time() - start_time
            speed = (file_size * 8) / elapsed / 1e6  # Mbps

            CryptoLogger.log(
                f"{operation.capitalize()} completed: "
                f"{len(file_data)} -> {len(processed_data)} bytes, "
                f"speed: {speed:.2f} Mbps, time: {elapsed:.2f}s",
                False
            )

        except Exception as e:
            # Удаляем частично созданный файл при ошибке
            if os.path.exists(output_path):
                os.remove(output_path)
            CryptoLogger.log(f"Error in {operation}: {str(e)}", True)
            raise e

    @staticmethod
    def generate_test_file(path: str, size: int):
        """Генерация тестового файла (для обратной совместимости)"""
        import os
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