from .base_mode import BaseMode


class CTRMode(BaseMode):
    def encrypt(self, data: bytes) -> bytes:
        """Шифрование в режиме CTR"""
        blocks = self._split_into_blocks(data, pad=False)
        cipher_blocks = []

        for i, block in enumerate(blocks):
            counter = self._increment_counter(self.iv, i)
            encrypted_counter = self._encrypt_block(counter)
            cipher_block = bytes(a ^ b for a, b in zip(block, encrypted_counter))
            cipher_blocks.append(cipher_block)

        return b''.join(cipher_blocks)

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование в режиме CTR (идентично шифрованию)"""
        return self.encrypt(data)

    def _increment_counter(self, iv: bytes, increment: int) -> bytes:
        """Инкремент счетчика (big-endian)"""
        counter_int = int.from_bytes(iv, byteorder='big')
        counter_int = (counter_int + increment) % (2 ** 128)
        return counter_int.to_bytes(16, byteorder='big')