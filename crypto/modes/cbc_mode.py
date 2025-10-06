from Crypto.Util.Padding import pad, unpad
from .base_mode import BaseMode


class CBCMode(BaseMode):
    def encrypt(self, data: bytes) -> bytes:
        """Шифрование в режиме CBC с PKCS7 паддингом"""
        padded_data = pad(data, self.BLOCK_SIZE)
        blocks = self._split_into_blocks(padded_data)
        cipher_blocks = []
        prev = self.iv

        for block in blocks:
            xored = bytes(a ^ b for a, b in zip(block, prev))
            encrypted_block = self._encrypt_block(xored)
            cipher_blocks.append(encrypted_block)
            prev = encrypted_block

        return b''.join(cipher_blocks)

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование в режиме CBC с удалением PKCS7 паддинга"""
        if len(data) % self.BLOCK_SIZE != 0:
            raise ValueError("Data length must be multiple of block size")

        blocks = self._split_into_blocks(data)
        plain_blocks = []
        prev = self.iv

        for block in blocks:
            decrypted_block = self._decrypt_block(block)
            plain_block = bytes(a ^ b for a, b in zip(decrypted_block, prev))
            plain_blocks.append(plain_block)
            prev = block

        plaintext = b''.join(plain_blocks)
        return unpad(plaintext, self.BLOCK_SIZE)