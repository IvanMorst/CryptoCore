#!/usr/bin/env python3
"""
CryptoCore CLI Tool
Командный интерфейс для криптографической системы с поддержкой AEAD (GCM) и KDF (Sprint 7)
"""

import argparse
import sys
import os
import tempfile
from pathlib import Path
import struct
import hashlib

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from crypto.file_processor import FileProcessor
from crypto.crypto_logger import CryptoLogger
from crypto.crypto_exception import CryptoException
from csprng import CSPRNG
from hash.sha256 import sha256_file
from hash.sha3_256 import sha3_256_file
from mac.hmac import hmac_sha256_file, verify_hmac_file
from crypto.aead.gcm import GCM, AuthenticationError
from crypto.kdf.pbkdf2 import pbkdf2_hmac_sha256, generate_salt  # 🆕 Импорт KDF функций
from crypto.kdf.key_hierarchy import derive_key as kh_derive_key  # 🆕 Импорт функции иерархии ключей


class CryptoCoreCLI:
    """Класс для обработки командной строки CryptoCore с поддержкой AEAD и KDF"""

    @staticmethod
    def create_parser():
        """Создание парсера аргументов с поддержкой GCM и KDF"""
        parser = argparse.ArgumentParser(
            description='CryptoCore - Cryptographic File Operations with AEAD and KDF Support',
            epilog='Examples:\n'
                   '  # Hash computation:\n'
                   '  cryptocore dgst --algorithm sha256 --input document.pdf\n\n'
                   '  # HMAC generation:\n'
                   '  cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt\n\n'
                   '  # GCM encryption with AAD:\n'
                   '  cryptocore encrypt --algorithm aes --mode gcm --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output ciphertext.bin --aad aabbccddeeff\n\n'
                   '  # Key derivation:\n'
                   '  cryptocore derive --password "MySecurePassword123!" --salt a1b2c3d4e5f601234567890123456789 --iterations 100000 --length 32\n\n'
                   '  # Key derivation with auto-generated salt:\n'
                   '  cryptocore derive --password "AnotherPassword" --iterations 500000 --length 16\n',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        # Old syntax arguments (for backward compatibility)
        parser.add_argument(
            '--algorithm',
            help='Encryption algorithm (aes) - for backward compatibility'
        )

        parser.add_argument(
            '--mode',
            help='Encryption mode (ecb, cbc, ctr, cfb, ofb, gcm) - for backward compatibility'
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

        # 🆕 AAD for GCM
        parser.add_argument(
            '--aad',
            help='Additional Authenticated Data (AAD) as hexadecimal string for GCM mode'
        )

        # 🆕 Nonce/IV for GCM (renamed for consistency but keeping iv for backward compatibility)
        parser.add_argument(
            '--iv',
            '--nonce',
            dest='nonce',
            help='Nonce/Initialization Vector as hexadecimal string (12 bytes for GCM)'
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

        # 🆕 Subcommand for encryption/decryption (new syntax) с поддержкой GCM
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
            choices=['ecb', 'cbc', 'ctr', 'cfb', 'ofb', 'gcm'],
            help='Encryption mode (ecb, cbc, ctr, cfb, ofb, gcm)'
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

        # 🆕 GCM-specific arguments
        encrypt_parser.add_argument(
            '--aad',
            help='Additional Authenticated Data (AAD) as hexadecimal string (for GCM mode only)'
        )

        encrypt_parser.add_argument(
            '--nonce',
            '--iv',
            dest='nonce',
            help='Nonce/Initialization Vector as hexadecimal string (12 bytes for GCM)'
        )

        # 🆕 Subcommand for key derivation (Sprint 7)
        derive_parser = subparsers.add_parser('derive', help='Key derivation operations (Sprint 7)')

        derive_parser.add_argument(
            '--password',
            required=True,
            help='Password for key derivation'
        )

        derive_parser.add_argument(
            '--salt',
            help='Salt as hexadecimal string (16+ bytes). If not provided, random salt will be generated.'
        )

        derive_parser.add_argument(
            '--iterations',
            type=int,
            default=100000,
            help='Number of iterations (default: 100000)'
        )

        derive_parser.add_argument(
            '--length',
            type=int,
            default=32,
            help='Key length in bytes (default: 32)'
        )

        derive_parser.add_argument(
            '--algorithm',
            choices=['pbkdf2'],
            default='pbkdf2',
            help='KDF algorithm (currently only pbkdf2)'
        )

        derive_parser.add_argument(
            '--output',
            help='Optional: write derived key to file (binary format)'
        )

        derive_parser.add_argument(
            '--context',
            help='Optional: context for key hierarchy derivation'
        )

        derive_parser.add_argument(
            '--master-key',
            help='Optional: master key (hex) for key hierarchy derivation'
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
                (args.mode and args.mode in ['ecb', 'cbc', 'ctr', 'cfb', 'ofb', 'gcm']) or
                args.encrypt or
                args.decrypt)

    @staticmethod
    def validate_hex_key(key_str: str, for_hmac: bool = False, min_length: int = None) -> bytes:
        """
        Валидация и преобразование hex-ключа в байты

        Args:
            key_str: Key as hex string
            for_hmac: True if key is for HMAC (arbitrary length allowed)
            min_length: Minimum length in bytes (for GCM nonce)

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
                key_bytes = bytes.fromhex(key_str)
                if min_length and len(key_bytes) < min_length:
                    raise ValueError(f"Key must be at least {min_length} bytes for GCM mode")
                return key_bytes
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
            if input_path.suffix == '.dec':
                return str(input_path.with_suffix(''))
            else:
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
        Обработка криптографической операции с поддержкой AEAD
        """
        try:
            # 🆕 Обработка AAD для GCM
            aad_bytes = b""
            if hasattr(args, 'aad') and args.aad:
                aad_bytes = CryptoCoreCLI.validate_hex_key(args.aad, for_hmac=True)
                if args.mode != 'gcm':
                    print(f"Warning: --aad is only used with GCM mode, ignoring for {args.mode} mode",
                          file=sys.stderr)

            # 🆕 Обработка nonce/IV
            nonce_bytes = None
            if hasattr(args, 'nonce') and args.nonce:
                nonce_bytes = CryptoCoreCLI.validate_hex_key(args.nonce, for_hmac=True)
                if args.mode == 'gcm' and len(nonce_bytes) != 12:
                    print(f"Warning: GCM typically uses 12-byte nonce, got {len(nonce_bytes)} bytes",
                          file=sys.stderr)

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
                CryptoCoreCLI.encrypt_file(args.input, output_path, key_bytes,
                                           crypto_mode, aad_bytes, nonce_bytes)
            else:
                CryptoCoreCLI.decrypt_file(args.input, output_path, key_bytes,
                                           crypto_mode, aad_bytes, nonce_bytes)

            return True

        except AuthenticationError as e:
            print(f"[ERROR] Authentication failed: {e}", file=sys.stderr)
            # Удалить частично созданный файл
            if 'output_path' in locals() and output_path and os.path.exists(output_path):
                os.remove(output_path)
            return False
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return False

    @staticmethod
    def process_derive_operation(args):
        """
        Обработка операции вывода ключей (Sprint 7)

        Args:
            args: Парсированные аргументы командной строки

        Returns:
            bool: True если операция успешна
        """
        try:
            # Валидация параметров
            if args.iterations <= 0:
                raise ValueError("Iterations must be positive")
            if args.length <= 0:
                raise ValueError("Key length must be positive")
            if args.length > (2 ** 32 - 1) * 32:  # Ограничение PBKDF2
                raise ValueError(f"Key length too large: maximum is {(2 ** 32 - 1) * 32} bytes")

            # Логирование начала операции
            CryptoLogger.setup_logging()
            CryptoLogger.log(
                f"Key derivation started: algorithm={args.algorithm}, "
                f"iterations={args.iterations}, "
                f"length={args.length} bytes"
            )

            # Обработка пароля
            password = args.password.encode('utf-8')

            # Логирование информации о пароле (без самого пароля)
            CryptoLogger.log(f"Password length: {len(password)} characters")

            # Обработка соли
            salt_bytes = None
            if args.salt:
                # Валидация hex-строки соли
                salt_str = args.salt.strip().lower()
                if not all(c in '0123456789abcdef' for c in salt_str):
                    raise ValueError("Salt must be a valid hexadecimal string")

                # Проверка минимальной длины соли
                if len(salt_str) < 32:  # Минимум 16 байт в hex
                    print(f"Warning: Salt is short ({len(salt_str) // 2} bytes), "
                          f"recommended minimum is 16 bytes",
                          file=sys.stderr)

                salt_bytes = bytes.fromhex(salt_str)
                CryptoLogger.log(f"Using provided salt: {len(salt_bytes)} bytes")
            else:
                # Генерация случайной соли
                salt_bytes = generate_salt(16)
                print(f"Generated salt: {salt_bytes.hex()}")
                CryptoLogger.log(f"Generated random salt: {len(salt_bytes)} bytes")

            # Вывод ключа в зависимости от алгоритма
            derived_key = None

            if args.algorithm == 'pbkdf2':
                if args.master_key:
                    print("Warning: --master-key is ignored for PBKDF2 algorithm",
                          file=sys.stderr)

                if args.context:
                    print("Warning: --context is ignored for PBKDF2 algorithm",
                          file=sys.stderr)

                # Вывод ключа с использованием PBKDF2
                CryptoLogger.log(
                    f"Starting PBKDF2-HMAC-SHA256 derivation: "
                    f"password_len={len(password)}, "
                    f"salt_len={len(salt_bytes)}, "
                    f"iterations={args.iterations}"
                )

                derived_key = pbkdf2_hmac_sha256(
                    password,
                    salt_bytes,
                    args.iterations,
                    args.length
                )

                CryptoLogger.log(
                    f"PBKDF2 key derived successfully: "
                    f"key_length={len(derived_key)} bytes"
                )

            else:
                raise ValueError(f"Unsupported KDF algorithm: {args.algorithm}")

            # Запись ключа в файл, если указан --output
            if args.output:
                try:
                    with open(args.output, 'wb') as f:
                        f.write(derived_key)

                    print(f"Key written to: {args.output} ({len(derived_key)} bytes)")
                    CryptoLogger.log(
                        f"Derived key written to file: {args.output}, "
                        f"size={len(derived_key)} bytes"
                    )

                    # Вычисление хеша ключа для логирования
                    key_hash = hashlib.sha256(derived_key).hexdigest()[:16]
                    CryptoLogger.log(f"Key SHA-256 (first 16 chars): {key_hash}")

                except IOError as e:
                    error_msg = f"Failed to write key to file: {e}"
                    CryptoLogger.log(error_msg, is_error=True)
                    raise ValueError(error_msg)

            # Вывод результата в stdout: KEY_HEX SALT_HEX
            print(f"{derived_key.hex()} {salt_bytes.hex()}")

            # Безопасная очистка пароля из памяти
            # Заполняем память нулями вместо простого удаления ссылки
            password_array = bytearray(password)
            for i in range(len(password_array)):
                password_array[i] = 0
            password = bytes(password_array)

            CryptoLogger.log("Key derivation completed successfully")

            return True

        except ValueError as e:
            error_msg = f"Validation error: {e}"
            CryptoLogger.log(error_msg, is_error=True)
            print(f"Error: {e}", file=sys.stderr)
            return False
        except Exception as e:
            error_msg = f"Unexpected error during key derivation: {e}"
            CryptoLogger.log(error_msg, is_error=True)
            print(f"Error: {e}", file=sys.stderr)
            return False

    @staticmethod
    def encrypt_file(input_path: str, output_path: str, key: bytes, mode: str,
                     aad: bytes = b"", nonce: bytes = None):
        """
        Шифрование файла с поддержкой GCM

        Args:
            input_path: Path to input file
            output_path: Path to output file
            key: Encryption key
            mode: Encryption mode
            aad: Additional Authenticated Data (for GCM)
            nonce: Nonce/IV (optional, generated if None)
        """
        # 🆕 Специальная обработка для GCM
        if mode == 'gcm':
            CryptoCoreCLI.encrypt_file_gcm(input_path, output_path, key, aad, nonce)
            return

        # Стандартное шифрование для других режимов
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
        if aad:
            print(f"AAD (ignored for {mode}): {aad.hex()}")
        print(f"Original size: {len(plaintext)} bytes")
        print(f"Encrypted size: {len(encrypted)} bytes")

    @staticmethod
    def decrypt_file(input_path: str, output_path: str, key: bytes, mode: str,
                     aad: bytes = b"", nonce: bytes = None):
        """
        Дешифрование файла с поддержкой GCM

        Args:
            input_path: Path to input file
            output_path: Path to output file
            key: Encryption key
            mode: Encryption mode
            aad: Additional Authenticated Data (for GCM)
            nonce: Nonce/IV (optional, read from file if None)
        """
        # 🆕 Специальная обработка для GCM
        if mode == 'gcm':
            CryptoCoreCLI.decrypt_file_gcm(input_path, output_path, key, aad, nonce)
            return

        # Стандартное дешифрование для других режимов
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
        if aad:
            print(f"AAD (ignored for {mode}): {aad.hex()}")
        print(f"Encrypted size: {len(ciphertext)} bytes")
        print(f"Decrypted size: {len(decrypted)} bytes")

    @staticmethod
    def encrypt_file_gcm(input_path: str, output_path: str, key: bytes,
                         aad: bytes = b"", nonce: bytes = None):
        """
        GCM encryption with AAD support

        Args:
            input_path: Path to input file
            output_path: Path to output file
            key: Encryption key (16, 24, or 32 bytes)
            aad: Additional Authenticated Data
            nonce: Nonce (12 bytes, generated if None)
        """
        # Validate key length for GCM
        if len(key) not in [16, 24, 32]:
            raise ValueError(f"Key must be 16, 24, or 32 bytes for GCM. Got {len(key)} bytes")

        # Read input file
        with open(input_path, 'rb') as f:
            plaintext = f.read()

        # Encrypt with GCM
        gcm = GCM(key, nonce)
        encrypted = gcm.encrypt(plaintext, aad)

        # Write output
        with open(output_path, 'wb') as f:
            f.write(encrypted)

        print(f"GCM encryption successful: {input_path} -> {output_path}")
        print(f"Key: {key.hex()}")
        print(f"Nonce: {gcm.nonce.hex()}")
        print(f"AAD: {aad.hex() if aad else 'None'}")
        print(f"Original size: {len(plaintext)} bytes")
        print(f"Encrypted size: {len(encrypted)} bytes")
        print(f"Tag size: 16 bytes")
        print(f"Structure: 12B nonce + {len(encrypted) - 28}B ciphertext + 16B tag")

    @staticmethod
    def decrypt_file_gcm(input_path: str, output_path: str, key: bytes,
                         aad: bytes = b"", nonce: bytes = None):
        """
        GCM decryption with authentication

        Args:
            input_path: Path to input file
            output_path: Path to output file
            key: Encryption key
            aad: Additional Authenticated Data
            nonce: Nonce (if provided, uses this instead of reading from file)
        """
        # Validate key length for GCM
        if len(key) not in [16, 24, 32]:
            raise ValueError(f"Key must be 16, 24, or 32 bytes for GCM. Got {len(key)} bytes")

        try:
            # Read encrypted file
            with open(input_path, 'rb') as f:
                encrypted = f.read()

            # Check minimum length (12B nonce + 0B ciphertext + 16B tag = 28B)
            if len(encrypted) < 28:
                raise ValueError(f"GCM file too short: {len(encrypted)} bytes (minimum 28 bytes)")

            if nonce:
                # Use provided nonce (for testing with NIST vectors)
                gcm = GCM(key, nonce)
                decrypted = gcm.decrypt(encrypted, aad)
                actual_nonce = nonce
            else:
                # Nonce is embedded in the file (first 12 bytes)
                # Extract nonce from file
                file_nonce = encrypted[:12]
                gcm = GCM(key, file_nonce)
                # Decrypt (nonce будет извлечен из данных внутри метода decrypt)
                decrypted = gcm.decrypt(encrypted, aad)
                actual_nonce = file_nonce

            # Write output only if authentication succeeded
            with open(output_path, 'wb') as f:
                f.write(decrypted)

            print(f"GCM decryption successful: {input_path} -> {output_path}")
            print(f"Key: {key.hex()}")
            print(f"Nonce: {actual_nonce.hex()}")
            print(f"AAD: {aad.hex() if aad else 'None'}")
            print(f"Encrypted size: {len(encrypted)} bytes")
            print(f"Decrypted size: {len(decrypted)} bytes")

        except AuthenticationError as e:
            # Delete output file if it was partially created
            if os.path.exists(output_path):
                os.remove(output_path)
            raise AuthenticationError(f"GCM authentication failed: {e}")
        except Exception as e:
            # Clean up on any error
            if os.path.exists(output_path):
                os.remove(output_path)
            raise e

    @staticmethod
    def process_operation(args):
        """
        Основной обработчик операций
        """
        if args.command == 'dgst':
            return CryptoCoreCLI.process_dgst_operation(args)
        elif args.command == 'encrypt':
            return CryptoCoreCLI.process_crypto_operation(args)
        elif args.command == 'derive':
            return CryptoCoreCLI.process_derive_operation(args)
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
        # Инициализация логирования
        CryptoLogger.setup_logging()
        CryptoLogger.log("CryptoCore CLI started with KDF support (Sprint 7)")

        # Парсинг аргументов
        args = CryptoCoreCLI.parse_arguments()

        # Логирование аргументов (без паролей для безопасности)
        args_dict = vars(args).copy()
        if 'password' in args_dict and args_dict['password']:
            args_dict['password'] = '***'  # Маскируем пароль в логах
        CryptoLogger.log(f"CLI arguments: {args_dict}")

        # Обработка операции
        success = CryptoCoreCLI.process_operation(args)

        if success:
            CryptoLogger.log("CLI operation completed successfully")
        else:
            CryptoLogger.log("CLI operation failed", is_error=True)

        # Возвращаем код выхода
        sys.exit(0 if success else 1)

    except AuthenticationError as e:
        error_msg = f"Authentication error: {e}"
        CryptoLogger.log(error_msg, is_error=True)
        print(f"[AUTH ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        CryptoLogger.log("Operation cancelled by user", is_error=True)
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_msg = f"Fatal error: {e}"
        CryptoLogger.log(error_msg, is_error=True)
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()