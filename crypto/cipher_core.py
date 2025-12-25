import os
import struct
import hashlib
import time
from typing import List
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
import csprng

try:
    from crypto.crypto_logger import CryptoLogger

    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    print("Warning: CryptoLogger not available, logging disabled")


class CipherCore:
    BLOCK_SIZE = 16  # AES block size

    def __init__(self, key: bytes, mode: str = 'ecb', iv: bytes = None):
        if len(key) not in [16, 24, 32]:
            error_msg = f"Key must be 16, 24, or 32 bytes for AES. Got {len(key)} bytes"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError(error_msg)

        self.key = key
        self.mode = mode.lower()

        # Инициализация IV
        if self.mode == 'ecb':
            self.iv = None
        else:
            if iv:
                self.iv = iv
            else:
                self.iv = csprng.generate_iv(16)

        # 🆕 Для ECB/CBC: буфер для неполных блоков при потоковой обработке
        self._encrypt_buffer = b''
        self._decrypt_buffer = b''

        # 🆕 Флаг для отслеживания первого вызова дешифрования в CBC
        self._first_decrypt_call = True

        if LOGGING_AVAILABLE:
            CryptoLogger.setup_logging()
            CryptoLogger.log(f"CipherCore initialized: mode={mode}, key_size={len(key) * 8} bits")

    def _process_ecb_chunk(self, data: bytes, encrypt: bool, is_final: bool = True) -> bytes:
        """Обработка чанка в режиме ECB с учетом паддинга"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"ECB processing: encrypt={encrypt}, len={len(data)}, is_final={is_final}")

        if encrypt:
            if is_final:
                # Последний чанк - применяем паддинг
                padded_data = pad(data, self.BLOCK_SIZE)
                cipher = AES.new(self.key, AES.MODE_ECB)
                return cipher.encrypt(padded_data)
            else:
                # Промежуточный чанк - должен быть кратен BLOCK_SIZE
                if len(data) % self.BLOCK_SIZE != 0:
                    # Дополняем нулями до кратности
                    padding_len = self.BLOCK_SIZE - (len(data) % self.BLOCK_SIZE)
                    data = data + b'\x00' * padding_len
                cipher = AES.new(self.key, AES.MODE_ECB)
                return cipher.encrypt(data)
        else:
            # Дешифрование
            cipher = AES.new(self.key, AES.MODE_ECB)
            decrypted = cipher.decrypt(data)

            if is_final:
                # Последний чанк - удаляем паддинг
                return unpad(decrypted, self.BLOCK_SIZE)
            else:
                # Промежуточный чанк - удаляем нулевое дополнение
                # Удаляем нули с конца, но осторожно
                while decrypted and decrypted[-1] == 0:
                    decrypted = decrypted[:-1]
                return decrypted

    def _process_cbc_chunk(self, data: bytes, encrypt: bool, is_final: bool = True) -> bytes:
        """Обработка чанка в режиме CBC"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"CBC processing: encrypt={encrypt}, len={len(data)}, is_final={is_final}")

        if encrypt:
            if is_final:
                # Последний чанк - применяем паддинг
                padded_data = pad(data, self.BLOCK_SIZE)
                cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
                encrypted = cipher.encrypt(padded_data)
                # Сохраняем последний блок для следующего чанка
                self.iv = encrypted[-self.BLOCK_SIZE:] if len(encrypted) >= self.BLOCK_SIZE else self.iv
                return encrypted
            else:
                # Промежуточный чанк - должен быть кратен BLOCK_SIZE
                if len(data) % self.BLOCK_SIZE != 0:
                    padding_len = self.BLOCK_SIZE - (len(data) % self.BLOCK_SIZE)
                    data = data + b'\x00' * padding_len

                cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
                encrypted = cipher.encrypt(data)
                # Сохраняем последний блок для следующего чанка
                self.iv = encrypted[-self.BLOCK_SIZE:] if len(encrypted) >= self.BLOCK_SIZE else self.iv
                return encrypted
        else:
            # Дешифрование CBC
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted = cipher.decrypt(data)

            # Сохраняем текущий зашифрованный блок как IV для следующего
            self.iv = data[-self.BLOCK_SIZE:] if len(data) >= self.BLOCK_SIZE else self.iv

            if is_final:
                # Последний чанк - удаляем паддинг
                return unpad(decrypted, self.BLOCK_SIZE)
            else:
                # Промежуточный чанк - удаляем нулевое дополнение
                while decrypted and decrypted[-1] == 0:
                    decrypted = decrypted[:-1]
                return decrypted

    def encrypt_chunk(self, data: bytes, is_final: bool = True) -> bytes:
        """Шифрование чанка данных"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Encrypting chunk: {len(data)} bytes, mode={self.mode}, is_final={is_final}")

        if self.mode == 'ecb':
            return self._process_ecb_chunk(data, encrypt=True, is_final=is_final)
        elif self.mode == 'cbc':
            return self._process_cbc_chunk(data, encrypt=True, is_final=is_final)
        elif self.mode == 'cfb':
            cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
            return cipher.encrypt(data)
        elif self.mode == 'ofb':
            cipher = AES.new(self.key, AES.MODE_OFB, self.iv)
            return cipher.encrypt(data)
        elif self.mode == 'ctr':
            counter = Counter.new(128, initial_value=int.from_bytes(self.iv, 'big'))
            cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
            return cipher.encrypt(data)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def decrypt_chunk(self, data: bytes, is_final: bool = True) -> bytes:
        """Дешифрование чанка данных"""
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Decrypting chunk: {len(data)} bytes, mode={self.mode}, is_final={is_final}")

        if self.mode == 'ecb':
            return self._process_ecb_chunk(data, encrypt=False, is_final=is_final)
        elif self.mode == 'cbc':
            return self._process_cbc_chunk(data, encrypt=False, is_final=is_final)
        elif self.mode == 'cfb':
            cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
            return cipher.decrypt(data)
        elif self.mode == 'ofb':
            cipher = AES.new(self.key, AES.MODE_OFB, self.iv)
            return cipher.decrypt(data)
        elif self.mode == 'ctr':
            counter = Counter.new(128, initial_value=int.from_bytes(self.iv, 'big'))
            cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
            return cipher.decrypt(data)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    # 🆕 Упрощенные методы для обратной совместимости
    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных (полная совместимость)"""
        if self.mode == 'ecb':
            padded_data = pad(data, self.BLOCK_SIZE)
            cipher = AES.new(self.key, AES.MODE_ECB)
            return cipher.encrypt(padded_data)
        elif self.mode == 'cbc':
            padded_data = pad(data, self.BLOCK_SIZE)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            encrypted = cipher.encrypt(padded_data)
            return self.iv + encrypted
        elif self.mode == 'ctr':
            counter = Counter.new(128, initial_value=int.from_bytes(self.iv, 'big'))
            cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
            encrypted = cipher.encrypt(data)
            return self.iv + encrypted
        elif self.mode in ['cfb', 'ofb']:
            if self.mode == 'cfb':
                cipher = AES.new(self.key, AES.MODE_CFB, self.iv, segment_size=128)
            else:
                cipher = AES.new(self.key, AES.MODE_OFB, self.iv)
            encrypted = cipher.encrypt(data)
            return self.iv + encrypted
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование данных (полная совместимость)"""
        if self.mode == 'ecb':
            if len(data) % self.BLOCK_SIZE != 0:
                raise ValueError(f"Data length must be multiple of block size {self.BLOCK_SIZE}")
            cipher = AES.new(self.key, AES.MODE_ECB)
            decrypted_padded = cipher.decrypt(data)
            return unpad(decrypted_padded, self.BLOCK_SIZE)
        elif self.mode == 'cbc':
            if len(data) < self.BLOCK_SIZE:
                raise ValueError("Ciphertext too short to contain IV")

            iv = data[:self.BLOCK_SIZE]
            actual_ciphertext = data[self.BLOCK_SIZE:]

            if len(actual_ciphertext) % self.BLOCK_SIZE != 0:
                raise ValueError(f"Ciphertext length must be multiple of block size {self.BLOCK_SIZE}")

            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(actual_ciphertext)
            return unpad(decrypted_padded, self.BLOCK_SIZE)
        elif self.mode == 'ctr':
            if len(data) < self.BLOCK_SIZE:
                raise ValueError("Ciphertext too short to contain nonce")

            nonce = data[:self.BLOCK_SIZE]
            actual_ciphertext = data[self.BLOCK_SIZE:]

            counter = Counter.new(128, initial_value=int.from_bytes(nonce, 'big'))
            cipher = AES.new(self.key, AES.MODE_CTR, counter=counter)
            return cipher.decrypt(actual_ciphertext)
        elif self.mode in ['cfb', 'ofb']:
            if len(data) < self.BLOCK_SIZE:
                raise ValueError("Ciphertext too short to contain IV")

            iv = data[:self.BLOCK_SIZE]
            actual_ciphertext = data[self.BLOCK_SIZE:]

            if self.mode == 'cfb':
                cipher = AES.new(self.key, AES.MODE_CFB, iv, segment_size=128)
            else:
                cipher = AES.new(self.key, AES.MODE_OFB, iv)
            return cipher.decrypt(actual_ciphertext)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def get_iv(self) -> bytes:
        """Возвращает IV"""
        return self.iv

    def set_iv(self, iv: bytes):
        """Устанавливает IV"""
        if self.mode != 'ecb':
            self.iv = iv

    def get_key_info(self) -> dict:
        """Информация о ключе"""
        info = {
            'length': len(self.key),
            'hex': self.key.hex(),
            'algorithm': 'AES',
            'key_size': len(self.key) * 8,
            'mode': self.mode.upper(),
            'iv_used': self.iv is not None,
            'iv': self.iv.hex() if self.iv else None
        }

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Key info: {info}")

        return info


def create_cipher(key: bytes, mode: str = 'ecb') -> CipherCore:
    if LOGGING_AVAILABLE:
        CryptoLogger.log(f"Creating cipher: mode={mode}, key_size={len(key)} bytes")
    return CipherCore(key, mode)


def encrypt_data(data: bytes, key: bytes, mode: str = 'ecb') -> bytes:
    if LOGGING_AVAILABLE:
        CryptoLogger.log(f"Quick encrypt: mode={mode}, data_size={len(data)} bytes")
    cipher = CipherCore(key, mode)
    return cipher.encrypt(data)


def decrypt_data(data: bytes, key: bytes, mode: str = 'ecb') -> bytes:
    if LOGGING_AVAILABLE:
        CryptoLogger.log(f"Quick decrypt: mode={mode}, data_size={len(data)} bytes")
    cipher = CipherCore(key, mode)
    return cipher.decrypt(data)