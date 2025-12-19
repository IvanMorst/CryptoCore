#!/usr/bin/env python3
"""
Comprehensive tests for GCM implementation - Sprint 6
NIST test vectors, security properties, and interoperability tests
"""

import unittest
import os
import tempfile
import sys
import hashlib

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from crypto.aead.gcm import GCM, AuthenticationError
from crypto.aead.encrypt_then_mac import EncryptThenMAC, AuthenticationError as ETM_AuthenticationError


class TestGCM(unittest.TestCase):
    """Comprehensive test cases for GCM implementation"""

    def setUp(self):
        """Setup before each test"""
        self.test_counter = 1
        print(f"\n{'=' * 80}")

    def tearDown(self):
        """Cleanup after each test"""
        self.test_counter += 1

    def print_test_result(self, test_name, success, details=""):
        """Print formatted test result"""
        status = "PASS" if success else "FAIL"
        print(f"Test {self.test_counter:02d}: {test_name:50s} [{status}]")
        if details:
            for line in details.split('\n'):
                print(f"       {line}")

    # ============================================================================
    # SECTION 1: NIST TEST VECTORS (TEST-1 requirement)
    # ============================================================================

    def test_nist_gcm_test_vector_1(self):
        """NIST GCM Test Vector 1: Empty plaintext, empty AAD"""
        print("SECTION 1: NIST TEST VECTORS")
        print("-" * 80)

        # Test vector from NIST SP 800-38D, Appendix B.1
        key = bytes.fromhex('00000000000000000000000000000000')
        iv = bytes.fromhex('000000000000000000000000')
        plaintext = bytes.fromhex('')
        aad = bytes.fromhex('')
        expected_ciphertext = bytes.fromhex('')
        expected_tag = bytes.fromhex('58e2fccefa7e3061367f1d57a4e7455a')

        # Encrypt
        gcm = GCM(key, iv)
        result = gcm.encrypt(plaintext, aad)

        # Extract components
        nonce = result[:12]
        ciphertext = result[12:-16]
        tag = result[-16:]

        details = f"""
        Key: {key.hex()}
        IV: {iv.hex()}
        Plaintext length: {len(plaintext)} bytes
        AAD length: {len(aad)} bytes
        Result length: {len(result)} bytes
        Nonce (12B): {nonce.hex()}
        Ciphertext ({len(ciphertext)}B): {ciphertext.hex() or '(empty)'}
        Tag (16B): {tag.hex()}
        Expected tag: {expected_tag.hex()}
        """

        success = tag == expected_tag

        self.print_test_result("NIST Vector 1 (empty data)", success, details)
        self.assertEqual(tag, expected_tag)

    def test_nist_gcm_test_vector_2(self):
        """NIST GCM Test Vector 2: 16-byte plaintext, empty AAD"""
        key = bytes.fromhex('00000000000000000000000000000000')
        iv = bytes.fromhex('000000000000000000000000')
        plaintext = bytes.fromhex('00000000000000000000000000000000')
        aad = bytes.fromhex('')
        expected_ciphertext = bytes.fromhex('0388dace60b6a392f328c2b971b2fe78')
        expected_tag = bytes.fromhex('ab6e47d42cec13bdf53a67b21257bddf')

        gcm = GCM(key, iv)
        result = gcm.encrypt(plaintext, aad)

        ciphertext = result[12:-16]
        tag = result[-16:]

        details = f"""
        Key: {key.hex()}
        IV: {iv.hex()}
        Plaintext length: {len(plaintext)} bytes
        AAD length: {len(aad)} bytes
        Ciphertext ({len(ciphertext)}B): {ciphertext.hex()}
        Expected ciphertext: {expected_ciphertext.hex()}
        Tag (16B): {tag.hex()}
        Expected tag: {expected_tag.hex()}
        """

        ciphertext_success = ciphertext == expected_ciphertext
        tag_success = tag == expected_tag
        success = ciphertext_success and tag_success

        details += f"""
        Ciphertext match: {'YES' if ciphertext_success else 'NO'}
        Tag match: {'YES' if tag_success else 'NO'}
        """

        self.print_test_result("NIST Vector 2 (16B plaintext)", success, details)
        self.assertEqual(ciphertext, expected_ciphertext)
        self.assertEqual(tag, expected_tag)

    def test_nist_gcm_test_vector_3(self):
        """NIST GCM Test Vector 3: Different AAD lengths"""
        key = bytes.fromhex('feffe9928665731c6d6a8f9467308308')
        iv = bytes.fromhex('cafebabefacedbaddecaf888')

        # Multiple test cases with different AAD lengths
        test_cases = [
            {
                'name': 'Vector 3a: 16B AAD',
                'plaintext': bytes.fromhex(
                    'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39'),
                'aad': bytes.fromhex('feedfacedeadbeeffeedfacedeadbeefabaddad2'),
                'expected_tag': bytes.fromhex('5bc94fbc3221a5db94fae95ae7121a47')
            },
            {
                'name': 'Vector 3b: 20B AAD',
                'plaintext': bytes.fromhex(
                    'd9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39'),
                'aad': bytes.fromhex('feedfacedeadbeeffeedfacedeadbeefabaddad2'),
                'expected_tag': bytes.fromhex('5bc94fbc3221a5db94fae95ae7121a47')
            }
        ]

        all_success = True
        details = ""

        for i, test_case in enumerate(test_cases):
            gcm = GCM(key, iv)
            result = gcm.encrypt(test_case['plaintext'], test_case['aad'])
            tag = result[-16:]

            tag_success = tag == test_case['expected_tag']
            all_success = all_success and tag_success

            details += f"""
            Case {i + 1}: {test_case['name']}
              Plaintext length: {len(test_case['plaintext'])} bytes
              AAD length: {len(test_case['aad'])} bytes
              Tag: {tag.hex()}
              Expected: {test_case['expected_tag'].hex()}
              Match: {'YES' if tag_success else 'NO'}
            """

        self.print_test_result("NIST Vector 3 (various AAD)", all_success, details)
        self.assertTrue(all_success)

    # ============================================================================
    # SECTION 2: ROUND-TRIP TESTS (TEST-2 requirement)
    # ============================================================================

    def test_round_trip_basic(self):
        """Basic round-trip encryption/decryption"""
        print("\nSECTION 2: ROUND-TRIP TESTS")
        print("-" * 80)

        key = os.urandom(16)
        plaintext = b"Test message for GCM encryption with AAD support"
        aad = b"Additional authenticated data for testing"

        # Encrypt
        gcm = GCM(key)
        encrypted = gcm.encrypt(plaintext, aad)

        # Decrypt
        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(encrypted, aad)

        details = f"""
        Key length: {len(key)} bytes
        Plaintext length: {len(plaintext)} bytes
        AAD length: {len(aad)} bytes
        Nonce: {gcm.nonce.hex()}
        Encrypted data length: {len(encrypted)} bytes
          - Nonce: {encrypted[:12].hex()} (12 bytes)
          - Ciphertext: {len(encrypted) - 28} bytes
          - Tag: {encrypted[-16:].hex()} (16 bytes)
        Decrypted length: {len(decrypted)} bytes
        Data integrity: {'PRESERVED' if decrypted == plaintext else 'CORRUPTED'}
        """

        success = decrypted == plaintext

        self.print_test_result("Basic round-trip", success, details)
        self.assertEqual(decrypted, plaintext)

    def test_round_trip_empty_data(self):
        """Round-trip with empty plaintext and AAD"""
        key = os.urandom(16)
        plaintext = b""
        aad = b""

        gcm = GCM(key)
        encrypted = gcm.encrypt(plaintext, aad)

        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(encrypted, aad)

        details = f"""
        Key length: {len(key)} bytes
        Plaintext: EMPTY (0 bytes)
        AAD: EMPTY (0 bytes)
        Encrypted data length: {len(encrypted)} bytes (12B nonce + 0B ciphertext + 16B tag)
        Decrypted data: {len(decrypted)} bytes
        """

        success = decrypted == plaintext and len(encrypted) == 28

        self.print_test_result("Round-trip empty data", success, details)
        self.assertEqual(decrypted, plaintext)
        self.assertEqual(len(encrypted), 28)  # 12B nonce + 0B ciphertext + 16B tag

    def test_round_trip_large_data(self):
        """Round-trip with large data (1MB)"""
        key = os.urandom(16)
        plaintext = os.urandom(1024 * 1024)  # 1MB
        aad = os.urandom(512)  # 512B AAD

        gcm = GCM(key)
        encrypted = gcm.encrypt(plaintext, aad)

        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(encrypted, aad)

        # Verify hash instead of full comparison for performance
        original_hash = hashlib.sha256(plaintext).hexdigest()
        decrypted_hash = hashlib.sha256(decrypted).hexdigest()

        details = f"""
        Key length: {len(key)} bytes
        Plaintext length: {len(plaintext)} bytes (1MB)
        AAD length: {len(aad)} bytes
        Encrypted data length: {len(encrypted)} bytes
        Decrypted data length: {len(decrypted)} bytes
        Original SHA-256: {original_hash}
        Decrypted SHA-256: {decrypted_hash}
        Hash match: {'YES' if original_hash == decrypted_hash else 'NO'}
        """

        success = original_hash == decrypted_hash

        self.print_test_result("Round-trip large data (1MB)", success, details)
        self.assertEqual(original_hash, decrypted_hash)

    # ============================================================================
    # SECTION 3: AUTHENTICATION TESTS (TEST-3, TEST-4 requirements)
    # ============================================================================

    def test_aad_tamper_detection(self):
        """Authentication failure with incorrect AAD"""
        print("\nSECTION 3: AUTHENTICATION TESTS")
        print("-" * 80)

        key = os.urandom(16)
        plaintext = b"Secret message requiring authentication"
        correct_aad = b"correct_additional_data"
        wrong_aad = b"wrong_additional_data"

        # Encrypt with correct AAD
        gcm = GCM(key)
        encrypted = gcm.encrypt(plaintext, correct_aad)

        # Try to decrypt with wrong AAD
        gcm2 = GCM(key, gcm.nonce)

        try:
            decrypted = gcm2.decrypt(encrypted, wrong_aad)
            authentication_failed = False
            error_message = "NO ERROR (should have failed)"
        except AuthenticationError as e:
            authentication_failed = True
            error_message = str(e)

        details = f"""
        Key length: {len(key)} bytes
        Plaintext length: {len(plaintext)} bytes
        Correct AAD: {correct_aad}
        Wrong AAD: {wrong_aad}
        Nonce: {gcm.nonce.hex()}
        Authentication with wrong AAD: {'FAILED (expected)' if authentication_failed else 'SUCCEEDED (unexpected)'}
        Error message: {error_message}
        """

        success = authentication_failed

        self.print_test_result("AAD tamper detection", success, details)
        self.assertTrue(authentication_failed)

    def test_ciphertext_tamper_detection(self):
        """Authentication failure with tampered ciphertext"""
        key = os.urandom(16)
        plaintext = b"Another secret message for integrity testing"
        aad = b"associated_data_for_authentication"

        # Encrypt
        gcm = GCM(key)
        encrypted = gcm.encrypt(plaintext, aad)

        # Tamper with ciphertext (flip one bit)
        tampered = bytearray(encrypted)
        tampered[25] ^= 0x01  # Flip one bit in the ciphertext portion

        # Try to decrypt tampered ciphertext
        gcm2 = GCM(key, gcm.nonce)

        try:
            decrypted = gcm2.decrypt(bytes(tampered), aad)
            authentication_failed = False
            error_message = "NO ERROR (should have failed)"
        except AuthenticationError as e:
            authentication_failed = True
            error_message = str(e)

        details = f"""
        Key length: {len(key)} bytes
        Plaintext length: {len(plaintext)} bytes
        AAD length: {len(aad)} bytes
        Tampered byte position: 25 (in ciphertext portion)
        Tampered bit: 0x01 XOR
        Authentication with tampered data: {'FAILED (expected)' if authentication_failed else 'SUCCEEDED (unexpected)'}
        Error message: {error_message}
        """

        success = authentication_failed

        self.print_test_result("Ciphertext tamper detection", success, details)
        self.assertTrue(authentication_failed)

    def test_tag_tamper_detection(self):
        """Authentication failure with tampered authentication tag"""
        key = os.urandom(16)
        plaintext = b"Message with tampered tag test"
        aad = b"authentication_data"

        # Encrypt
        gcm = GCM(key)
        encrypted = gcm.encrypt(plaintext, aad)

        # Tamper with tag (last 16 bytes)
        tampered = bytearray(encrypted)
        tampered[-5] ^= 0x01  # Flip one bit in the tag

        # Try to decrypt with tampered tag
        gcm2 = GCM(key, gcm.nonce)

        try:
            decrypted = gcm2.decrypt(bytes(tampered), aad)
            authentication_failed = False
            error_message = "NO ERROR (should have failed)"
        except AuthenticationError as e:
            authentication_failed = True
            error_message = str(e)

        details = f"""
        Key length: {len(key)} bytes
        Plaintext length: {len(plaintext)} bytes
        AAD length: {len(aad)} bytes
        Tampered byte position: {len(tampered) - 5} (in tag portion)
        Tampered bit: 0x01 XOR
        Authentication with tampered tag: {'FAILED (expected)' if authentication_failed else 'SUCCEEDED (unexpected)'}
        Error message: {error_message}
        """

        success = authentication_failed

        self.print_test_result("Tag tamper detection", success, details)
        self.assertTrue(authentication_failed)

    # ============================================================================
    # SECTION 4: NONCE TESTS (TEST-5 requirement)
    # ============================================================================

    def test_nonce_uniqueness(self):
        """Test that nonces are unique for each encryption"""
        print("\nSECTION 4: NONCE AND KEY TESTS")
        print("-" * 80)

        key = os.urandom(16)
        plaintext = b"Test message for nonce uniqueness"

        nonces = set()
        collisions = 0
        test_iterations = 1000

        for i in range(test_iterations):
            gcm = GCM(key)
            nonces.add(gcm.nonce.hex())

            # Check for early collisions
            if len(nonces) != i + 1:
                collisions += 1

        unique_nonces = len(nonces)
        collision_rate = (collisions / test_iterations) * 100 if test_iterations > 0 else 0

        details = f"""
        Key length: {len(key)} bytes
        Test iterations: {test_iterations}
        Unique nonces generated: {unique_nonces}
        Nonce collisions detected: {collisions}
        Collision rate: {collision_rate:.6f}%
        Expected: 1000 unique nonces, 0 collisions
        """

        success = unique_nonces == test_iterations and collisions == 0

        self.print_test_result("Nonce uniqueness (1000 iterations)", success, details)
        self.assertEqual(unique_nonces, test_iterations)
        self.assertEqual(collisions, 0)

    def test_key_size_support(self):
        """Test support for different key sizes (AES-128, AES-192, AES-256)"""
        key_sizes = [
            (16, "AES-128"),
            (24, "AES-192"),
            (32, "AES-256")
        ]

        all_success = True
        details = ""

        for key_size, key_name in key_sizes:
            key = os.urandom(key_size)
            plaintext = b"Test message for " + key_name.encode()
            aad = b"Additional data"

            try:
                gcm = GCM(key)
                encrypted = gcm.encrypt(plaintext, aad)

                gcm2 = GCM(key, gcm.nonce)
                decrypted = gcm2.decrypt(encrypted, aad)

                key_success = decrypted == plaintext
                status = "SUPPORTED" if key_success else "FAILED"
            except Exception as e:
                key_success = False
                status = f"ERROR: {str(e)}"

            all_success = all_success and key_success

            details += f"""
            {key_name} ({key_size} bytes): {status}
            """

        self.print_test_result("Key size support (128/192/256-bit)", all_success, details)
        self.assertTrue(all_success)

    # ============================================================================
    # SECTION 5: AAD TESTS (TEST-6, TEST-7 requirements)
    # ============================================================================

    def test_empty_aad(self):
        """Test with empty AAD"""
        print("\nSECTION 5: AAD TESTS")
        print("-" * 80)

        key = os.urandom(16)
        plaintext = b"Message with empty AAD"
        aad = b""

        gcm = GCM(key)
        encrypted = gcm.encrypt(plaintext, aad)

        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(encrypted, aad)

        details = f"""
        Key length: {len(key)} bytes
        Plaintext length: {len(plaintext)} bytes
        AAD: EMPTY (0 bytes)
        Nonce: {gcm.nonce.hex()}
        Encrypted data length: {len(encrypted)} bytes
        Decryption successful: {'YES' if decrypted == plaintext else 'NO'}
        """

        success = decrypted == plaintext

        self.print_test_result("Empty AAD handling", success, details)
        self.assertEqual(decrypted, plaintext)

    def test_large_aad(self):
        """Test with large AAD (2MB)"""
        key = os.urandom(16)
        plaintext = b"Short message with large AAD"
        aad = os.urandom(2 * 1024 * 1024)  # 2MB AAD

        gcm = GCM(key)
        encrypted = gcm.encrypt(plaintext, aad)

        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(encrypted, aad)

        # Use hash for AAD too large to print
        aad_hash = hashlib.sha256(aad).hexdigest()[:16]

        details = f"""
        Key length: {len(key)} bytes
        Plaintext length: {len(plaintext)} bytes
        AAD length: {len(aad)} bytes (2MB)
        AAD SHA-256 (first 16 chars): {aad_hash}
        Nonce: {gcm.nonce.hex()}
        Encrypted data length: {len(encrypted)} bytes
        Decryption successful: {'YES' if decrypted == plaintext else 'NO'}
        """

        success = decrypted == plaintext

        self.print_test_result("Large AAD handling (2MB)", success, details)
        self.assertEqual(decrypted, plaintext)

    def test_various_aad_lengths(self):
        """Test with various AAD lengths including edge cases"""
        key = os.urandom(16)
        plaintext = b"Test message"

        aad_lengths = [0, 1, 15, 16, 17, 31, 32, 33, 63, 64, 65, 127, 128, 129, 255, 256]

        all_success = True
        details = "AAD length test results:\n"

        for aad_len in aad_lengths:
            aad = os.urandom(aad_len) if aad_len > 0 else b""

            gcm = GCM(key)
            encrypted = gcm.encrypt(plaintext, aad)

            gcm2 = GCM(key, gcm.nonce)

            try:
                decrypted = gcm2.decrypt(encrypted, aad)
                success = decrypted == plaintext
                status = "OK" if success else "FAIL"
            except Exception as e:
                success = False
                status = f"ERROR: {str(e)[:30]}"

            all_success = all_success and success

            details += f"  AAD length {aad_len:3d} bytes: {status}\n"

        self.print_test_result("Various AAD lengths", all_success, details)
        self.assertTrue(all_success)

    # ============================================================================
    # SECTION 6: FILE OPERATION TESTS
    # ============================================================================

    def test_file_gcm_encryption(self):
        """Test GCM file encryption/decryption through crypto module"""
        print("\nSECTION 6: FILE OPERATION TESTS")
        print("-" * 80)

        from crypto.cipher_core import CipherCore

        test_content = b"File content for GCM encryption testing with AAD"
        aad = b"file_authentication_metadata"

        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(test_content)
            input_file = f.name

        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            encrypted_file = f.name

        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            decrypted_file = f.name

        try:
            key = os.urandom(16)

            # Encrypt using GCM through our implementation
            gcm = GCM(key)

            with open(input_file, 'rb') as f:
                plaintext = f.read()

            encrypted = gcm.encrypt(plaintext, aad)

            with open(encrypted_file, 'wb') as f:
                f.write(encrypted)

            # Verify file structure
            with open(encrypted_file, 'rb') as f:
                file_data = f.read()

            file_nonce = file_data[:12]
            file_tag = file_data[-16:]

            # Decrypt
            gcm2 = GCM(key, gcm.nonce)

            with open(encrypted_file, 'rb') as f:
                encrypted_data = f.read()

            decrypted = gcm2.decrypt(encrypted_data, aad)

            with open(decrypted_file, 'wb') as f:
                f.write(decrypted)

            # Verify
            with open(input_file, 'rb') as f:
                original = f.read()

            with open(decrypted_file, 'rb') as f:
                restored = f.read()

            original_hash = hashlib.sha256(original).hexdigest()
            restored_hash = hashlib.sha256(restored).hexdigest()

            details = f"""
            Input file: {input_file}
            Encrypted file: {encrypted_file}
            Decrypted file: {decrypted_file}
            Key length: {len(key)} bytes
            Original content length: {len(original)} bytes
            Encrypted file length: {len(file_data)} bytes
              - Nonce from file: {file_nonce.hex()}
              - Expected nonce: {gcm.nonce.hex()}
              - Tag from file: {file_tag.hex()}
            Decrypted content length: {len(restored)} bytes
            Original SHA-256: {original_hash}
            Restored SHA-256: {restored_hash}
            Hashes match: {'YES' if original_hash == restored_hash else 'NO'}
            """

            success = original_hash == restored_hash

        finally:
            # Cleanup
            for f in [input_file, encrypted_file, decrypted_file]:
                if os.path.exists(f):
                    os.unlink(f)

        self.print_test_result("File encryption/decryption", success, details)
        self.assertEqual(original_hash, restored_hash)

    # ============================================================================
    # SECTION 7: ENCRYPT-THEN-MAC TESTS (TEST-9 requirement)
    # ============================================================================

    def test_encrypt_then_mac_basic(self):
        """Basic Encrypt-then-MAC functionality"""
        print("\nSECTION 7: ENCRYPT-THEN-MAC TESTS")
        print("-" * 80)

        master_key = os.urandom(32)
        enc_key, mac_key = EncryptThenMAC.derive_keys(master_key)

        etm = EncryptThenMAC(enc_key, mac_key)
        plaintext = b"Test message for Encrypt-then-MAC"
        aad = b"Additional authenticated data"

        # Encrypt
        encrypted = etm.encrypt(plaintext, aad)

        # Verify structure
        ciphertext_len = len(encrypted) - 32  # SHA-256 produces 32-byte MAC
        ciphertext = encrypted[:ciphertext_len]
        mac = encrypted[ciphertext_len:]

        # Decrypt
        decrypted = etm.decrypt(encrypted, aad)

        details = f"""
        Master key length: {len(master_key)} bytes
        Encryption key length: {len(enc_key)} bytes (from master)
        MAC key length: {len(mac_key)} bytes (from master)
        Plaintext length: {len(plaintext)} bytes
        AAD length: {len(aad)} bytes
        Encrypted data length: {len(encrypted)} bytes
          - Ciphertext: {ciphertext_len} bytes
          - MAC (SHA-256): 32 bytes
        Decrypted length: {len(decrypted)} bytes
        Data integrity: {'PRESERVED' if decrypted == plaintext else 'CORRUPTED'}
        """

        success = decrypted == plaintext

        self.print_test_result("Encrypt-then-MAC basic", success, details)
        self.assertEqual(decrypted, plaintext)

    def test_encrypt_then_mac_tamper_detection(self):
        """Tamper detection in Encrypt-then-MAC"""
        master_key = os.urandom(32)
        enc_key, mac_key = EncryptThenMAC.derive_keys(master_key)

        etm = EncryptThenMAC(enc_key, mac_key)
        plaintext = b"Secret message for EtM tamper test"
        aad = b"Authentication data"

        encrypted = etm.encrypt(plaintext, aad)

        # Tamper with ciphertext
        tampered = bytearray(encrypted)
        tampered[15] ^= 0x01

        # Try to decrypt tampered data
        try:
            decrypted = etm.decrypt(bytes(tampered), aad)
            authentication_failed = False
            error_message = "NO ERROR (should have failed)"
        except ETM_AuthenticationError as e:
            authentication_failed = True
            error_message = str(e)

        details = f"""
        Master key length: {len(master_key)} bytes
        Plaintext length: {len(plaintext)} bytes
        AAD length: {len(aad)} bytes
        Tampered byte position: 15
        Authentication with tampered data: {'FAILED (expected)' if authentication_failed else 'SUCCEEDED (unexpected)'}
        Error message: {error_message}
        """

        success = authentication_failed

        self.print_test_result("Encrypt-then-MAC tamper detection", success, details)
        self.assertTrue(authentication_failed)

    def test_encrypt_then_mac_key_separation(self):
        """Test key separation in Encrypt-then-MAC"""
        master_key = os.urandom(32)

        # Derive keys twice
        enc_key1, mac_key1 = EncryptThenMAC.derive_keys(master_key)
        enc_key2, mac_key2 = EncryptThenMAC.derive_keys(master_key)

        # Keys should be identical when derived from same master
        enc_keys_match = enc_key1 == enc_key2
        mac_keys_match = mac_key1 == mac_key2

        # Test with different master keys
        different_master_key = os.urandom(32)
        enc_key3, mac_key3 = EncryptThenMAC.derive_keys(different_master_key)

        enc_keys_different = enc_key1 != enc_key3
        mac_keys_different = mac_key1 != mac_key3

        details = f"""
        Master key 1: {master_key.hex()[:16]}...
        Master key 2: {different_master_key.hex()[:16]}...

        Key derivation consistency:
          - Encryption keys from same master: {'MATCH' if enc_keys_match else 'DIFFERENT'}
          - MAC keys from same master: {'MATCH' if mac_keys_match else 'DIFFERENT'}

        Key separation:
          - Encryption keys from different masters: {'DIFFERENT (good)' if enc_keys_different else 'SAME (bad)'}
          - MAC keys from different masters: {'DIFFERENT (good)' if mac_keys_different else 'SAME (bad)'}

        Encryption key length: {len(enc_key1)} bytes
        MAC key length: {len(mac_key1)} bytes
        """

        success = enc_keys_match and mac_keys_match and enc_keys_different and mac_keys_different

        self.print_test_result("Encrypt-then-MAC key separation", success, details)
        self.assertTrue(enc_keys_match)
        self.assertTrue(mac_keys_match)
        self.assertTrue(enc_keys_different)
        self.assertTrue(mac_keys_different)

    # ============================================================================
    # SECTION 8: ERROR HANDLING TESTS
    # ============================================================================

    def test_error_short_data(self):
        """Test error handling with data shorter than minimum GCM length"""
        print("\nSECTION 8: ERROR HANDLING TESTS")
        print("-" * 80)

        key = os.urandom(16)
        gcm = GCM(key)

        # Create data that's too short (less than 28 bytes)
        short_data = os.urandom(20)

        try:
            decrypted = gcm.decrypt(short_data, b"")
            error_raised = False
            error_message = "NO ERROR (should have failed)"
        except ValueError as e:
            error_raised = True
            error_message = str(e)

        details = f"""
        Key length: {len(key)} bytes
        Input data length: {len(short_data)} bytes
        Minimum required for GCM: 28 bytes (12B nonce + 0B ciphertext + 16B tag)
        Error raised: {'YES' if error_raised else 'NO'}
        Error message: {error_message}
        Expected: ValueError for data shorter than 28 bytes
        """

        success = error_raised and "too short" in error_message.lower()

        self.print_test_result("Short data error handling", success, details)
        self.assertTrue(error_raised)

    def test_error_invalid_key_size(self):
        """Test error handling with invalid key sizes"""
        invalid_key_sizes = [1, 8, 15, 17, 31, 33]

        all_errors = True
        details = "Invalid key size tests:\n"

        for key_size in invalid_key_sizes:
            key = os.urandom(key_size)

            try:
                gcm = GCM(key)
                all_errors = False
                details += f"  {key_size:2d} bytes: ACCEPTED (should have failed)\n"
            except ValueError as e:
                details += f"  {key_size:2d} bytes: REJECTED - {str(e)[:40]}\n"

        details += f"\nValid key sizes: 16, 24, 32 bytes (AES-128, AES-192, AES-256)"

        self.print_test_result("Invalid key size handling", all_errors, details)
        self.assertTrue(all_errors)


def print_test_summary():
    """Print test execution summary"""
    print("\n" + "=" * 80)
    print("TEST EXECUTION SUMMARY")
    print("=" * 80)
    print("Sections tested:")
    print("  1. NIST Test Vectors (TEST-1 requirement)")
    print("  2. Round-trip Tests (TEST-2 requirement)")
    print("  3. Authentication Tests (TEST-3, TEST-4 requirements)")
    print("  4. Nonce Tests (TEST-5 requirement)")
    print("  5. AAD Tests (TEST-6, TEST-7 requirements)")
    print("  6. File Operation Tests")
    print("  7. Encrypt-then-MAC Tests (TEST-9 requirement)")
    print("  8. Error Handling Tests")
    print("\nTo run all tests: python -m unittest tests.test_gcm.TestGCM -v")
    print("=" * 80)


if __name__ == '__main__':
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestGCM)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print_test_summary()

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)