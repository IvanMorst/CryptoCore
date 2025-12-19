"""
HMAC (Hash-based Message Authentication Code) implementation
RFC 2104 compliant implementation using SHA-256
"""

import struct
from typing import Optional
import sys
import os

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hash.sha256 import SHA256


class HMAC:
    """
    HMAC implementation following RFC 2104
    Uses SHA-256 as the underlying hash function
    """

    # SHA-256 block size is 64 bytes (512 bits)
    BLOCK_SIZE = 64

    def __init__(self, key: bytes, hash_func_name: str = 'sha256'):
        """
        Initialize HMAC with a key

        Args:
            key: HMAC key (arbitrary length)
            hash_func_name: Name of hash function (currently only 'sha256' supported)
        """
        if hash_func_name != 'sha256':
            raise ValueError(f"Unsupported hash function: {hash_func_name}")

        self.hash_func = SHA256
        self.key = self._process_key(key)

    def _process_key(self, key: bytes) -> bytes:
        """
        Process key according to RFC 2104:
        - If key longer than block size: hash it to get key length = hash output size
        - If key shorter than block size: pad with zeros to block size
        """
        # Step 1: Keys longer than block size are hashed
        if len(key) > self.BLOCK_SIZE:
            # IMPORTANT FIX: Create hash instance and use update/digest
            hasher = self.hash_func()
            hasher.update(key)
            key = hasher.digest()

        # Step 2: Keys shorter than block size are padded with zeros
        if len(key) < self.BLOCK_SIZE:
            key = key + b'\x00' * (self.BLOCK_SIZE - len(key))

        return key

    @staticmethod
    def _xor_bytes(a: bytes, b: bytes) -> bytes:
        """XOR two byte strings of equal length"""
        if len(a) != len(b):
            raise ValueError("Byte strings must have equal length")
        return bytes(x ^ y for x, y in zip(a, b))

    def compute(self, message: bytes) -> bytes:
        """
        Compute HMAC for a message

        Formula: HMAC(K, m) = H((K ⊕ opad) ∥ H((K ⊕ ipad) ∥ m))
        where H is SHA-256

        Args:
            message: Message to authenticate

        Returns:
            bytes: HMAC value
        """
        # Create inner and outer pads
        ipad = b'\x36' * self.BLOCK_SIZE
        opad = b'\x5c' * self.BLOCK_SIZE

        # XOR key with pads
        key_ipad = self._xor_bytes(self.key, ipad)
        key_opad = self._xor_bytes(self.key, opad)

        # Inner hash: H((K ⊕ ipad) ∥ message)
        inner_hasher = self.hash_func()
        inner_hasher.update(key_ipad)
        inner_hasher.update(message)
        inner_hash = inner_hasher.digest()

        # Outer hash: H((K ⊕ opad) ∥ inner_hash)
        outer_hasher = self.hash_func()
        outer_hasher.update(key_opad)
        outer_hasher.update(inner_hash)

        return outer_hasher.digest()

    def compute_hex(self, message: bytes) -> str:
        """
        Compute HMAC and return as hexadecimal string

        Args:
            message: Message to authenticate

        Returns:
            str: HMAC as hexadecimal string
        """
        return self.compute(message).hex()

    def compute_file(self, filename: str, chunk_size: int = 8192) -> str:
        """
        Compute HMAC for a file (streaming)

        Args:
            filename: Path to file
            chunk_size: Size of chunks to read

        Returns:
            str: HMAC as hexadecimal string
        """
        # Create inner and outer pads
        ipad = b'\x36' * self.BLOCK_SIZE
        opad = b'\x5c' * self.BLOCK_SIZE

        # XOR key with pads
        key_ipad = self._xor_bytes(self.key, ipad)
        key_opad = self._xor_bytes(self.key, opad)

        # Inner hash: H((K ⊕ ipad) ∥ message)
        inner_hasher = self.hash_func()
        inner_hasher.update(key_ipad)

        try:
            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    inner_hasher.update(chunk)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filename}")
        except IOError as e:
            raise IOError(f"Error reading file {filename}: {e}")

        inner_hash = inner_hasher.digest()

        # Outer hash: H((K ⊕ opad) ∥ inner_hash)
        outer_hasher = self.hash_func()
        outer_hasher.update(key_opad)
        outer_hasher.update(inner_hash)

        return outer_hasher.hexdigest()


# Convenience functions
def hmac_sha256(key: bytes, message: bytes) -> bytes:
    """
    Convenience function for one-shot HMAC-SHA256 computation

    Args:
        key: HMAC key
        message: Message to authenticate

    Returns:
        bytes: HMAC as bytes
    """
    hmac = HMAC(key, 'sha256')
    return hmac.compute(message)


def hmac_sha256_hex(key: bytes, message: bytes) -> str:
    """
    Convenience function for one-shot HMAC-SHA256 computation

    Args:
        key: HMAC key
        message: Message to authenticate

    Returns:
        str: HMAC as hexadecimal string
    """
    hmac = HMAC(key, 'sha256')
    return hmac.compute_hex(message)


def hmac_sha256_file(key: bytes, filename: str, chunk_size: int = 8192) -> str:
    """
    Convenience function for HMAC-SHA256 of a file

    Args:
        key: HMAC key
        filename: Path to file
        chunk_size: Size of chunks to read

    Returns:
        str: HMAC as hexadecimal string
    """
    hmac = HMAC(key, 'sha256')
    return hmac.compute_file(filename, chunk_size)


def verify_hmac(key: bytes, message: bytes, expected_hmac: str) -> bool:
    """
    Verify HMAC

    Args:
        key: HMAC key
        message: Message to verify
        expected_hmac: Expected HMAC value (hex string)

    Returns:
        bool: True if HMAC matches, False otherwise
    """
    computed = hmac_sha256_hex(key, message)
    return computed == expected_hmac.lower()


def verify_hmac_file(key: bytes, filename: str, expected_hmac: str, chunk_size: int = 8192) -> bool:
    """
    Verify HMAC for a file

    Args:
        key: HMAC key
        filename: Path to file
        expected_hmac: Expected HMAC value (hex string)
        chunk_size: Size of chunks to read

    Returns:
        bool: True if HMAC matches, False otherwise
    """
    computed = hmac_sha256_file(key, filename, chunk_size)
    return computed == expected_hmac.lower()