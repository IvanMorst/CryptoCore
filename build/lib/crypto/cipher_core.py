import os
import struct
import hashlib
from typing import List
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class CipherCore:
    BLOCK_SIZE = 16  # AES block size

    def __init__(self, key: bytes):
        """
        Инициализация cipher core

        Args:
            key: ключ шифрования (16, 24, или 32 байта для AES)
        """
        if len(key) not in [16, 24, 32]:
            raise ValueError(
                f"Key must be 16, 24, or 32 bytes for AES. Got {len(key)} bytes"
            )
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в режиме ECB с PKCS7 паддингом"""
        # Добавляем PKCS7 паддинг
        padded_data = pad(data, self.BLOCK_SIZE)

        # Создаем AES cipher в режиме ECB
        cipher = AES.new(self.key, AES.MODE_ECB)

        # Шифруем
        encrypted = cipher.encrypt(padded_data)

        return encrypted

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование данных в режиме ECB с удалением PKCS7 паддинга"""
        if len(data) % self.BLOCK_SIZE != 0:
            raise ValueError(
                f"Data length ({len(data)}) must be multiple of block size ({self.BLOCK_SIZE})"
            )

        # Создаем AES cipher в режиме ECB
        cipher = AES.new(self.key, AES.MODE_ECB)

        # Дешифруем
        decrypted_padded = cipher.decrypt(data)

        # Удаляем паддинг
        decrypted = unpad(decrypted_padded, self.BLOCK_SIZE)

        return decrypted

    def get_key_info(self) -> dict:
        """Информация о ключе"""
        return {
            'length': len(self.key),
            'hex': self.key.hex(),
            'algorithm': 'AES',
            'key_size': len(self.key) * 8  # в битах
        }