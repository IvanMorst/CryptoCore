from .base_mode import BaseMode


class OFBMode(BaseMode):
    def encrypt(self, data: bytes) -> bytes:
        """Шифрование в режиме OFB"""
        blocks = self._split_into_blocks(data, pad=False)
        cipher_blocks = []
        keystream_block = self.iv

        for block in blocks:
            keystream_block = self._encrypt_block(keystream_block)
            cipher_block = bytes(a ^ b for a, b in zip(block, keystream_block))
            cipher_blocks.append(cipher_block)

        return b''.join(cipher_blocks)

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование в режиме OFB (идентично шифрованию)"""
        return self.encrypt(data)