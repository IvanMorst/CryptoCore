"""
PBKDF2 (Password-Based Key Derivation Function 2) implementation
RFC 2898 compliant implementation using HMAC-SHA256
"""

import struct
import hashlib
from typing import Union
import os

# Импорт нашей реализации HMAC
from mac.hmac import hmac_sha256


class PBKDF2:
    """
    PBKDF2 implementation following RFC 2898
    Uses HMAC-SHA256 as the underlying PRF
    """

    def __init__(self, prf: callable = None):
        """
        Initialize PBKDF2 with a PRF (default: HMAC-SHA256)

        Args:
            prf: Pseudorandom function (default: HMAC-SHA256)
        """
        self.prf = prf or hmac_sha256

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
            u_prev = self.prf(password, block_salt)
            block = u_prev

            # Compute U2 through Uc
            for _ in range(2, iterations + 1):
                u_curr = self.prf(password, u_prev)
                # XOR u_curr into block
                block = bytes(a ^ b for a, b in zip(block, u_curr))
                u_prev = u_curr

            derived_key += block

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