"""
GCM mode adapter for CLI integration
"""

import os
from crypto.aead.gcm import GCM, AuthenticationError


class GCM_Mode:
    """GCM mode wrapper for CipherCore compatibility"""

    def __init__(self, key: bytes, iv: bytes = None):
        self.key = key
        self.nonce = iv if iv else None
        self.gcm = GCM(key, self.nonce)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt with empty AAD (CLI will handle AAD separately)"""
        return self.gcm.encrypt(data, b"")

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt with empty AAD"""
        try:
            return self.gcm.decrypt(data, b"")
        except AuthenticationError as e:
            raise AuthenticationError(str(e))

    def get_key_info(self) -> dict:
        """Get encryption info"""
        return {
            'algorithm': 'AES-GCM',
            'key': self.key.hex(),
            'nonce': self.gcm.nonce.hex() if hasattr(self.gcm, 'nonce') else None,
            'nonce_length': len(self.gcm.nonce) if hasattr(self.gcm, 'nonce') else 0
        }