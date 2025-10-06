#!/usr/bin/env python3
"""
CryptoCore CLI Tool
Командный интерфейс для криптографической системы
"""

import argparse
import sys
import os
from pathlib import Path

# Добавляем путь для импорта crypto модуля
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from crypto.file_processor import FileProcessor
from crypto.crypto_logger import CryptoLogger
from crypto.crypto_exception import CryptoException


class CryptoCoreCLI:
    """Класс для обработки командной строки CryptoCore"""

    @staticmethod
    def parse_arguments():
        """Парсинг аргументов командной строки"""
        parser = argparse.ArgumentParser(
            description='CryptoCore - Cryptographic File Encryption/Decryption Tool',
            epilog='Example:\n'
                   '  cryptocore --algorithm aes --mode ecb --encrypt \\\n'
                   '             --key 00112233445566778899aabbccddeeff \\\n'
                   '             --input plaintext.txt --output ciphertext.bin\n'
                   '  cryptocore --algorithm aes --mode ecb --decrypt \\\n'
                   '             --key 00112233445566778899aabbccddeeff \\\n'
                   '             --input ciphertext.bin --output decrypted.txt',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        # Обязательные аргументы
        parser.add_argument(
            '--algorithm',
            required=True,
            choices=['aes'],
            help='Encryption algorithm (currently only aes supported)'
        )

        parser.add_argument(
            '--mode',
            required=True,
            choices=['ecb'],
            help='Encryption mode (currently only ecb supported)'
        )

        # Взаимоисключающие флаги операции
        operation_group = parser.add_mutually_exclusive_group(required=True)
        operation_group.add_argument(
            '--encrypt',
            action='store_true',
            help='Perform encryption operation'
        )
        operation_group.add_argument(
            '--decrypt',
            action='store_true',
            help='Perform decryption operation'
        )

        parser.add_argument(
            '--key',
            required=True,
            help='Encryption key as hexadecimal string (16, 24, or 32 bytes for AES)'
        )

        parser.add_argument(
            '--input',
            required=True,
            help='Path to input file'
        )

        parser.add_argument(
            '--output',
            help='Path to output file (default: generated based on operation)'
        )

        return parser.parse_args()

    @staticmethod
    def validate_hex_key(key_str: str) -> bytes:
        """
        Валидация и преобразование hex-ключа в байты

        Args:
            key_str: hex-строка ключа

        Returns:
            bytes: ключ в виде байтов

        Raises:
            ValueError: если ключ невалидный
        """
        # Удаляем возможные префиксы и пробелы
        key_str = key_str.lower().strip().replace(' ', '').replace(':', '')

        if key_str.startswith('0x'):
            key_str = key_str[2:]

        # Проверяем что строка состоит только из hex символов
        if not all(c in '0123456789abcdef' for c in key_str):
            raise ValueError("Key must be a valid hexadecimal string")

        # Проверяем длину ключа
        key_length = len(key_str)
        if key_length not in [32, 48, 64]:  # 16, 24, 32 байта в hex
            raise ValueError(
                f"Key must be 16, 24, or 32 bytes (got {key_length // 2} bytes). "
                f"Hex string length should be 32, 48, or 64 characters"
            )

        # Преобразуем hex в байты
        try:
            key_bytes = bytes.fromhex(key_str)
        except ValueError as e:
            raise ValueError(f"Invalid hex key: {e}")

        return key_bytes

    @staticmethod
    def generate_default_output_path(input_path: str, encrypt: bool) -> str:
        """
        Генерация пути выходного файла по умолчанию

        Args:
            input_path: путь к входному файлу
            encrypt: флаг операции (шифрование/дешифрование)

        Returns:
            str: путь выходного файла
        """
        input_path = Path(input_path)

        if encrypt:
            # Для шифрования: input.txt -> input.txt.enc
            return str(input_path.with_suffix(input_path.suffix + '.enc'))
        else:
            # Для дешифрования: file.enc -> file.enc.dec
            if input_path.suffix == '.enc':
                return str(input_path.with_suffix(input_path.suffix + '.dec'))
            else:
                return str(input_path.with_suffix(input_path.suffix + '.dec'))

    @staticmethod
    def process_operation(args):
        """
        Обработка криптографической операции

        Args:
            args: аргументы командной строки

        Returns:
            bool: успех операции
        """
        try:
            # Валидация ключа
            key_bytes = CryptoCoreCLI.validate_hex_key(args.key)

            # Генерация выходного файла если не указан
            output_path = args.output
            if not output_path:
                output_path = CryptoCoreCLI.generate_default_output_path(
                    args.input, args.encrypt
                )
                print(f"Output file not specified. Using default: {output_path}")

            # Проверка существования входного файла
            if not os.path.exists(args.input):
                raise FileNotFoundError(f"Input file not found: {args.input}")

            # Проверка что выходной файл не совпадает с входным
            if os.path.abspath(args.input) == os.path.abspath(output_path):
                raise ValueError("Input and output files cannot be the same")

            # Выполнение операции
            if args.encrypt:
                CryptoCoreCLI.encrypt_file(args.input, output_path, key_bytes)
            else:
                CryptoCoreCLI.decrypt_file(args.input, output_path, key_bytes)

            return True

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return False

    @staticmethod
    def encrypt_file(input_path: str, output_path: str, key: bytes):
        """
        Шифрование файла

        Args:
            input_path: путь к входному файлу
            output_path: путь к выходному файлу
            key: ключ шифрования
        """
        from crypto.cipher_core import CipherCore

        # Создаем cipher core с предоставленным ключом
        cipher = CipherCore(key)

        # Читаем входной файл
        with open(input_path, 'rb') as f:
            plaintext = f.read()

        # Шифруем данные
        encrypted = cipher.encrypt(plaintext)

        # Записываем результат (без соли, так как ключ предоставлен напрямую)
        with open(output_path, 'wb') as f:
            f.write(encrypted)

        print(f"Encryption successful: {input_path} -> {output_path}")
        print(f"Key used: {key.hex()}")
        print(f"Original size: {len(plaintext)} bytes")
        print(f"Encrypted size: {len(encrypted)} bytes")

    @staticmethod
    def decrypt_file(input_path: str, output_path: str, key: bytes):
        """
        Дешифрование файла

        Args:
            input_path: путь к входному файлу
            output_path: путь к выходному файлу
            key: ключ дешифрования
        """
        from crypto.cipher_core import CipherCore

        # Создаем cipher core с предоставленным ключом
        cipher = CipherCore(key)

        # Читаем зашифрованный файл
        with open(input_path, 'rb') as f:
            ciphertext = f.read()

        # Дешифруем данные
        decrypted = cipher.decrypt(ciphertext)

        # Записываем результат
        with open(output_path, 'wb') as f:
            f.write(decrypted)

        print(f"Decryption successful: {input_path} -> {output_path}")
        print(f"Key used: {key.hex()}")
        print(f"Encrypted size: {len(ciphertext)} bytes")
        print(f"Decrypted size: {len(decrypted)} bytes")


def main():
    """Главная функция CLI"""
    try:
        # Парсинг аргументов
        args = CryptoCoreCLI.parse_arguments()

        # Обработка операции
        success = CryptoCoreCLI.process_operation(args)

        # Возвращаем код выхода
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()