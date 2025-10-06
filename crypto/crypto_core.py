import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from .key_generator import KeyGenerator
from .crypto_logger import CryptoLogger

# !/usr/bin/env python3
"""
CryptoCore CLI Tool
Командный интерфейс для криптографической системы с поддержкой разных режимов
"""

import argparse
import sys
import os
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from crypto.file_processor import FileProcessor
from crypto.crypto_logger import CryptoLogger


class CryptoCoreCLI:
    """Класс для обработки командной строки CryptoCore с поддержкой новых режимов"""

    @staticmethod
    def parse_arguments():
        """Парсинг аргументов командной строки с поддержкой новых режимов"""
        parser = argparse.ArgumentParser(
            description='CryptoCore - Cryptographic File Encryption/Decryption Tool',
            epilog='Examples:\n'
                   '  Encryption with CBC mode:\n'
                   '    cryptocore --algorithm aes --mode cbc --encrypt \\\n'
                   '               --key 00112233445566778899aabbccddeeff \\\n'
                   '               --input plaintext.txt --output ciphertext.bin\n\n'
                   '  Decryption with CBC mode and explicit IV:\n'
                   '    cryptocore --algorithm aes --mode cbc --decrypt \\\n'
                   '               --key 00112233445566778899aabbccddeeff \\\n'
                   '               --iv AABBCCDDEEFF00112233445566778899 \\\n'
                   '               --input ciphertext.bin --output decrypted.txt',
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
            choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'],
            help='Encryption mode'
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

        parser.add_argument(
            '--iv',
            help='Initialization vector as hexadecimal string (for decryption only)'
        )

        return parser.parse_args()

    @staticmethod
    def validate_hex_key(key_str: str) -> bytes:
        """
        Валидация и преобразование hex-ключа в байты
        """
        key_str = key_str.lower().strip().replace(' ', '').replace(':', '')

        if key_str.startswith('0x'):
            key_str = key_str[2:]

        if not all(c in '0123456789abcdef' for c in key_str):
            raise ValueError("Key must be a valid hexadecimal string")

        key_length = len(key_str)
        if key_length not in [32, 48, 64]:
            raise ValueError(
                f"Key must be 16, 24, or 32 bytes (got {key_length // 2} bytes). "
                f"Hex string length should be 32, 48, or 64 characters"
            )

        try:
            return bytes.fromhex(key_str)
        except ValueError as e:
            raise ValueError(f"Invalid hex key: {e}")

    @staticmethod
    def validate_hex_iv(iv_str: str) -> bytes:
        """
        Валидация и преобразование hex-IV в байты
        """
        if iv_str is None:
            return None

        iv_str = iv_str.lower().strip().replace(' ', '').replace(':', '')

        if iv_str.startswith('0x'):
            iv_str = iv_str[2:]

        if not all(c in '0123456789abcdef' for c in iv_str):
            raise ValueError("IV must be a valid hexadecimal string")

        iv_length = len(iv_str)
        if iv_length != 32:
            raise ValueError(
                f"IV must be 16 bytes (got {iv_length // 2} bytes). "
                f"Hex string length should be 32 characters"
            )

        try:
            return bytes.fromhex(iv_str)
        except ValueError as e:
            raise ValueError(f"Invalid hex IV: {e}")

    @staticmethod
    def generate_default_output_path(input_path: str, encrypt: bool, mode: str) -> str:
        """
        Генерация пути выходного файла по умолчанию
        """
        input_path = Path(input_path)

        if encrypt:
            suffix = f'.{mode}.enc'
        else:
            # Убираем .enc и добавляем .dec
            name = input_path.stem
            if name.endswith(f'.{mode}.enc'):
                name = name[:-len(f'.{mode}.enc')]
            suffix = '.dec'

        return str(input_path.with_name(input_path.stem + suffix))

    @staticmethod
    def process_operation(args):
        """
        Обработка криптографической операции с поддержкой новых режимов
        """
        try:
            # Валидация ключа
            key_bytes = CryptoCoreCLI.validate_hex_key(args.key)

            # Валидация IV
            iv_bytes = None
            if args.iv:
                if args.encrypt:
                    print("Warning: IV provided for encryption will be ignored",
                          file=sys.stderr)
                else:
                    iv_bytes = CryptoCoreCLI.validate_hex_iv(args.iv)

            # Генерация выходного файла если не указан
            output_path = args.output
            if not output_path:
                output_path = CryptoCoreCLI.generate_default_output_path(
                    args.input, args.encrypt, args.mode
                )
                print(f"Output file not specified. Using default: {output_path}")

            # Проверка существования входного файла
            if not os.path.exists(args.input):
                raise FileNotFoundError(f"Input file not found: {args.input}")

            # Проверка что выходной файл не совпадает с входным
            if os.path.abspath(args.input) == os.path.abspath(output_path):
                raise ValueError("Input and output files cannot be the same")

            # Выполнение операции
            FileProcessor.process_file(
                input_path=args.input,
                output_path=output_path,
                key=key_bytes,
                mode=args.mode,
                encrypt=args.encrypt,
                iv=iv_bytes
            )

            print(f"Operation successful: {args.input} -> {output_path}")
            print(f"Mode: {args.mode}, Key: {args.key}")
            if iv_bytes and args.decrypt:
                print(f"IV used: {iv_bytes.hex()}")

            return True

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return False


def main():
    """Главная функция CLI"""
    try:
        CryptoLogger.setup_logging()
        args = CryptoCoreCLI.parse_arguments()
        success = CryptoCoreCLI.process_operation(args)
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()