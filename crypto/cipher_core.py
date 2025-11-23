import os
import struct
import hashlib
from typing import List
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
import csprng  # 🆕 Импорт CSPRNG модуля


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
            raise ValueError(
                f"Key must be 16, 24, or 32 bytes for AES. Got {len(key)} bytes"
            )
        self.key = key
        self.mode = mode.lower()

        # 🆕 Генерация IV для режимов, которые требуют его
        if self.mode in ['cbc', 'cfb', 'ofb', 'ctr']:
            self.iv = csprng.generate_iv(16)
        else:
            self.iv = None

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в выбранном режиме с PKCS7 паддингом"""
        if self.mode == 'ecb':
            return self._encrypt_ecb(data)
        elif self.mode == 'cbc':
            return self._encrypt_cbc(data)
        elif self.mode == 'ctr':
            return self._encrypt_ctr(data)
        elif self.mode in ['cfb', 'ofb']:
            return self._encrypt_stream(data)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование данных в выбранном режиме"""
        if self.mode == 'ecb':
            return self._decrypt_ecb(data)
        elif self.mode == 'cbc':
            return self._decrypt_cbc(data)
        elif self.mode == 'ctr':
            return self._decrypt_ctr(data)
        elif self.mode in ['cfb', 'ofb']:
            return self._decrypt_stream(data)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def _encrypt_ecb(self, data: bytes) -> bytes:
        """Шифрование в режиме ECB"""
        padded_data = pad(data, self.BLOCK_SIZE)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(padded_data)

    def _decrypt_ecb(self, data: bytes) -> bytes:
        """Дешифрование в режиме ECB"""
        if len(data) % self.BLOCK_SIZE != 0:
            raise ValueError(f"Data length must be multiple of block size {self.BLOCK_SIZE}")

        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_padded = cipher.decrypt(data)
        return unpad(decrypted_padded, self.BLOCK_SIZE)

    def _encrypt_cbc(self, data: bytes) -> bytes:
        """Шифрование в режиме CBC"""
        padded_data = pad(data, self.BLOCK_SIZE)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(padded_data)
        return self.iv + encrypted  # 🆕 Prepending IV to ciphertext

    def _decrypt_cbc(self, data: bytes) -> bytes:
        """Дешифрование в режиме CBC"""
        if len(data) < self.BLOCK_SIZE:
            raise ValueError("Ciphertext too short to contain IV")

        # 🆕 Extract IV from beginning of ciphertext
        iv = data[:self.BLOCK_SIZE]
        actual_ciphertext = data[self.BLOCK_SIZE:]

        if len(actual_ciphertext) % self.BLOCK_SIZE != 0:
            raise ValueError(f"Ciphertext length must be multiple of block size {self.BLOCK_SIZE}")

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(actual_ciphertext)
        return unpad(decrypted_padded, self.BLOCK_SIZE)

    def _encrypt_ctr(self, data: bytes) -> bytes:
        """Шифрование в режиме CTR"""
        # 🆕 Create a counter starting from random value
        counter = Counter.new(128, initial_value=int.from_bytes(self.iv, 'big'))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
        encrypted = cipher.encrypt(data)
        return self.iv + encrypted  # 🆕 Prepending nonce to ciphertext

    def _decrypt_ctr(self, data: bytes) -> bytes:
        """Дешифрование в режиме CTR"""
        if len(data) < self.BLOCK_SIZE:
            raise ValueError("Ciphertext too short to contain nonce")

        # 🆕 Extract nonce from beginning of ciphertext
        nonce = data[:self.BLOCK_SIZE]
        actual_ciphertext = data[self.BLOCK_SIZE:]

        counter = Counter.new(128, initial_value=int.from_bytes(nonce, 'big'))
        cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
        return cipher.decrypt(actual_ciphertext)

    def _encrypt_stream(self, data: bytes) -> bytes:
        """Шифрование в потоковых режимах (CFB, OFB)"""
        if self.mode == 'cfb':
            cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
        else:  # ofb
            cipher = AES.new(self.key, AES.MODE_OFB, self.iv)

        encrypted = cipher.encrypt(data)
        return self.iv + encrypted  # 🆕 Prepending IV to ciphertext

    def _decrypt_stream(self, data: bytes) -> bytes:
        """Дешифрование в потоковых режимах (CFB, OFB)"""
        if len(data) < self.BLOCK_SIZE:
            raise ValueError("Ciphertext too short to contain IV")

        # 🆕 Extract IV from beginning of ciphertext
        iv = data[:self.BLOCK_SIZE]
        actual_ciphertext = data[self.BLOCK_SIZE:]

        if self.mode == 'cfb':
            cipher = AES.new(self.key, AES.MODE_CFB, iv, segment_size=128)
        else:  # ofb
            cipher = AES.new(self.key, AES.MODE_OFB, iv)

        return cipher.decrypt(actual_ciphertext)

    def get_key_info(self) -> dict:
        """Информация о ключе"""
        return {
            'length': len(self.key),
            'hex': self.key.hex(),
            'algorithm': 'AES',
            'key_size': len(self.key) * 8,  # в битах
            'mode': self.mode.upper(),
            'iv_used': self.iv is not None,
            'iv': self.iv.hex() if self.iv else None
        }