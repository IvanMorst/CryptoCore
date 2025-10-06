import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class CipherCore:
    BLOCK_SIZE = 16  # AES block size

    def __init__(self, key: bytes):
        if len(key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes for AES")
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в режиме ECB с PKCS7 паддингом"""
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_data = pad(data, self.BLOCK_SIZE)
        return cipher.encrypt(padded_data)

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование данных в режиме ECB с удалением PKCS7 паддинга"""
        if len(data) % self.BLOCK_SIZE != 0:
            raise ValueError(f"Data length must be multiple of block size {self.BLOCK_SIZE}")

        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_padded = cipher.decrypt(data)
        return unpad(decrypted_padded, self.BLOCK_SIZE)