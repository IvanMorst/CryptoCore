"""
Encrypt-then-MAC paradigm implementation
C = E(K_e, P), T = MAC(K_m, C ∥ AAD), output = C ∥ T
"""

import os
import hashlib
from typing import Tuple


class AuthenticationError(Exception):
    """Exception for authentication failures in Encrypt-then-MAC"""
    pass


class EncryptThenMAC:
    """Encrypt-then-MAC authenticated encryption"""

    def __init__(self, enc_key: bytes, mac_key: bytes,
                 enc_mode: str = 'ctr', hash_algo: str = 'sha256'):
        from crypto.cipher_core import CipherCore
        from mac.hmac import HMAC

        self.encryptor = CipherCore(enc_key, enc_mode)
        self.hmac = HMAC(mac_key, hash_algo)
        self.hash_algo = hash_algo

    @staticmethod
    def derive_keys(master_key: bytes, hash_algo: str = 'sha256') -> Tuple[bytes, bytes]:
        """Derive separate encryption and MAC keys from master key"""
        if hash_algo == 'sha256':
            hash_func = hashlib.sha256
        else:
            raise ValueError(f"Unsupported hash algorithm: {hash_algo}")

        # Key separation using HKDF-like approach
        enc_key = hash_func(master_key + b'enc').digest()[:16]
        mac_key = hash_func(master_key + b'mac').digest()

        return enc_key, mac_key

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        """Encrypt then compute MAC"""
        # Encrypt
        ciphertext = self.encryptor.encrypt(plaintext)

        # Compute MAC over ciphertext + AAD
        mac_data = ciphertext + aad
        tag = self.hmac.compute(mac_data)

        # Convert hex tag to bytes
        tag_bytes = bytes.fromhex(tag) if isinstance(tag, str) else tag

        return ciphertext + tag_bytes

    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        """Verify MAC then decrypt"""
        # Split ciphertext and tag (tag length depends on hash algorithm)
        if self.hash_algo == 'sha256':
            tag_len = 32  # SHA-256 produces 32-byte hash
        else:
            raise ValueError(f"Unknown tag length for {self.hash_algo}")

        if len(data) < tag_len:
            raise ValueError("Data too short")

        ciphertext = data[:-tag_len]
        tag = data[-tag_len:]

        # Verify MAC
        mac_data = ciphertext + aad
        expected_tag = self.hmac.compute(mac_data)
        expected_tag_bytes = bytes.fromhex(expected_tag) if isinstance(expected_tag, str) else expected_tag

        # Constant-time comparison
        if len(tag) != len(expected_tag_bytes):
            raise AuthenticationError("MAC verification failed")

        # Use constant-time comparison to avoid timing attacks
        result = 0
        for x, y in zip(tag, expected_tag_bytes):
            result |= x ^ y

        if result != 0:
            raise AuthenticationError("MAC verification failed")

        # Decrypt
        return self.encryptor.decrypt(ciphertext)