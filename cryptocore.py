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
from mac.hmac import hmac_sha256_file, verify_hmac_file  # 🆕 Импорт HMAC функций


class CryptoCoreCLI:
    """Класс для обработки командной строки CryptoCore"""

    @staticmethod
    def create_parser():
        """Создание парсера аргументов"""
        parser = argparse.ArgumentParser(
            description='CryptoCore - Cryptographic File Encryption/Decryption, Hashing, and HMAC Tool',
            epilog='Examples:\n'
                   '  # Hash computation:\n'
                   '  cryptocore dgst --algorithm sha256 --input document.pdf\n\n'
                   '  # HMAC generation:\n'
                   '  cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt\n\n'
                   '  # HMAC verification:\n'
                   '  cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt --verify expected_hmac.txt\n\n'
                   '  # Encryption (old syntax):\n'
                   '  cryptocore --algorithm aes --mode ctr --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output ciphertext.bin',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        # Old syntax arguments (for backward compatibility)
        parser.add_argument(
            '--algorithm',
            help='Encryption algorithm (aes) - for backward compatibility'
        )

        parser.add_argument(
            '--mode',
            help='Encryption mode (ecb, cbc, ctr, cfb, ofb) - for backward compatibility'
        )

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
            help='Encryption/HMAC key as hexadecimal string. '
                 'For HMAC: arbitrary length. For AES: 16, 24, or 32 bytes.'
        )

        parser.add_argument(
            '--input',
            help='Path to input file'
        )

        parser.add_argument(
            '--output',
            help='Path to output file (default: generated based on operation)'
        )

        # New syntax subparsers
        subparsers = parser.add_subparsers(dest='command', help='Command to execute')

        # 🆕 Subcommand for hash/HMAC operations
        dgst_parser = subparsers.add_parser('dgst', help='Compute hash or HMAC of a file')

        dgst_parser.add_argument(
            '--algorithm',
            required=True,
            choices=['sha256', 'sha3-256'],
            help='Hash algorithm (sha256, sha3-256)'
        )

        dgst_parser.add_argument(
            '--hmac',
            action='store_true',
            help='Enable HMAC mode (requires --key)'
        )

        dgst_parser.add_argument(
            '--key',
            help='Key for HMAC mode (hex string, arbitrary length). Required when --hmac is specified.'
        )

        dgst_parser.add_argument(
            '--input',
            required=True,
            help='Path to input file to be hashed'
        )

        dgst_parser.add_argument(
            '--output',
            help='Optional: write output to file instead of stdout'
        )

        dgst_parser.add_argument(
            '--verify',
            help='Optional: verify against existing hash/HMAC file'
        )

        # Subcommand for encryption/decryption (new syntax)
        encrypt_parser = subparsers.add_parser('encrypt', help='Encryption/decryption operations (new syntax)')

        encrypt_parser.add_argument(
            '--algorithm',
            required=True,
            choices=['aes'],
            help='Encryption algorithm (currently only aes supported)'
        )

        encrypt_parser.add_argument(
            '--mode',
            required=True,
            choices=['ecb', 'cbc', 'ctr', 'cfb', 'ofb'],
            help='Encryption mode (ecb, cbc, ctr, cfb, ofb)'
        )

        encrypt_op_group = encrypt_parser.add_mutually_exclusive_group(required=True)
        encrypt_op_group.add_argument(
            '--encrypt',
            action='store_true',
            help='Perform encryption operation'
        )

        encrypt_op_group.add_argument(
            '--decrypt',
            action='store_true',
            help='Perform decryption operation'
        )

        encrypt_parser.add_argument(
            '--key',
            help='Encryption key as hexadecimal string (16, 24, or 32 bytes for AES). '
                 'If omitted for encryption, a secure random key will be generated and displayed.'
        )

        encrypt_parser.add_argument(
            '--input',
            required=True,
            help='Path to input file'
        )

        encrypt_parser.add_argument(
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
        """Проверяем, используется ли старый синтаксис шифрования"""
        return (args.algorithm == 'aes' or
                (args.mode and args.mode in ['ecb', 'cbc', 'ctr', 'cfb', 'ofb']) or
                args.encrypt or
                args.decrypt)

    @staticmethod
    def validate_hex_key(key_str: str, for_hmac: bool = False) -> bytes:
        """
        Валидация и преобразование hex-ключа в байты

        Args:
            key_str: Key as hex string
            for_hmac: True if key is for HMAC (arbitrary length allowed)

        Returns:
            bytes: Key as bytes
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

        # Для HMAC: произвольная длина
        if for_hmac:
            try:
                return bytes.fromhex(key_str)
            except ValueError as e:
                raise ValueError(f"Invalid hex key: {e}")

        # Для AES: проверяем длину ключа
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
    def read_expected_hash(filename: str) -> str:
        """
        Read expected hash/HMAC from file

        Args:
            filename: Path to file containing expected hash

        Returns:
            str: Hash value (hex string)
        """
        try:
            with open(filename, 'r') as f:
                content = f.read().strip()

            # Parse format: HASH_VALUE FILENAME
            # We extract just the hash part
            parts = content.split()
            if not parts:
                raise ValueError("Empty hash file")

            # The hash is the first part (hex string)
            hash_value = parts[0].lower()

            # Validate it looks like a hex string
            if not all(c in '0123456789abcdef' for c in hash_value):
                raise ValueError(f"Invalid hash format in file: {hash_value}")

            return hash_value

        except FileNotFoundError:
            raise FileNotFoundError(f"Hash file not found: {filename}")
        except IOError as e:
            raise IOError(f"Error reading hash file {filename}: {e}")

    @staticmethod
    def process_dgst_operation(args):
        """
        Обработка операции хеширования/HMAC
        """
        try:
            # Проверка существования входного файла
            if not os.path.exists(args.input):
                raise FileNotFoundError(f"Input file not found: {args.input}")

            # Проверка HMAC режима
            if args.hmac:
                if not args.key:
                    raise ValueError("--key is required when --hmac is specified")

                # Валидация ключа для HMAC (произвольная длина)
                key_bytes = CryptoCoreCLI.validate_hex_key(args.key, for_hmac=True)

                # Выбор алгоритма хеширования для HMAC
                if args.algorithm == 'sha256':
                    # Используем нашу реализацию HMAC-SHA256
                    computed_value = hmac_sha256_file(key_bytes, args.input)
                    operation_type = "HMAC-SHA256"
                elif args.algorithm == 'sha3-256':
                    # Для SHA3-256 HMAC не реализован в требованиях
                    raise ValueError("HMAC with SHA3-256 is not supported in this sprint")
                else:
                    raise ValueError(f"Unsupported algorithm for HMAC: {args.algorithm}")
            else:
                # Обычное хеширование
                if args.algorithm == 'sha256':
                    computed_value = sha256_file(args.input)
                    operation_type = "SHA-256"
                elif args.algorithm == 'sha3-256':
                    computed_value = sha3_256_file(args.input)
                    operation_type = "SHA3-256"
                else:
                    raise ValueError(f"Unsupported hash algorithm: {args.algorithm}")

            # Проверка если указан --verify
            if args.verify:
                expected_value = CryptoCoreCLI.read_expected_hash(args.verify)

                if computed_value.lower() == expected_value.lower():
                    print(f"[OK] {operation_type} verification successful")
                    return True
                else:
                    print(f"[ERROR] {operation_type} verification failed", file=sys.stderr)
                    print(f"Computed: {computed_value}", file=sys.stderr)
                    print(f"Expected: {expected_value}", file=sys.stderr)
                    return False

            # Форматирование вывода
            if args.hmac:
                output_line = f"{computed_value}  {args.input}\n"
            else:
                output_line = f"{computed_value}  {args.input}\n"

            # Вывод результата
            if args.output:
                # Запись в файл
                with open(args.output, 'w') as f:
                    f.write(output_line)
                print(f"{operation_type} written to: {args.output}")
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
                    key_bytes = CryptoCoreCLI.validate_hex_key(args.key, for_hmac=False)
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
                key_bytes = CryptoCoreCLI.validate_hex_key(args.key, for_hmac=False)

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
            return CryptoCoreCLI.process_dgst_operation(args)
        elif args.command == 'encrypt':
            return CryptoCoreCLI.process_crypto_operation(args)
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
        else:
            # Если команда не указана, покажем помощь
            if not args.command:
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