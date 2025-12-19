"""
GCM (Galois/Counter Mode) implementation from scratch
Following NIST SP 800-38D specification
"""

import os
import struct
from typing import Tuple
from Crypto.Cipher import AES


class AuthenticationError(Exception):
    """Exception for authentication failures in GCM"""
    pass


class GCM:
    """Galois/Counter Mode (GCM) authenticated encryption"""

    def __init__(self, key: bytes, nonce: bytes = None):
        if len(key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes for AES")

        self.key = key
        self.nonce = nonce if nonce else os.urandom(12)

        # Initialize AES for CTR mode
        self.aes = AES.new(key, AES.MODE_ECB)

        # Precompute H for GHASH
        zero_block = bytes(16)
        self.H = int.from_bytes(self.aes.encrypt(zero_block), 'big')

    def _mult_gf(self, x: int, y: int) -> int:
        """
        Multiplication in GF(2^128)
        Irreducible polynomial: x^128 + x^7 + x^2 + x + 1
        """
        R = 0xE1000000000000000000000000000000
        z = 0
        v = y

        # Polynomial multiplication
        for i in range(127, -1, -1):
            if (x >> i) & 1:
                z ^= v
            # Multiply v by x
            if v & 1:
                v = (v >> 1) ^ R
            else:
                v >>= 1

        return z

    def _ghash(self, aad: bytes, ciphertext: bytes) -> int:
        """Compute GHASH authentication value"""
        # Prepare blocks
        aad_len = len(aad)
        ct_len = len(ciphertext)

        # Process AAD
        y = 0
        for i in range(0, aad_len, 16):
            block = aad[i:i+16]
            if len(block) < 16:
                block = block.ljust(16, b'\x00')
            block_int = int.from_bytes(block, 'big')
            y = self._mult_gf(y ^ block_int, self.H)

        # Process ciphertext
        for i in range(0, ct_len, 16):
            block = ciphertext[i:i+16]
            if len(block) < 16:
                block = block.ljust(16, b'\x00')
            block_int = int.from_bytes(block, 'big')
            y = self._mult_gf(y ^ block_int, self.H)

        # Process lengths (64-bit for AAD, 64-bit for ciphertext)
        len_block = ((aad_len * 8) << 64) | (ct_len * 8)
        len_bytes = len_block.to_bytes(16, 'big')
        len_int = int.from_bytes(len_bytes, 'big')
        y = self._mult_gf(y ^ len_int, self.H)

        return y

    def _compute_j0(self, nonce: bytes) -> bytes:
        """Compute J0 from nonce according to NIST SP 800-38D"""
        if len(nonce) == 12:
            # For 96-bit nonce: J0 = nonce || 0x00000001
            j0 = nonce + b'\x00\x00\x00\x01'
        else:
            # For non-96-bit nonce: J0 = GHASH(nonce || zeros)
            # where zeros pad to multiple of 128 bits
            nonce_len = len(nonce)
            padding_len = (16 - (nonce_len % 16)) % 16
            padded_nonce = nonce + b'\x00' * padding_len + (nonce_len * 8).to_bytes(8, 'big') + (0).to_bytes(8, 'big')

            # GHASH of padded nonce
            j0_int = 0
            for i in range(0, len(padded_nonce), 16):
                block = padded_nonce[i:i+16]
                block_int = int.from_bytes(block, 'big')
                j0_int = self._mult_gf(j0_int ^ block_int, self.H)

            j0 = j0_int.to_bytes(16, 'big')

        return j0

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        """GCM encryption with authentication"""
        # Generate J0 from nonce
        j0 = self._compute_j0(self.nonce)
        j0_int = int.from_bytes(j0, 'big')

        # Encrypt with CTR mode (starting from J0+1)
        ciphertext = bytearray()

        for i in range(0, len(plaintext), 16):
            counter = (j0_int + 1 + (i // 16)).to_bytes(16, 'big')
            keystream = self.aes.encrypt(counter)

            block = plaintext[i:i+16]
            encrypted = bytes(a ^ b for a, b in zip(block, keystream[:len(block)]))
            ciphertext.extend(encrypted)

        ciphertext = bytes(ciphertext)

        # Compute authentication tag
        s = self.aes.encrypt(j0)
        s_int = int.from_bytes(s, 'big')

        t = self._ghash(aad, ciphertext) ^ s_int

        # Format: nonce (12B) + ciphertext + tag (16B)
        return self.nonce + ciphertext + t.to_bytes(16, 'big')

    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        """GCM decryption with authentication"""
        if len(data) < 28:  # min: 12B nonce + 0B ciphertext + 16B tag = 28B
            raise ValueError("Data too short for GCM")

        # Extract components
        nonce = data[:12]
        ciphertext = data[12:-16]
        tag = int.from_bytes(data[-16:], 'big')

        # Verify authentication tag
        j0 = self._compute_j0(nonce)

        s = self.aes.encrypt(j0)
        s_int = int.from_bytes(s, 'big')

        t_computed = self._ghash(aad, ciphertext) ^ s_int

        if t_computed != tag:
            raise AuthenticationError("GCM authentication failed")

        # Decrypt with CTR mode
        j0_int = int.from_bytes(j0, 'big')
        plaintext = bytearray()

        for i in range(0, len(ciphertext), 16):
            counter = (j0_int + 1 + (i // 16)).to_bytes(16, 'big')
            keystream = self.aes.encrypt(counter)

            block = ciphertext[i:i+16]
            decrypted = bytes(a ^ b for a, b in zip(block, keystream[:len(block)]))
            plaintext.extend(decrypted)

        return bytes(plaintext)