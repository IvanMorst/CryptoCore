#!/usr/bin/env python3
"""
CryptoCore CLI Tool
Командный интерфейс для криптографической системы
"""

import argparse
import sys
import os
from pathlib import Path

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from crypto.file_processor import FileProcessor
from crypto.crypto_logger import CryptoLogger
from crypto.crypto_exception import CryptoException
from csprng import CSPRNG
from hash.sha256 import sha256_file
from hash.sha3_256 import sha3_256_file


class CryptoCoreCLI:
    """Класс для обработки командной строки CryptoCore"""

    @staticmethod
    def create_parser():
        """Создание парсера аргументов с поддержкой старого и нового синтаксиса"""
        parser = argparse.ArgumentParser(
            description='CryptoCore - Cryptographic File Encryption/Decryption and Hashing Tool',
            epilog='Examples:\n'
                   '  # Encryption (old syntax):\n'
                   '  cryptocore --algorithm aes --mode ctr --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output ciphertext.bin\n\n'
                   '  # Encryption (new syntax):\n'
                   '  cryptocore encrypt --algorithm aes --mode ctr --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output ciphertext.bin\n\n'
                   '  # Hash computation:\n'
                   '  cryptocore dgst --algorithm sha256 --input document.pdf\n\n'
                   '  # Hash with output to file:\n'
                   '  cryptocore dgst --algorithm sha3-256 --input backup.tar --output backup.sha3',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        # 🆕 Создаем subparsers для новых команд
        subparsers = parser.add_subparsers(dest='command', help='Command to execute')

        # 🆕 Subcommand for hash operations
        dgst_parser = subparsers.add_parser('dgst', help='Compute message digest (hash)')

        dgst_parser.add_argument(
            '--algorithm',
            required=True,
            choices=['sha256', 'sha3-256'],
            help='Hash algorithm (sha256, sha3-256)'
        )

        dgst_parser.add_argument(
            '--input',
            required=True,
            help='Path to input file to be hashed'
        )

        dgst_parser.add_argument(
            '--output',
            help='Optional: write hash output to file instead of stdout'
        )

        # 🆕 Subcommand for encryption/decryption (новый синтаксис)
        encrypt_parser = subparsers.add_parser('encrypt', help='Encryption/decryption operations (new syntax)')

        # Старый синтаксис (прямые аргументы) - для обратной совместимости
        parser.add_argument(
            '--algorithm',
            help='Encryption algorithm (aes) - for backward compatibility'
        )

        parser.add_argument(
            '--mode',
            help='Encryption mode (ecb, cbc, ctr, cfb, ofb) - for backward compatibility'
        )

        # Взаимоисключающие флаги операции (для старого синтаксиса)
        operation_group = parser.add_mutually_exclusive_group()
        operation_group.add_argument(
            '--encrypt',
            action='store_true',
            help='Perform encryption operation - for backward compatibility'
        )

        operation_group.add_argument(
            '--decrypt',
            action='store_true',
            help='Perform decryption operation - for backward compatibility'
        )

        parser.add_argument(
            '--key',
            help='Encryption key as hexadecimal string (16, 24, or 32 bytes for AES). '
                 'If omitted for encryption, a secure random key will be generated and displayed.'
        )

        parser.add_argument(
            '--input',
            help='Path to input file'
        )

        parser.add_argument(
            '--output',
            help='Path to output file (default: generated based on operation)'
        )

        return parser

    @staticmethod
    def parse_arguments():
        """Парсинг аргументов командной строки"""
        parser = CryptoCoreCLI.create_parser()
        return parser.parse_args()

    @staticmethod
    def is_legacy_syntax(args):
        """Проверяем, используется ли старый синтаксис"""
        return (args.algorithm is not None or
                args.mode is not None or
                args.encrypt or
                args.decrypt)

    @staticmethod
    def validate_hex_key(key_str: str) -> bytes:
        """
        Валидация и преобразование hex-ключа в байты
        """
        if not key_str:
            raise ValueError("Key cannot be empty")

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
    def check_key_strength(key_bytes: bytes):
        """
        Проверка силы ключа и вывод предупреждений
        """
        if not CSPRNG.validate_key_strength(key_bytes):
            print(f"Warning: The provided key may be weak. Consider using a cryptographically secure random key.",
                  file=sys.stderr)

    @staticmethod
    def generate_default_output_path(input_path: str, encrypt: bool) -> str:
        """
        Генерация пути выходного файла по умолчанию
        """
        input_path = Path(input_path)

        if encrypt:
            return str(input_path.with_suffix(input_path.suffix + '.enc'))
        else:
            if input_path.suffix == '.enc':
                return str(input_path.with_suffix(input_path.suffix + '.dec'))
            else:
                return str(input_path.with_suffix(input_path.suffix + '.dec'))

    @staticmethod
    def process_hash_operation(args):
        """
        Обработка операции хеширования
        """
        try:
            # Проверка существования входного файла
            if not os.path.exists(args.input):
                raise FileNotFoundError(f"Input file not found: {args.input}")

            # Выбор алгоритма хеширования
            if args.algorithm == 'sha256':
                hash_value = sha256_file(args.input)
            elif args.algorithm == 'sha3-256':
                hash_value = sha3_256_file(args.input)
            else:
                raise ValueError(f"Unsupported hash algorithm: {args.algorithm}")

            # Форматирование вывода в стиле *sum tools
            output_line = f"{hash_value}  {args.input}\n"

            # Вывод результата
            if args.output:
                # Запись в файл
                with open(args.output, 'w') as f:
                    f.write(output_line)
                print(f"Hash written to: {args.output}")
            else:
                # Вывод в stdout
                print(output_line, end='')

            return True

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return False

    @staticmethod
    def process_crypto_operation(args, mode='ecb'):
        """
        Обработка криптографической операции
        """
        try:
            # Обработка ключа
            key_bytes = None
            key_was_generated = False

            if args.encrypt:
                if args.key:
                    # Используем предоставленный ключ
                    key_bytes = CryptoCoreCLI.validate_hex_key(args.key)
                    CryptoCoreCLI.check_key_strength(key_bytes)
                else:
                    # Генерируем случайный ключ
                    key_bytes = CSPRNG.generate_key(16)  # AES-128
                    key_hex = key_bytes.hex()
                    print(f"Generated random key: {key_hex}")
                    key_was_generated = True
            else:  # decrypt
                if not args.key:
                    raise ValueError("Key is required for decryption operations")
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

            # Используем режим из аргументов или значение по умолчанию
            crypto_mode = args.mode if hasattr(args, 'mode') and args.mode else mode

            # Выполнение операции
            if args.encrypt:
                CryptoCoreCLI.encrypt_file(args.input, output_path, key_bytes, crypto_mode)
            else:
                CryptoCoreCLI.decrypt_file(args.input, output_path, key_bytes, crypto_mode)

            return True

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return False

    @staticmethod
    def encrypt_file(input_path: str, output_path: str, key: bytes, mode: str):
        """
        Шифрование файла
        """
        from crypto.cipher_core import CipherCore

        # Создаем cipher core с предоставленным ключом и режимом
        cipher = CipherCore(key, mode)

        # Читаем входной файл
        with open(input_path, 'rb') as f:
            plaintext = f.read()

        # Шифруем данные
        encrypted = cipher.encrypt(plaintext)

        # Записываем результат
        with open(output_path, 'wb') as f:
            f.write(encrypted)

        print(f"Encryption successful: {input_path} -> {output_path}")
        print(f"Mode: {mode.upper()}")
        print(f"Key: {key.hex()}")
        print(f"Original size: {len(plaintext)} bytes")
        print(f"Encrypted size: {len(encrypted)} bytes")

    @staticmethod
    def decrypt_file(input_path: str, output_path: str, key: bytes, mode: str):
        """
        Дешифрование файла
        """
        from crypto.cipher_core import CipherCore

        # Создаем cipher core с предоставленным ключом и режимом
        cipher = CipherCore(key, mode)

        # Читаем зашифрованный файл
        with open(input_path, 'rb') as f:
            ciphertext = f.read()

        # Дешифруем данные
        decrypted = cipher.decrypt(ciphertext)

        # Записываем результат
        with open(output_path, 'wb') as f:
            f.write(decrypted)

        print(f"Decryption successful: {input_path} -> {output_path}")
        print(f"Mode: {mode.upper()}")
        print(f"Key: {key.hex()}")
        print(f"Encrypted size: {len(ciphertext)} bytes")
        print(f"Decrypted size: {len(decrypted)} bytes")

    @staticmethod
    def process_operation(args):
        """
        Основной обработчик операций
        """
        if args.command == 'dgst':
            return CryptoCoreCLI.process_hash_operation(args)
        elif CryptoCoreCLI.is_legacy_syntax(args):
            # Старый синтаксис - проверяем обязательные аргументы
            if not args.algorithm:
                raise ValueError("--algorithm is required for encryption/decryption")
            if not args.mode:
                raise ValueError("--mode is required for encryption/decryption")
            if not (args.encrypt or args.decrypt):
                raise ValueError("Either --encrypt or --decrypt must be specified")
            if not args.input:
                raise ValueError("--input is required")

            return CryptoCoreCLI.process_crypto_operation(args)
        elif args.command == 'encrypt':
            # Новый синтаксис для шифрования
            if not hasattr(args, 'algorithm') or not args.algorithm:
                raise ValueError("--algorithm is required for encryption/decryption")
            if not hasattr(args, 'mode') or not args.mode:
                raise ValueError("--mode is required for encryption/decryption")
            if not hasattr(args, 'input') or not args.input:
                raise ValueError("--input is required")

            return CryptoCoreCLI.process_crypto_operation(args)
        else:
            # Если команда не указана, покажем помощь
            if not args.command and not CryptoCoreCLI.is_legacy_syntax(args):
                CryptoCoreCLI.create_parser().print_help()
                return False
            else:
                raise ValueError(f"Invalid command or arguments")


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