#!/usr/bin/env python3
"""
HMAC compatibility test with known RFC 4231 vectors
"""

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mac.hmac import hmac_sha256


class TestHMACCompatibility(unittest.TestCase):
    """Test HMAC compatibility with RFC 4231"""

    def test_rfc_4231_test_case_1(self):
        """RFC 4231 Test Case 1"""
        key = bytes([0x0b] * 20)  # 20 bytes of 0x0b
        data = b"Hi There"
        expected = bytes.fromhex("b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")

        result = hmac_sha256(key, data)
        self.assertEqual(result, expected)
        print(f"✅ RFC 4231 Test Case 1 passed")

    def test_rfc_4231_test_case_2(self):
        """RFC 4231 Test Case 2"""
        key = b"Jefe"
        data = b"what do ya want for nothing?"
        expected = bytes.fromhex("5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843")

        result = hmac_sha256(key, data)
        self.assertEqual(result, expected)
        print(f"✅ RFC 4231 Test Case 2 passed")

    def test_hmac_with_different_key_lengths(self):
        """Test HMAC with different key lengths"""
        test_cases = [
            # (key, data, expected_hex)
            (b"", b"", "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad"),
            (b"key", b"The quick brown fox jumps over the lazy dog",
             "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8"),
        ]

        for key, data, expected_hex in test_cases:
            expected = bytes.fromhex(expected_hex)
            result = hmac_sha256(key, data)
            self.assertEqual(result, expected)

        print(f"✅ HMAC with different key lengths passed")


def run_hmac_compatibility_tests():
    """Run HMAC compatibility tests"""
    print("🔐 HMAC RFC 4231 COMPATIBILITY TESTS")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(TestHMACCompatibility('test_rfc_4231_test_case_1'))
    suite.addTest(TestHMACCompatibility('test_rfc_4231_test_case_2'))
    suite.addTest(TestHMACCompatibility('test_hmac_with_different_key_lengths'))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print("📊 HMAC COMPATIBILITY SUMMARY")
    print("=" * 60)

    if result.wasSuccessful():
        print("✅ HMAC IMPLEMENTATION IS RFC 4231 COMPATIBLE")
        print("✅ PBKDF2 WILL NOW PRODUCE CORRECT RFC 6070 RESULTS")
    else:
        print("❌ HMAC IMPLEMENTATION HAS ISSUES")
        print("❌ PBKDF2 MAY NOT PRODUCE CORRECT RESULTS")

    print("=" * 60)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_hmac_compatibility_tests()
    sys.exit(0 if success else 1)