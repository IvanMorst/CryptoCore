import os
import struct
import hashlib
import time  # Добавлен импорт для измерения времени
from typing import List
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
import csprng  # 🆕 Импорт CSPRNG модуля

# Импорт для логирования
try:
    from crypto.crypto_logger import CryptoLogger

    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    print("Warning: CryptoLogger not available, logging disabled")


class CipherCore:
    BLOCK_SIZE = 16  # AES block size

    def __init__(self, key: bytes, mode: str = 'ecb'):
        """
        Инициализация cipher core

        Args:
            key: ключ шифрования (16, 24, или 32 байта для AES)
            mode: режим работы (ecb, cbc, ctr, cfb, ofb)
        """
        if len(key) not in [16, 24, 32]:
            error_msg = f"Key must be 16, 24, or 32 bytes for AES. Got {len(key)} bytes"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError(error_msg)

        self.key = key
        self.mode = mode.lower()

        # 🆕 Генерация IV для режимов, которые требуют его
        if self.mode in ['cbc', 'cfb', 'ofb', 'ctr']:
            self.iv = csprng.generate_iv(16)
        else:
            self.iv = None

        # Логирование инициализации
        if LOGGING_AVAILABLE:
            CryptoLogger.setup_logging()
            key_info = self.get_key_info()
            CryptoLogger.log_key_generation(key_info)
            CryptoLogger.log(f"CipherCore initialized: mode={mode}, key_size={len(key) * 8} bits")

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в выбранном режиме с PKCS7 паддингом"""
        # Логирование начала операции
        start_time = time.time()

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"Starting encryption: mode={self.mode}, "
                f"data_size={len(data)} bytes, "
                f"key={self.key.hex()[:16]}..."
            )

        # Выполнение шифрования
        if self.mode == 'ecb':
            result = self._encrypt_ecb(data)
        elif self.mode == 'cbc':
            result = self._encrypt_cbc(data)
        elif self.mode == 'ctr':
            result = self._encrypt_ctr(data)
        elif self.mode in ['cfb', 'ofb']:
            result = self._encrypt_stream(data)
        else:
            error_msg = f"Unsupported mode: {self.mode}"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError(error_msg)

        # Логирование завершения операции
        elapsed = time.time() - start_time

        if LOGGING_AVAILABLE:
            CryptoLogger.log_performance(f"Encryption ({self.mode})", len(data), start_time)
            CryptoLogger.log(
                f"Encryption completed: {len(data)} -> {len(result)} bytes "
                f"(overhead: {len(result) - len(data)} bytes)"
            )

        return result

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование данных в выбранном режиме"""
        # Логирование начала операции
        start_time = time.time()

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"Starting decryption: mode={self.mode}, "
                f"data_size={len(data)} bytes, "
                f"key={self.key.hex()[:16]}..."
            )

        # Выполнение дешифрования
        if self.mode == 'ecb':
            result = self._decrypt_ecb(data)
        elif self.mode == 'cbc':
            result = self._decrypt_cbc(data)
        elif self.mode == 'ctr':
            result = self._decrypt_ctr(data)
        elif self.mode in ['cfb', 'ofb']:
            result = self._decrypt_stream(data)
        else:
            error_msg = f"Unsupported mode: {self.mode}"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError(error_msg)

        # Логирование завершения операции
        elapsed = time.time() - start_time

        if LOGGING_AVAILABLE:
            CryptoLogger.log_performance(f"Decryption ({self.mode})", len(data), start_time)
            CryptoLogger.log(
                f"Decryption completed: {len(data)} -> {len(result)} bytes"
            )

        return result

    def _encrypt_ecb(self, data: bytes) -> bytes:
        """Шифрование в режиме ECB"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log("ECB encryption started")

        padded_data = pad(data, self.BLOCK_SIZE)
        cipher = AES.new(self.key, AES.MODE_ECB)
        result = cipher.encrypt(padded_data)

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"ECB padding added: {len(padded_data) - len(data)} bytes")

        return result

    def _decrypt_ecb(self, data: bytes) -> bytes:
        """Дешифрование в режиме ECB"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log("ECB decryption started")

        if len(data) % self.BLOCK_SIZE != 0:
            error_msg = f"Data length must be multiple of block size {self.BLOCK_SIZE}"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError(error_msg)

        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_padded = cipher.decrypt(data)
        result = unpad(decrypted_padded, self.BLOCK_SIZE)

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"ECB padding removed: {len(decrypted_padded) - len(result)} bytes")

        return result

    def _encrypt_cbc(self, data: bytes) -> bytes:
        """Шифрование в режиме CBC"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"CBC encryption started, IV={self.iv.hex()}")

        padded_data = pad(data, self.BLOCK_SIZE)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(padded_data)

        # 🆕 Prepending IV to ciphertext
        result = self.iv + encrypted

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"CBC encryption: IV={self.iv.hex()}, "
                f"padding={len(padded_data) - len(data)} bytes"
            )

        return result

    def _decrypt_cbc(self, data: bytes) -> bytes:
        """Дешифрование в режиме CBC"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log("CBC decryption started")

        if len(data) < self.BLOCK_SIZE:
            error_msg = "Ciphertext too short to contain IV"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError(error_msg)

        # 🆕 Extract IV from beginning of ciphertext
        iv = data[:self.BLOCK_SIZE]
        actual_ciphertext = data[self.BLOCK_SIZE:]

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"CBC decryption: extracted IV={iv.hex()}")

        if len(actual_ciphertext) % self.BLOCK_SIZE != 0:
            error_msg = f"Ciphertext length must be multiple of block size {self.BLOCK_SIZE}"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError(error_msg)

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(actual_ciphertext)
        result = unpad(decrypted_padded, self.BLOCK_SIZE)

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"CBC decryption: padding removed={len(decrypted_padded) - len(result)} bytes"
            )

        return result

    def _encrypt_ctr(self, data: bytes) -> bytes:
        """Шифрование в режиме CTR"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"CTR encryption started, nonce={self.iv.hex()}")

        # 🆕 Create a counter starting from random value
        counter = Counter.new(128, initial_value=int.from_bytes(self.iv, 'big'))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
        encrypted = cipher.encrypt(data)

        # 🆕 Prepending nonce to ciphertext
        result = self.iv + encrypted

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"CTR encryption: nonce={self.iv.hex()}")

        return result

    def _decrypt_ctr(self, data: bytes) -> bytes:
        """Дешифрование в режиме CTR"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log("CTR decryption started")

        if len(data) < self.BLOCK_SIZE:
            error_msg = "Ciphertext too short to contain nonce"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError("Ciphertext too short to contain nonce")

        # 🆕 Extract nonce from beginning of ciphertext
        nonce = data[:self.BLOCK_SIZE]
        actual_ciphertext = data[self.BLOCK_SIZE:]

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"CTR decryption: extracted nonce={nonce.hex()}")

        counter = Counter.new(128, initial_value=int.from_bytes(nonce, 'big'))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
        result = cipher.decrypt(actual_ciphertext)

        if LOGGING_AVAILABLE:
            CryptoLogger.log("CTR decryption completed")

        return result

    def _encrypt_stream(self, data: bytes) -> bytes:
        """Шифрование в потоковых режимах (CFB, OFB)"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"{self.mode.upper()} encryption started, IV={self.iv.hex()}"
            )

        if self.mode == 'cfb':
            cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
        else:  # ofb
            cipher = AES.new(self.key, AES.MODE_OFB, self.iv)

        encrypted = cipher.encrypt(data)

        # 🆕 Prepending IV to ciphertext
        result = self.iv + encrypted

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"{self.mode.upper()} encryption completed")

        return result

    def _decrypt_stream(self, data: bytes) -> bytes:
        """Дешифрование в потоковых режимах (CFB, OFB)"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"{self.mode.upper()} decryption started")

        if len(data) < self.BLOCK_SIZE:
            error_msg = "Ciphertext too short to contain IV"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError(error_msg)

        # 🆕 Extract IV from beginning of ciphertext
        iv = data[:self.BLOCK_SIZE]
        actual_ciphertext = data[self.BLOCK_SIZE:]

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"{self.mode.upper()} decryption: extracted IV={iv.hex()}")

        if self.mode == 'cfb':
            cipher = AES.new(self.key, AES.MODE_CFB, iv, segment_size=128)
        else:  # ofb
            cipher = AES.new(self.key, AES.MODE_OFB, iv)

        result = cipher.decrypt(actual_ciphertext)

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"{self.mode.upper()} decryption completed")

        return result

    def get_key_info(self) -> dict:
        """Информация о ключе"""
        info = {
            'length': len(self.key),
            'hex': self.key.hex(),
            'algorithm': 'AES',
            'key_size': len(self.key) * 8,  # в битах
            'mode': self.mode.upper(),
            'iv_used': self.iv is not None,
            'iv': self.iv.hex() if self.iv else None
        }

        # Логирование информации о ключе
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Key info: {info}")

        return info


# Convenience functions with logging
def create_cipher(key: bytes, mode: str = 'ecb') -> CipherCore:
    """Создание шифра с логированием"""
    if LOGGING_AVAILABLE:
        CryptoLogger.log(f"Creating cipher: mode={mode}, key_size={len(key)} bytes")

    return CipherCore(key, mode)


def encrypt_data(data: bytes, key: bytes, mode: str = 'ecb') -> bytes:
    """Удобная функция для шифрования данных"""
    if LOGGING_AVAILABLE:
        CryptoLogger.log(
            f"Quick encrypt: mode={mode}, "
            f"data_size={len(data)} bytes, "
            f"key_size={len(key)} bytes"
        )

    cipher = CipherCore(key, mode)
    return cipher.encrypt(data)


def decrypt_data(data: bytes, key: bytes, mode: str = 'ecb') -> bytes:
    """Удобная функция для дешифрования данных"""
    if LOGGING_AVAILABLE:
        CryptoLogger.log(
            f"Quick decrypt: mode={mode}, "
            f"data_size={len(data)} bytes, "
            f"key_size={len(key)} bytes"
        )

    cipher = CipherCore(key, mode)
    return cipher.decrypt(data)