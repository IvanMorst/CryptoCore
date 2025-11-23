#!/usr/bin/env python3
"""
Tests for SHA3-256 implementation
"""

import unittest
import sys
import os

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hash.sha3_256 import SHA3_256, sha3_256, sha3_256_file  # 🆕 Добавлен импорт sha3_256_file


class TestSHA3_256(unittest.TestCase):
    """Test cases for SHA3-256 implementation"""

    def test_empty_string(self):
        """Test empty string"""
        # SHA3-256("") = a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
        expected = "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"
        result = sha3_256(b"")
        self.assertEqual(result, expected)

    def test_abc(self):
        """Test 'abc' string"""
        # SHA3-256("abc") = 3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532
        expected = "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"
        result = sha3_256(b"abc")
        self.assertEqual(result, expected)

    def test_incremental_hashing(self):
        """Test incremental hashing vs one-shot"""
        message = b"Test message for incremental hashing with SHA3"

        # One-shot hashing
        hash1 = sha3_256(message)

        # Incremental hashing
        hasher = SHA3_256()
        hasher.update(message[:5])
        hasher.update(message[5:15])
        hasher.update(message[15:])
        hash2 = hasher.hexdigest()

        self.assertEqual(hash1, hash2)

    def test_file_hashing(self):
        """Test file hashing functionality"""
        # Create a test file
        test_content = b"File content for SHA3 hashing test"
        test_file = "test_sha3_file.txt"

        try:
            with open(test_file, 'wb') as f:
                f.write(test_content)

            # Hash using our function
            file_hash = sha3_256(test_content)

            # Hash using file function
            file_hash_from_func = sha3_256_file(test_file)

            self.assertEqual(file_hash, file_hash_from_func)

        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_avalanche_effect(self):
        """Test that changing one bit produces completely different hash"""
        message1 = b"Hello SHA3 World"

        # Convert to bytearray to modify one byte
        msg2_bytes = bytearray(message1)
        msg2_bytes[0] ^= 0x01  # Flip one bit
        message2 = bytes(msg2_bytes)

        hash1 = sha3_256(message1)
        hash2 = sha3_256(message2)

        # Hashes should be completely different
        self.assertNotEqual(hash1, hash2)

        # Count differing bits
        hex1 = int(hash1, 16)
        hex2 = int(hash2, 16)
        diff_bits = bin(hex1 ^ hex2).count('1')

        # Should have significant number of differing bits (avalanche effect)
        self.assertGreater(diff_bits, 100)
        print(f"SHA3-256 Avalanche effect: {diff_bits} bits differ")


if __name__ == '__main__':
    print("Running SHA3-256 tests...")
    unittest.main(verbosity=2)