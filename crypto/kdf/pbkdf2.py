"""
PBKDF2 (Password-Based Key Derivation Function 2) implementation
RFC 2898 compliant implementation using HMAC-SHA256
"""

import struct
from typing import Union
import os

# Импорт нашей реализации HMAC
from mac.hmac import HMAC


class PBKDF2:
    """
    PBKDF2 implementation following RFC 2898
    Uses HMAC-SHA256 as the underlying PRF
    """

    def __init__(self):
        """Initialize PBKDF2 with HMAC-SHA256"""
        pass

    def _hmac_sha256(self, key: bytes, data: bytes) -> bytes:
        """
        HMAC-SHA256 wrapper for PBKDF2

        Args:
            key: HMAC key
            data: Data to authenticate

        Returns:
            bytes: HMAC-SHA256 result
        """
        hmac = HMAC(key, 'sha256')
        return hmac.compute(data)

    def derive(self, password: Union[str, bytes],
               salt: Union[str, bytes],
               iterations: int,
               dklen: int) -> bytes:
        """
        Derive a key from password and salt

        Args:
            password: Password (string or bytes)
            salt: Salt (string or bytes, hex string if string)
            iterations: Number of iterations
            dklen: Desired key length in bytes

        Returns:
            bytes: Derived key
        """
        # Convert inputs to bytes
        if isinstance(password, str):
            password = password.encode('utf-8')

        if isinstance(salt, str):
            # Check if it's a hex string
            salt_str = salt.strip().lower()
            if all(c in '0123456789abcdef' for c in salt_str):
                salt = bytes.fromhex(salt_str)
            else:
                salt = salt.encode('utf-8')

        # Validate inputs
        if iterations <= 0:
            raise ValueError("Iterations must be positive")
        if dklen <= 0:
            raise ValueError("Key length must be positive")
        if dklen > (2**32 - 1) * 32:  # SHA-256 output is 32 bytes
            raise ValueError("Key length too large")

        # Calculate number of blocks needed
        hlen = 32  # SHA-256 output length
        blocks_needed = (dklen + hlen - 1) // hlen

        derived_key = b''

        for i in range(1, blocks_needed + 1):
            # U1 = PRF(password, salt || INT_32_BE(i))
            block_salt = salt + struct.pack('>I', i)
            u_block = self._hmac_sha256(password, block_salt)
            block_result = u_block

            # Compute U2 through Uc
            for _ in range(2, iterations + 1):
                u_curr = self._hmac_sha256(password, u_block)
                # XOR current U with block_result
                block_result = bytes(x ^ y for x, y in zip(block_result, u_curr))
                u_block = u_curr

            derived_key += block_result

        # Return exactly dklen bytes
        return derived_key[:dklen]


def pbkdf2_hmac_sha256(password: Union[str, bytes],
                       salt: Union[str, bytes],
                       iterations: int,
                       dklen: int) -> bytes:
    """
    Convenience function for PBKDF2-HMAC-SHA256

    Args:
        password: Password (string or bytes)
        salt: Salt (string or bytes)
        iterations: Number of iterations
        dklen: Desired key length in bytes

    Returns:
        bytes: Derived key
    """
    pbkdf2 = PBKDF2()
    return pbkdf2.derive(password, salt, iterations, dklen)


def generate_salt(salt_size: int = 16) -> bytes:
    """
    Generate cryptographically secure random salt

    Args:
        salt_size: Size of salt in bytes (default: 16)

    Returns:
        bytes: Random salt
    """
    return os.urandom(salt_size)