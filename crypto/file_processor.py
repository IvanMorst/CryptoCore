import os
import time
from crypto.cipher_core import CipherCore
from crypto.crypto_logger import CryptoLogger


class FileProcessor:
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
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        file_size = os.path.getsize(input_path)
        operation = "encryption" if encrypt else "decryption"

        CryptoLogger.log(
            f"Processing {operation} ({mode}): "
            f"{input_path} -> {output_path} (size: {file_size} bytes)",
            False
        )

        start_time = time.time()

        try:
            if encrypt:
                FileProcessor._encrypt_file(input_path, output_path, key, mode)
            else:
                FileProcessor._decrypt_file(input_path, output_path, key, mode, iv)

            elapsed = time.time() - start_time
            speed = (file_size * 8) / elapsed / 1e6 if elapsed > 0 else 0

            CryptoLogger.log(
                f"{operation.capitalize()} completed: "
                f"{speed:.2f} Mbps, {elapsed:.2f} seconds",
                False
            )

        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            CryptoLogger.log(f"Error details: {str(e)}", True)
            raise e

    @staticmethod
    def _encrypt_file(input_path: str, output_path: str, key: bytes, mode: str):
        """Шифрование файла"""
        with open(input_path, 'rb') as infile:
            plaintext = infile.read()

        cipher = CipherCore(key, mode)
        encrypted = cipher.encrypt(plaintext)

        with open(output_path, 'wb') as outfile:
            # Записываем IV для режимов кроме ECB
            if mode != 'ecb':
                outfile.write(cipher.get_iv())
            outfile.write(encrypted)

        CryptoLogger.log(
            f"Encryption: {len(plaintext)} -> {len(encrypted)} bytes "
            f"(mode: {mode}, iv: {cipher.get_iv().hex() if mode != 'ecb' else 'N/A'})",
            False
        )

    @staticmethod
    def _decrypt_file(input_path: str, output_path: str, key: bytes,
                      mode: str, iv: bytes = None):
        """Дешифрование файла"""
        with open(input_path, 'rb') as infile:
            if mode != 'ecb':
                # Читаем IV из файла если не предоставлен
                if iv is None:
                    file_iv = infile.read(16)
                    if len(file_iv) != 16:
                        raise ValueError(
                            f"Invalid IV in file: expected 16 bytes, got {len(file_iv)}"
                        )
                else:
                    file_iv = iv
                ciphertext = infile.read()
            else:
                file_iv = None
                ciphertext = infile.read()

        cipher = CipherCore(key, mode, file_iv)
        decrypted = cipher.decrypt(ciphertext)

        with open(output_path, 'wb') as outfile:
            outfile.write(decrypted)

        CryptoLogger.log(
            f"Decryption: {len(ciphertext)} -> {len(decrypted)} bytes "
            f"(mode: {mode}, iv: {file_iv.hex() if file_iv else 'N/A'})",
            False
        )