from abc import ABC, abstractmethod
from Crypto.Cipher import AES


class BaseMode(ABC):
    BLOCK_SIZE = 16

    def __init__(self, key: bytes, iv: bytes):
        self.key = key
        self.iv = iv
        self._cipher = AES.new(key, AES.MODE_ECB)

    def _split_into_blocks(self, data: bytes, pad: bool = True) -> list:
        """Разделение данных на блоки"""
        if pad and len(data) % self.BLOCK_SIZE != 0:
            raise ValueError("Data must be padded to block size")

        return [data[i:i + self.BLOCK_SIZE]
                for i in range(0, len(data), self.BLOCK_SIZE)]

    def _encrypt_block(self, block: bytes) -> bytes:
        """Шифрование одного блока в ECB режиме"""
        return self._cipher.encrypt(block)

    def _decrypt_block(self, block: bytes) -> bytes:
        """Дешифрование одного блока в ECB режиме"""
        return self._cipher.decrypt(block)

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        """Абстрактный метод шифрования"""
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        """Абстрактный метод дешифрования"""
        pass