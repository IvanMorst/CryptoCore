import os
import time
import hashlib
import psutil
from typing import Optional


class Generator:
    @staticmethod
    def generate_random_bytes(num_bytes: int) -> bytes:
        """Генерация криптографически безопасных случайных байтов"""
        return Generator.generate_random_bits(num_bytes * 8)

    @staticmethod
    def generate_random_bits(num_bits: int) -> bytes:
        """Генерация случайных битов с использованием энтропии системы"""
        random_bits = bytearray(num_bits // 8)

        free_memory = psutil.virtual_memory().available
        time_entropy = time.time_ns()

        count = 0
        bits_generated = 0
        byte_index = 0
        bit_index = 0

        while bits_generated < num_bits:
            if count == 1000:
                free_memory = psutil.virtual_memory().available
                time_entropy = time.time_ns()
                count = 0

            entropy = free_memory ^ time_entropy * count
            hash_result = Generator._hash(str(entropy))

            for i in range(8):
                if bits_generated >= num_bits:
                    break

                bit = (hash_result[i] & 0xFF) % 2
                random_bits[byte_index] |= (bit << (7 - bit_index))

                bits_generated += 1
                count += 1
                bit_index += 1

                if bit_index == 8:
                    byte_index += 1
                    bit_index = 0

        return bytes(random_bits)

    @staticmethod
    def _hash(input_str: str) -> bytes:
        """Хеширование строки с использованием SHA-1"""
        return hashlib.sha1(input_str.encode()).digest()

    @staticmethod
    def generate_test_file(path: str, size: int):
        """Генерация тестового файла со случайными данными"""
        start_time = time.time()

        with open(path, 'wb') as f:
            remaining = size
            while remaining > 0:
                chunk_size = min(remaining, 8192)
                random_data = Generator.generate_random_bytes(chunk_size)
                f.write(random_data)
                remaining -= chunk_size

        elapsed = time.time() - start_time
        speed = (size * 8) / elapsed / 1e6  # Mbps

        from .crypto_logger import CryptoLogger
        CryptoLogger.log(
            f"Generated test file: {path} "
            f"(size: {size} bytes, speed: {speed:.2f} Mbps)",
            False
        )