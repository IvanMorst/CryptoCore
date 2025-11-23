#!/usr/bin/env python3
"""
Tests for SHA-256 implementation
"""

import unittest
import sys
import os

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hash.sha256 import SHA256, sha256, sha256_file  # 🆕 Добавлен импорт sha256_file


class TestSHA256(unittest.TestCase):
    """Test cases for SHA-256 implementation"""

    def test_nist_empty_string(self):
        """Test NIST vector: empty string"""
        # NIST test vector: SHA-256("") = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        result = sha256(b"")
        self.assertEqual(result, expected)

    def test_nist_abc(self):
        """Test NIST vector: 'abc'"""
        # NIST test vector: SHA-256("abc") = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
        expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        result = sha256(b"abc")
        self.assertEqual(result, expected)

    def test_nist_long_message(self):
        """Test NIST vector: 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'"""
        # NIST test vector for the given string
        message = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
        expected = "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
        result = sha256(message)
        self.assertEqual(result, expected)

    def test_incremental_hashing(self):
        """Test incremental hashing vs one-shot"""
        message = b"Test message for incremental hashing"

        # One-shot hashing
        hash1 = sha256(message)

        # Incremental hashing
        hasher = SHA256()
        hasher.update(message[:10])
        hasher.update(message[10:20])
        hasher.update(message[20:])
        hash2 = hasher.hexdigest()

        self.assertEqual(hash1, hash2)

    def test_file_hashing(self):
        """Test file hashing functionality"""
        # Create a test file
        test_content = b"File content for hashing test"
        test_file = "test_hash_file.txt"

        try:
            with open(test_file, 'wb') as f:
                f.write(test_content)

            # Hash using our function
            file_hash = sha256(test_content)

            # Hash using file function
            file_hash_from_func = sha256_file(test_file)

            self.assertEqual(file_hash, file_hash_from_func)

        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_avalanche_effect(self):
        """Test that changing one bit produces completely different hash"""
        message1 = b"Hello World"
        message2 = b"Hello World"  # Same but we'll change one byte

        # Convert to bytearray to modify one byte
        msg2_bytes = bytearray(message1)
        msg2_bytes[0] ^= 0x01  # Flip one bit
        message2 = bytes(msg2_bytes)

        hash1 = sha256(message1)
        hash2 = sha256(message2)

        # Hashes should be completely different
        self.assertNotEqual(hash1, hash2)

        # Count differing bits
        hex1 = int(hash1, 16)
        hex2 = int(hash2, 16)
        diff_bits = bin(hex1 ^ hex2).count('1')

        # Should have significant number of differing bits (avalanche effect)
        self.assertGreater(diff_bits, 100)
        print(f"Avalanche effect: {diff_bits} bits differ")


if __name__ == '__main__':
    print("Running SHA-256 tests...")
    unittest.main(verbosity=2)