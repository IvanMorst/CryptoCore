#!/usr/bin/env python3
"""
Tests for Cryptographically Secure Pseudorandom Number Generator
"""

import sys
import os
import unittest

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from csprng import CSPRNG, generate_random_bytes


class TestCSPRNG(unittest.TestCase):
    """Test cases for CSPRNG module"""

    def test_generate_random_bytes(self):
        """Test basic random bytes generation"""
        # Test different sizes
        for size in [1, 16, 32, 100]:
            with self.subTest(size=size):
                random_bytes = CSPRNG.generate_random_bytes(size)
                self.assertEqual(len(random_bytes), size)
                self.assertIsInstance(random_bytes, bytes)

    def test_generate_random_bytes_invalid_size(self):
        """Test error handling for invalid sizes"""
        with self.assertRaises(ValueError):
            CSPRNG.generate_random_bytes(0)
        with self.assertRaises(ValueError):
            CSPRNG.generate_random_bytes(-1)

    def test_generate_key(self):
        """Test key generation"""
        for key_size in [16, 24, 32]:
            with self.subTest(key_size=key_size):
                key = CSPRNG.generate_key(key_size)
                self.assertEqual(len(key), key_size)
                self.assertIsInstance(key, bytes)

    def test_generate_key_invalid_size(self):
        """Test error handling for invalid key sizes"""
        with self.assertRaises(ValueError):
            CSPRNG.generate_key(15)
        with self.assertRaises(ValueError):
            CSPRNG.generate_key(33)

    def test_generate_iv(self):
        """Test IV generation"""
        iv = CSPRNG.generate_iv(16)
        self.assertEqual(len(iv), 16)
        self.assertIsInstance(iv, bytes)

    def test_key_uniqueness(self):
        """Test that generated keys are unique"""
        key_set = set()
        num_keys = 1000

        for _ in range(num_keys):
            key = CSPRNG.generate_key(16)
            key_hex = key.hex()

            # Check for uniqueness
            self.assertNotIn(key_hex, key_set, f"Duplicate key found: {key_hex}")
            key_set.add(key_hex)

        print(f"Successfully generated {len(key_set)} unique AES-128 keys.")

    def test_key_strength_validation(self):
        """Test key strength validation"""
        # Strong key (random)
        strong_key = CSPRNG.generate_key(16)
        self.assertTrue(CSPRNG.validate_key_strength(strong_key))

        # Weak key (all zeros)
        weak_key_zeros = bytes(16)
        self.assertFalse(CSPRNG.validate_key_strength(weak_key_zeros))

        # Weak key (sequential increasing)
        weak_key_sequential_inc = bytes(range(16))
        self.assertFalse(CSPRNG.validate_key_strength(weak_key_sequential_inc))

        # Weak key (sequential decreasing)
        weak_key_sequential_dec = bytes(range(15, -1, -1))
        self.assertFalse(CSPRNG.validate_key_strength(weak_key_sequential_dec))

        # Weak key (all same bytes)
        weak_key_same = bytes([0xAB] * 16)
        self.assertFalse(CSPRNG.validate_key_strength(weak_key_same))

    def test_basic_entropy(self):
        """Test basic entropy characteristics"""
        key = CSPRNG.generate_key(16)
        total_bits = len(key) * 8
        ones_count = sum(bin(b).count('1') for b in key)
        ones_ratio = ones_count / total_bits

        # Check that ones ratio is reasonable (between 30% and 70%)
        self.assertGreaterEqual(ones_ratio, 0.3)
        self.assertLessEqual(ones_ratio, 0.7)

        print(f"Key entropy test: {ones_count}/{total_bits} bits set ({ones_ratio:.1%})")


def generate_nist_test_data():
    """Generate test data for NIST statistical tests"""
    total_size = 10_000_000  # 10 MB
    output_file = 'nist_test_data.bin'

    print(f"Generating {total_size} bytes for NIST testing...")

    with open(output_file, 'wb') as f:
        bytes_written = 0
        while bytes_written < total_size:
            chunk_size = min(4096, total_size - bytes_written)
            random_chunk = generate_random_bytes(chunk_size)
            f.write(random_chunk)
            bytes_written += chunk_size

    print(f"Generated {bytes_written} bytes for NIST testing in '{output_file}'")
    return output_file


if __name__ == '__main__':
    # Run unit tests
    #print("Running CSPRNG unit tests...")
    #unittest.main(verbosity=2)

    # Generate NIST test data
    print("\nGenerating NIST test data...")
    generate_nist_test_data()