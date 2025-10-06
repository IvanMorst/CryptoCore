import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from .key_generator import KeyGenerator
from .crypto_logger import CryptoLogger


class CryptoCore:
    BLOCK_SIZE = 16  # AES block size

    def __init__(self, password: str, salt: bytes = None):
        """
        Инициализация криптоядра с кастомной генерацией ключей
        :param password: пароль для генерации ключа
        :param salt: соль (если None - генерируется автоматически)
        """
        if salt is None:
            self.salt = KeyGenerator.generate_salt()
        else:
            self.salt = salt

        # Генерируем ключ с помощью кастомного генератора
        self.key = KeyGenerator.derive_key(password, self.salt)

        CryptoLogger.log(
            f"Key generated: salt={self.salt.hex()}, key_length={len(self.key)}",
            False
        )

    def get_salt(self) -> bytes:
        """Получить соль"""
        return self.salt

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

    @staticmethod
    def create_with_existing_salt(password: str, salt: bytes):
        """Создать экземпляр с существующей солью"""
        return CryptoCore(password, salt)