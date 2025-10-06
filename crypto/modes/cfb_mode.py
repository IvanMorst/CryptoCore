from .base_mode import BaseMode


class CFBMode(BaseMode):
    def encrypt(self, data: bytes) -> bytes:
        """Шифрование в режиме CFB (полный блок)"""
        blocks = self._split_into_blocks(data, pad=False)
        cipher_blocks = []
        prev = self.iv

        for block in blocks:
            encrypted_prev = self._encrypt_block(prev)
            cipher_block = bytes(a ^ b for a, b in zip(block, encrypted_prev))
            cipher_blocks.append(cipher_block)
            prev = cipher_block

        return b''.join(cipher_blocks)

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрование в режиме CFB (полный блок)"""
        blocks = self._split_into_blocks(data, pad=False)
        plain_blocks = []
        prev = self.iv

        for block in blocks:
            encrypted_prev = self._encrypt_block(prev)
            plain_block = bytes(a ^ b for a, b in zip(block, encrypted_prev))
            plain_blocks.append(plain_block)
            prev = block

        return b''.join(plain_blocks)