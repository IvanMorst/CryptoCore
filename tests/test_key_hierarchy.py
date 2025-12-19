#!/usr/bin/env python3
"""
Tests for Key Hierarchy implementation - Sprint 7
"""

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from crypto.kdf.key_hierarchy import KeyHierarchy, derive_key


class TestKeyHierarchy(unittest.TestCase):
    """Tests for Key Hierarchy implementation"""

    def setUp(self):
        self.master_key = b'\x00' * 32  # 32-byte master key

    def test_deterministic_output(self):
        """Test that same inputs produce same output"""
        context = "encryption"
        length = 32

        key1 = KeyHierarchy.derive_key(self.master_key, context, length)
        key2 = KeyHierarchy.derive_key(self.master_key, context, length)

        self.assertEqual(key1, key2)
        self.assertEqual(len(key1), length)

    def test_context_separation(self):
        """Test that different contexts produce different keys"""
        length = 32

        key1 = KeyHierarchy.derive_key(self.master_key, "encryption", length)
        key2 = KeyHierarchy.derive_key(self.master_key, "authentication", length)
        key3 = KeyHierarchy.derive_key(self.master_key, "integrity", length)

        # All keys should be different
        self.assertNotEqual(key1, key2)
        self.assertNotEqual(key1, key3)
        self.assertNotEqual(key2, key3)

        # All keys should have correct length
        self.assertEqual(len(key1), length)
        self.assertEqual(len(key2), length)
        self.assertEqual(len(key3), length)

    def test_various_key_lengths(self):
        """Test derivation of various key lengths"""
        context = "test"

        for length in [1, 16, 32, 64, 100, 256]:
            key = KeyHierarchy.derive_key(self.master_key, context, length)
            self.assertEqual(len(key), length)

    def test_derive_keys_function(self):
        """Test derive_keys function for multiple contexts"""
        contexts = ["encryption", "authentication", "mac", "iv"]
        length = 32

        keys = KeyHierarchy.derive_keys(self.master_key, contexts, length)

        # Check all contexts are present
        self.assertEqual(set(keys.keys()), set(contexts))

        # Check all keys have correct length
        for context, key in keys.items():
            self.assertEqual(len(key), length)

        # Check all keys are different
        key_values = list(keys.values())
        for i in range(len(key_values)):
            for j in range(i + 1, len(key_values)):
                self.assertNotEqual(key_values[i], key_values[j])

    def test_convenience_function(self):
        """Test convenience function derive_key"""
        context = "test"
        length = 32

        key = derive_key(self.master_key, context, length)
        self.assertEqual(len(key), length)

    def test_empty_master_key(self):
        """Test with empty master key (should fail)"""
        with self.assertRaises(ValueError):
            KeyHierarchy.derive_key(b'', "test", 32)

    def test_zero_length(self):
        """Test with zero length (should fail)"""
        with self.assertRaises(ValueError):
            KeyHierarchy.derive_key(self.master_key, "test", 0)

    def test_negative_length(self):
        """Test with negative length (should fail)"""
        with self.assertRaises(ValueError):
            KeyHierarchy.derive_key(self.master_key, "test", -1)

    def test_unicode_context(self):
        """Test with Unicode context string"""
        context = "🔒encryption_ключ"
        length = 32

        key = KeyHierarchy.derive_key(self.master_key, context, length)
        self.assertEqual(len(key), length)

    def test_bytes_context(self):
        """Test with bytes context"""
        context = b"encryption_context"
        length = 32

        key = KeyHierarchy.derive_key(self.master_key, context, length)
        self.assertEqual(len(key), length)

    def test_large_key_length(self):
        """Test with large key length"""
        context = "large_key"
        length = 1024  # 1KB key

        key = KeyHierarchy.derive_key(self.master_key, context, length)
        self.assertEqual(len(key), length)
        # Check that key is not all zeros
        self.assertNotEqual(key, b'\x00' * length)

    def test_master_key_variation(self):
        """Test that different master keys produce different derived keys"""
        context = "encryption"
        length = 32

        master_key1 = b'\x01' * 32
        master_key2 = b'\x02' * 32

        key1 = KeyHierarchy.derive_key(master_key1, context, length)
        key2 = KeyHierarchy.derive_key(master_key2, context, length)

        self.assertNotEqual(key1, key2)


def run_comprehensive_tests():
    """Run comprehensive key hierarchy tests"""
    print("Running Key Hierarchy Comprehensive Tests")
    print("=" * 60)

    master_key = b'\x00' * 32
    all_passed = True

    # Test 1: Deterministic output
    try:
        key1 = KeyHierarchy.derive_key(master_key, "test", 32)
        key2 = KeyHierarchy.derive_key(master_key, "test", 32)
        if key1 == key2:
            print("✓ Deterministic output: PASSED")
        else:
            print("✗ Deterministic output: FAILED")
            all_passed = False
    except Exception as e:
        print(f"✗ Deterministic output: ERROR - {e}")
        all_passed = False

    # Test 2: Context separation
    try:
        contexts = ["ctx1", "ctx2", "ctx3"]
        keys = []
        for ctx in contexts:
            keys.append(KeyHierarchy.derive_key(master_key, ctx, 32))

        # Check all unique
        unique_keys = set(keys)
        if len(unique_keys) == len(contexts):
            print("✓ Context separation: PASSED")
        else:
            print("✗ Context separation: FAILED")
            all_passed = False
    except Exception as e:
        print(f"✗ Context separation: ERROR - {e}")
        all_passed = False

    # Test 3: Various lengths
    try:
        lengths = [1, 16, 32, 64, 100]
        for length in lengths:
            key = KeyHierarchy.derive_key(master_key, "test", length)
            if len(key) == length:
                continue
            else:
                print(f"✗ Length test ({length} bytes): FAILED")
                all_passed = False
                break
        else:
            print("✓ Various lengths: PASSED")
    except Exception as e:
        print(f"✗ Various lengths: ERROR - {e}")
        all_passed = False

    print("=" * 60)
    if all_passed:
        print("All key hierarchy tests passed! ✓")
    else:
        print("Some tests failed ✗")

    return all_passed


if __name__ == '__main__':
    # Run comprehensive tests
    comprehensive_passed = run_comprehensive_tests()

    # Run unit tests
    print("\nRunning unit tests...")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestKeyHierarchy)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() and comprehensive_passed else 1)