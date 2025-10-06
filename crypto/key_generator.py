import hashlib
from typing import Optional
from .generator import Generator


class KeyGenerator:
    KEY_LENGTH = 16  # 256 бит
    SALT_SIZE = 16
    ITERATIONS = 100000

    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Генерация ключа из пароля и соли (адаптация Java кода)"""
        try:
            # Подготавливаем входные данные: password + salt
            input_data = password.encode('utf-8') + salt

            # Первое хеширование SHA-512
            digest = hashlib.sha512()
            digest.update(input_data)
            hash_result = digest.digest()

            # Многократные итерации с трансформациями
            for i in range(KeyGenerator.ITERATIONS):
                digest = hashlib.sha512()
                digest.update(hash_result)
                hash_result = digest.digest()

                # Применяем битовые трансформации (аналогично Java коду)
                transformed_hash = bytearray(hash_result)
                for j in range(len(transformed_hash)):
                    # (hash[j] << 3) | ((hash[j] & 0xFF) >>> 5)
                    original_byte = transformed_hash[j]
                    left_shifted = (original_byte << 3) & 0xFF
                    right_shifted = (original_byte & 0xFF) >> 5
                    transformed_byte = left_shifted | right_shifted

                    # hash[j] ^= (i >> (j % 8)) & 0xFF
                    xor_value = (i >> (j % 8)) & 0xFF
                    transformed_byte ^= xor_value

                    transformed_hash[j] = transformed_byte & 0xFF

                hash_result = bytes(transformed_hash)

            # Возвращаем первые KEY_LENGTH байт
            return hash_result[:KeyGenerator.KEY_LENGTH]

        except Exception as e:
            from .crypto_exception import CryptoException
            raise CryptoException("Key generation failed", e)

    @staticmethod
    def generate_salt() -> bytes:
        """Генерация соли с использованием нашего Generator"""
        return Generator.generate_random_bytes(KeyGenerator.SALT_SIZE)