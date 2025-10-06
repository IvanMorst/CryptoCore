import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from crypto.modes import CBCMode, CFBMode, OFBMode, CTRMode


class CipherCore:
    BLOCK_SIZE = 16

    def __init__(self, key: bytes, mode: str = 'ecb', iv: bytes = None):
        """
        Инициализация cipher core с поддержкой разных режимов

        Args:
            key: ключ шифрования (16, 24, или 32 байта для AES)
            mode: режим работы ('ecb', 'cbc', 'cfb', 'ofb', 'ctr')
            iv: вектор инициализации (требуется для режимов кроме ECB)
        """
        if len(key) not in [16, 24, 32]:
            raise ValueError(
                f"Key must be 16, 24, or 32 bytes for AES. Got {len(key)} bytes"
            )
        self.key = key
        self.mode = mode.lower()

        # Генерация IV для режимов, которые его требуют
        if self.mode != 'ecb' and iv is None:
            self.iv = os.urandom(self.BLOCK_SIZE)
        else:
            self.iv = iv

        # Инициализация соответствующего режима
        if self.mode == 'ecb':
            self._cipher = AES.new(self.key, AES.MODE_ECB)
        elif self.mode == 'cbc':
            if self.iv is None:
                raise ValueError("IV required for CBC mode")
            self._mode_instance = CBCMode(self.key, self.iv)
        elif self.mode == 'cfb':
            if self.iv is None:
                raise ValueError("IV required for CFB mode")
            self._mode_instance = CFBMode(self.key, self.iv)
        elif self.mode == 'ofb':
            if self.iv is None:
                raise ValueError("IV required for OFB mode")
            self._mode_instance = OFBMode(self.key, self.iv)
        elif self.mode == 'ctr':
            if self.iv is None:
                raise ValueError("IV required for CTR mode")
            self._mode_instance = CTRMode(self.key, self.iv)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных в выбранном режиме"""
        if self.mode == 'ecb':
            padded_data = pad(data, self.BLOCK_SIZE)
            return self._cipher.encrypt(padded_data)
        else:
            return self._mode_instance.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование данных в выбранном режиме"""
        if self.mode == 'ecb':
            decrypted_padded = self._cipher.decrypt(data)
            return unpad(decrypted_padded, self.BLOCK_SIZE)
        else:
            return self._mode_instance.decrypt(data)

    def get_iv(self) -> bytes:
        """Получить IV (для режимов кроме ECB)"""
        if self.mode == 'ecb':
            return None
        return self.iv

    def get_key_info(self) -> dict:
        """Информация о ключе и режиме"""
        info = {
            'length': len(self.key),
            'hex': self.key.hex(),
            'algorithm': 'AES',
            'key_size': len(self.key) * 8,
            'mode': self.mode
        }
        if self.mode != 'ecb':
            info['iv'] = self.iv.hex()
        return info