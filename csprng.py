"""
Cryptographically Secure Pseudorandom Number Generator (CSPRNG) Module
Uses os.urandom for cryptographically secure random number generation.
"""

import os
import sys
from typing import Optional


class CSPRNG:
    """
    Cryptographically Secure Pseudorandom Number Generator
    Uses operating system's cryptographic random number generator
    """

    @staticmethod
    def generate_random_bytes(num_bytes: int) -> bytes:
        """
        Generate cryptographically secure random bytes

        Args:
            num_bytes: Number of random bytes to generate

        Returns:
            bytes: Cryptographically secure random bytes

        Raises:
            ValueError: If num_bytes is not positive
            OSError: If OS random number generator fails
        """
        if num_bytes <= 0:
            raise ValueError(f"Number of bytes must be positive, got {num_bytes}")

        try:
            # Use OS cryptographic random number generator
            random_bytes = os.urandom(num_bytes)

            # Verify we got the requested number of bytes
            if len(random_bytes) != num_bytes:
                raise OSError(f"OS RNG returned {len(random_bytes)} bytes, expected {num_bytes}")

            return random_bytes

        except Exception as e:
            raise OSError(f"Cryptographic random number generation failed: {e}")

    @staticmethod
    def generate_random_hex_string(num_bytes: int) -> str:
        """
        Generate random bytes and return as hexadecimal string

        Args:
            num_bytes: Number of random bytes to generate

        Returns:
            str: Hexadecimal representation of random bytes
        """
        random_bytes = CSPRNG.generate_random_bytes(num_bytes)
        return random_bytes.hex()

    @staticmethod
    def generate_key(key_size: int = 16) -> bytes:
        """
        Generate cryptographic key of specified size

        Args:
            key_size: Key size in bytes (16 for AES-128, 32 for AES-256)

        Returns:
            bytes: Cryptographic key
        """
        if key_size not in [16, 24, 32]:
            raise ValueError(f"Invalid key size: {key_size}. Must be 16, 24, or 32 bytes")

        return CSPRNG.generate_random_bytes(key_size)

    @staticmethod
    def generate_iv(iv_size: int = 16) -> bytes:
        """
        Generate Initialization Vector (IV) for block cipher modes

        Args:
            iv_size: IV size in bytes (typically 16 for AES)

        Returns:
            bytes: Initialization Vector
        """
        return CSPRNG.generate_random_bytes(iv_size)

    @staticmethod
    def validate_key_strength(key: bytes) -> bool:
        """
        Validate key strength by checking for weak patterns

        Args:
            key: Key to validate

        Returns:
            bool: True if key appears strong, False if weak patterns detected
        """
        if not key:
            return False

        # Check for all zeros
        if all(b == 0 for b in key):
            return False

        # Check for sequential bytes (increasing)
        sequential_inc = all(key[i] + 1 == key[i + 1] for i in range(len(key) - 1))
        # Check for sequential bytes (decreasing)
        sequential_dec = all(key[i] - 1 == key[i + 1] for i in range(len(key) - 1))

        if sequential_inc or sequential_dec:
            return False

        # Check for repeated bytes
        if all(b == key[0] for b in key):
            return False

        # Check Hamming weight (should be around 50% ones)
        total_bits = len(key) * 8
        ones_count = sum(bin(b).count('1') for b in key)
        ones_ratio = ones_count / total_bits

        # If ratio is too extreme (outside 30%-70%), consider weak
        if ones_ratio < 0.3 or ones_ratio > 0.7:
            return False

        return True


# Convenience functions
def generate_random_bytes(num_bytes: int) -> bytes:
    """Convenience function for generating random bytes"""
    return CSPRNG.generate_random_bytes(num_bytes)


def generate_key(key_size: int = 16) -> bytes:
    """Convenience function for generating keys"""
    return CSPRNG.generate_key(key_size)


def generate_iv(iv_size: int = 16) -> bytes:
    """Convenience function for generating IVs"""
    return CSPRNG.generate_iv(iv_size)