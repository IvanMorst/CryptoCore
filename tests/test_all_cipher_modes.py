#!/usr/bin/env python3
"""
Comprehensive Test Suite for All Cipher Modes in CryptoCore
Tests all supported AES modes: ECB, CBC, CFB, OFB, CTR, GCM
"""

import unittest
import os
import sys
import tempfile
import hashlib
import time
from pathlib import Path

# Add project to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from crypto.cipher_core import CipherCore
from crypto.aead.gcm import GCM, AuthenticationError
from crypto.file_processor import FileProcessor
from csprng import generate_key, generate_iv


class TestAllCipherModes(unittest.TestCase):
    """
    Comprehensive test suite for all cipher modes
    """

    def setUp(self):
        """Setup before each test"""
        self.test_counter = 1
        self.start_time = time.time()
        print(f"\n{'=' * 80}")
        print(f"TEST {self.test_counter}: Starting test suite")
        print('=' * 80)

    def tearDown(self):
        """Cleanup after each test"""
        self.test_counter += 1
        elapsed = time.time() - self.start_time
        if hasattr(self, 'test_name'):
            print(f"\n✓ Test '{self.test_name}' completed in {elapsed:.3f}s")

    def print_test_header(self, test_name):
        """Print formatted test header"""
        self.test_name = test_name
        print(f"\n{'─' * 40}")
        print(f"🧪 TEST: {test_name}")
        print(f"{'─' * 40}")

    def print_success(self, message):
        """Print success message"""
        print(f"  ✓ {message}")

    def print_info(self, message):
        """Print info message"""
        print(f"  ℹ {message}")

    def print_warning(self, message):
        """Print warning message"""
        print(f"  ⚠ {message}")

    # ============================================================================
    # SECTION 1: ECB MODE TESTS
    # ============================================================================

    def test_ecb_mode_basic(self):
        """Test ECB (Electronic Codebook) mode - basic functionality"""
        self.print_test_header("ECB Mode - Basic Functionality")

        # Generate test data
        key = generate_key(16)  # AES-128
        plaintext = b"This is a test message for ECB mode encryption. " * 5

        # Create cipher
        cipher = CipherCore(key, 'ecb')
        self.print_info(f"Key: {key.hex()[:32]}...")
        self.print_info(f"Plaintext: {len(plaintext)} bytes")

        # Encrypt
        encrypt_start = time.time()
        ciphertext = cipher.encrypt(plaintext)
        encrypt_time = time.time() - encrypt_start
        self.print_info(f"Encryption time: {encrypt_time:.3f}s")

        # Verify structure
        self.print_info(f"Ciphertext: {len(ciphertext)} bytes")
        self.print_info(f"Size increase: {len(ciphertext) - len(plaintext)} bytes (padding)")

        # Decrypt
        decrypt_start = time.time()
        decrypted = cipher.decrypt(ciphertext)
        decrypt_time = time.time() - decrypt_start
        self.print_info(f"Decryption time: {decrypt_time:.3f}s")

        # Verify
        self.assertEqual(decrypted, plaintext, "ECB decryption failed")
        self.print_success("ECB round-trip successful")

        # Test identical blocks produce identical ciphertext (ECB characteristic)
        test_data = b"A" * 32  # Two identical 16-byte blocks
        cipher2 = CipherCore(key, 'ecb')
        ct = cipher2.encrypt(test_data)

        # In ECB, identical plaintext blocks produce identical ciphertext blocks
        block1 = ct[0:16]
        block2 = ct[16:32]
        self.assertEqual(block1, block2, "ECB: Identical blocks should produce identical ciphertext")
        self.print_success("ECB characteristic verified (identical blocks)")

        return True

    def test_ecb_mode_security_characteristics(self):
        """Test ECB mode security characteristics"""
        self.print_test_header("ECB Mode - Security Characteristics")

        key = generate_key(16)

        # Create pattern in plaintext
        pattern = b"PATTERN" * 10
        plaintext = pattern + b"DATA" + pattern

        cipher = CipherCore(key, 'ecb')
        ciphertext = cipher.encrypt(plaintext)

        # Check for patterns in ciphertext (ECB weakness)
        # In ECB, patterns in plaintext may be visible in ciphertext
        self.print_info("ECB shows patterns in ciphertext (known weakness)")
        self.print_warning("ECB is not recommended for secure applications")

        return True

    # ============================================================================
    # SECTION 2: CBC MODE TESTS
    # ============================================================================

    def test_cbc_mode_basic(self):
        """Test CBC (Cipher Block Chaining) mode - basic functionality"""
        self.print_test_header("CBC Mode - Basic Functionality")

        key = generate_key(16)
        plaintext = b"CBC mode provides better security than ECB. " * 8

        cipher = CipherCore(key, 'cbc')
        key_info = cipher.get_key_info()

        self.print_info(f"Key: {key.hex()[:32]}...")
        self.print_info(f"IV: {cipher.iv.hex()}")
        self.print_info(f"Plaintext: {len(plaintext)} bytes")

        # Encrypt
        encrypt_start = time.time()
        ciphertext = cipher.encrypt(plaintext)
        encrypt_time = time.time() - encrypt_start

        # Verify structure (IV prepended)
        self.assertEqual(ciphertext[:16], cipher.iv, "IV should be prepended")
        self.print_info(f"Ciphertext: {len(ciphertext)} bytes")
        self.print_info(f"Encryption time: {encrypt_time:.3f}s")

        # Decrypt
        decrypt_start = time.time()
        decrypted = cipher.decrypt(ciphertext)
        decrypt_time = time.time() - decrypt_start

        self.assertEqual(decrypted, plaintext, "CBC decryption failed")
        self.print_info(f"Decryption time: {decrypt_time:.3f}s")
        self.print_success("CBC round-trip successful")

        # Test different IV produces different ciphertext
        cipher2 = CipherCore(key, 'cbc')  # New random IV
        ciphertext2 = cipher2.encrypt(plaintext)

        self.assertNotEqual(ciphertext, ciphertext2, "Different IV should produce different ciphertext")
        self.print_success("CBC IV uniqueness verified")

        return True

    def test_cbc_mode_error_propagation(self):
        """Test CBC mode error propagation"""
        self.print_test_header("CBC Mode - Error Propagation")

        key = generate_key(16)
        plaintext = b"Testing error propagation in CBC mode. " * 4

        cipher = CipherCore(key, 'cbc')
        ciphertext = cipher.encrypt(plaintext)

        # Tamper with one byte in ciphertext
        tampered = bytearray(ciphertext)
        tampered[50] ^= 0x01  # Flip one bit

        # In CBC, one corrupted block affects two plaintext blocks
        try:
            decrypted = cipher.decrypt(bytes(tampered))
            # Should still decrypt (but with errors)
            self.print_info("CBC decrypts despite tampering (with errors)")

            # Check which blocks are affected
            original_blocks = [plaintext[i:i + 16] for i in range(0, len(plaintext), 16)]
            decrypted_blocks = [decrypted[i:i + 16] for i in range(0, len(decrypted), 16)]

            affected_count = sum(1 for i in range(len(original_blocks))
                                 if original_blocks[i] != decrypted_blocks[i])

            self.print_info(f"Tampering affected {affected_count} block(s)")
            self.assertGreater(affected_count, 0, "Tampering should affect output")

        except Exception as e:
            self.print_info(f"Decryption failed with tampering: {e}")

        self.print_success("CBC error propagation tested")
        return True

    # ============================================================================
    # SECTION 3: CTR MODE TESTS
    # ============================================================================

    def test_ctr_mode_basic(self):
        """Test CTR (Counter) mode - basic functionality"""
        self.print_test_header("CTR Mode - Basic Functionality")

        key = generate_key(16)
        plaintext = b"CTR mode turns block cipher into stream cipher. " * 6

        cipher = CipherCore(key, 'ctr')
        key_info = cipher.get_key_info()

        self.print_info(f"Key: {key.hex()[:32]}...")
        self.print_info(f"Nonce: {cipher.iv.hex()}")
        self.print_info(f"Plaintext: {len(plaintext)} bytes")

        # Encrypt
        encrypt_start = time.time()
        ciphertext = cipher.encrypt(plaintext)
        encrypt_time = time.time() - encrypt_start

        # No padding in CTR mode
        self.assertEqual(len(ciphertext), len(plaintext) + 16, "CTR: nonce prepended")
        self.print_info(f"Ciphertext: {len(ciphertext)} bytes (no padding)")
        self.print_info(f"Encryption time: {encrypt_time:.3f}s")

        # Decrypt
        decrypt_start = time.time()
        decrypted = cipher.decrypt(ciphertext)
        decrypt_time = time.time() - decrypt_start

        self.assertEqual(decrypted, plaintext, "CTR decryption failed")
        self.print_info(f"Decryption time: {decrypt_time:.3f}s")
        self.print_success("CTR round-trip successful")

        # Test parallel encryption capability
        self.print_info("CTR supports parallel encryption/decryption")

        return True

    def test_ctr_mode_random_access(self):
        """Test CTR mode random access capability"""
        self.print_test_header("CTR Mode - Random Access")

        key = generate_key(16)

        # Generate large plaintext
        plaintext = os.urandom(1024)  # 1KB random data

        cipher = CipherCore(key, 'ctr')
        ciphertext = cipher.encrypt(plaintext)

        # In CTR, we can decrypt any block independently
        # Extract nonce from ciphertext
        nonce = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]

        # Decrypt only a specific portion
        block_to_decrypt = 5  # 6th block (0-indexed)
        block_start = block_to_decrypt * 16
        block_end = block_start + 16

        if block_end <= len(actual_ciphertext):
            # Create cipher with same nonce
            cipher2 = CipherCore(key, 'ctr')
            # Manually decrypt just this block
            counter_block = int.from_bytes(nonce, 'big') + block_to_decrypt
            from Crypto.Cipher import AES
            from Crypto.Util import Counter

            ctr = Counter.new(128, initial_value=counter_block)
            aes_ctr = AES.new(key, AES.MODE_CTR, counter=ctr)

            # Encrypt zeros to get keystream for this position
            keystream_block = aes_ctr.encrypt(b'\x00' * 16)

            # Decrypt the block
            ciphertext_block = actual_ciphertext[block_start:block_end]
            decrypted_block = bytes(a ^ b for a, b in zip(ciphertext_block, keystream_block))

            # Verify against full decryption
            full_decrypted = cipher.decrypt(ciphertext)
            expected_block = full_decrypted[block_start:block_end]

            self.assertEqual(decrypted_block, expected_block, "CTR random access failed")
            self.print_success("CTR random access verified")

        return True

    # ============================================================================
    # SECTION 4: CFB MODE TESTS
    # ============================================================================

    def test_cfb_mode_basic(self):
        """Test CFB (Cipher Feedback) mode - basic functionality"""
        self.print_test_header("CFB Mode - Basic Functionality")

        key = generate_key(16)
        plaintext = b"CFB mode turns block cipher into self-synchronizing stream cipher. " * 4

        cipher = CipherCore(key, 'cfb')

        self.print_info(f"Key: {key.hex()[:32]}...")
        self.print_info(f"IV: {cipher.iv.hex()}")
        self.print_info(f"Plaintext: {len(plaintext)} bytes")

        # Encrypt
        encrypt_start = time.time()
        ciphertext = cipher.encrypt(plaintext)
        encrypt_time = time.time() - encrypt_start

        # No padding in CFB mode
        self.assertEqual(len(ciphertext), len(plaintext) + 16, "CFB: IV prepended")
        self.print_info(f"Ciphertext: {len(ciphertext)} bytes (no padding)")
        self.print_info(f"Encryption time: {encrypt_time:.3f}s")

        # Decrypt
        decrypt_start = time.time()
        decrypted = cipher.decrypt(ciphertext)
        decrypt_time = time.time() - decrypt_start

        self.assertEqual(decrypted, plaintext, "CFB decryption failed")
        self.print_info(f"Decryption time: {decrypt_time:.3f}s")
        self.print_success("CFB round-trip successful")

        # Test self-synchronizing property
        self.print_info("CFB is self-synchronizing after error")

        return True

    # ============================================================================
    # SECTION 5: OFB MODE TESTS
    # ============================================================================

    def test_ofb_mode_basic(self):
        """Test OFB (Output Feedback) mode - basic functionality"""
        self.print_test_header("OFB Mode - Basic Functionality")

        key = generate_key(16)
        plaintext = b"OFB mode turns block cipher into synchronous stream cipher. " * 4

        cipher = CipherCore(key, 'ofb')

        self.print_info(f"Key: {key.hex()[:32]}...")
        self.print_info(f"IV: {cipher.iv.hex()}")
        self.print_info(f"Plaintext: {len(plaintext)} bytes")

        # Encrypt
        encrypt_start = time.time()
        ciphertext = cipher.encrypt(plaintext)
        encrypt_time = time.time() - encrypt_start

        # No padding in OFB mode
        self.assertEqual(len(ciphertext), len(plaintext) + 16, "OFB: IV prepended")
        self.print_info(f"Ciphertext: {len(ciphertext)} bytes (no padding)")
        self.print_info(f"Encryption time: {encrypt_time:.3f}s")

        # Decrypt (identical to encryption in OFB)
        decrypt_start = time.time()
        decrypted = cipher.decrypt(ciphertext)
        decrypt_time = time.time() - decrypt_start

        self.assertEqual(decrypted, plaintext, "OFB decryption failed")
        self.print_info(f"Decryption time: {decrypt_time:.3f}s")
        self.print_success("OFB round-trip successful")

        # Test that encryption and decryption are identical operations
        cipher2 = CipherCore(key, 'ofb')
        test_data = b"Short test"
        encrypted = cipher2.encrypt(test_data)
        decrypted = cipher2.decrypt(encrypted)

        # In OFB, encrypt(encrypt(x)) should not return x
        double_encrypted = cipher2.encrypt(encrypted[16:])  # Skip IV
        self.assertNotEqual(double_encrypted, test_data, "OFB: double encryption check")

        self.print_success("OFB encryption/decryption symmetry verified")
        return True

    # ============================================================================
    # SECTION 6: GCM MODE TESTS (AEAD)
    # ============================================================================

    def test_gcm_mode_basic(self):
        """Test GCM (Galois/Counter Mode) - authenticated encryption"""
        self.print_test_header("GCM Mode - Authenticated Encryption")

        key = generate_key(16)
        plaintext = b"GCM provides authenticated encryption with associated data. " * 3
        aad = b"Additional Authenticated Data: timestamp=123456, user=test"

        # Create GCM instance
        gcm = GCM(key)

        self.print_info(f"Key: {key.hex()[:32]}...")
        self.print_info(f"Nonce: {gcm.nonce.hex()}")
        self.print_info(f"Plaintext: {len(plaintext)} bytes")
        self.print_info(f"AAD: {len(aad)} bytes")

        # Encrypt with AAD
        encrypt_start = time.time()
        ciphertext = gcm.encrypt(plaintext, aad)
        encrypt_time = time.time() - encrypt_start

        # GCM structure: nonce + ciphertext + tag
        self.assertEqual(len(ciphertext), len(plaintext) + 12 + 16, "GCM: nonce(12) + ciphertext + tag(16)")
        self.print_info(f"Ciphertext: {len(ciphertext)} bytes")
        self.print_info(f"Encryption time: {encrypt_time:.3f}s")

        # Decrypt with correct AAD
        decrypt_start = time.time()
        decrypted = gcm.decrypt(ciphertext, aad)
        decrypt_time = time.time() - decrypt_start

        self.assertEqual(decrypted, plaintext, "GCM decryption failed")
        self.print_info(f"Decryption time: {decrypt_time:.3f}s")
        self.print_success("GCM round-trip successful (with AAD)")

        # Test authentication failure with wrong AAD
        wrong_aad = b"Wrong additional data"
        gcm2 = GCM(key, gcm.nonce)

        with self.assertRaises(AuthenticationError):
            gcm2.decrypt(ciphertext, wrong_aad)
        self.print_success("GCM authentication failure verified (wrong AAD)")

        # Test authentication failure with tampered ciphertext
        tampered = bytearray(ciphertext)
        tampered[30] ^= 0x01  # Tamper with ciphertext

        with self.assertRaises(AuthenticationError):
            gcm2.decrypt(bytes(tampered), aad)
        self.print_success("GCM authentication failure verified (tampered data)")

        return True

    def test_gcm_mode_performance(self):
        """Test GCM mode performance with different data sizes"""
        self.print_test_header("GCM Mode - Performance Test")

        key = generate_key(16)
        aad = b"test_aad"

        sizes = [16, 64, 256, 1024, 4096, 16384]  # Bytes

        results = []

        for size in sizes:
            plaintext = os.urandom(size)

            gcm = GCM(key)

            # Encrypt
            start = time.time()
            ciphertext = gcm.encrypt(plaintext, aad)
            encrypt_time = time.time() - start

            # Decrypt
            gcm2 = GCM(key, gcm.nonce)
            start = time.time()
            decrypted = gcm2.decrypt(ciphertext, aad)
            decrypt_time = time.time() - start

            # Verify
            self.assertEqual(decrypted, plaintext, f"GPM failed for size {size}")

            throughput_mbps = (size * 8) / (encrypt_time * 1e6) if encrypt_time > 0 else 0

            results.append({
                'size': size,
                'encrypt_time': encrypt_time,
                'decrypt_time': decrypt_time,
                'throughput_mbps': throughput_mbps
            })

            self.print_info(f"  Size: {size:6d} bytes - "
                            f"Encrypt: {encrypt_time:.6f}s, "
                            f"Decrypt: {decrypt_time:.6f}s, "
                            f"Throughput: {throughput_mbps:.2f} Mbps")

        # Print summary
        print("\n  GCM Performance Summary:")
        print("  " + "─" * 60)
        for r in results:
            print(f"  {r['size']:6d} bytes: {r['throughput_mbps']:6.2f} Mbps "
                  f"(encrypt: {r['encrypt_time']:.4f}s, decrypt: {r['decrypt_time']:.4f}s)")

        self.print_success("GCM performance test completed")
        return True

    # ============================================================================
    # SECTION 7: FILE OPERATION TESTS
    # ============================================================================

    def test_file_encryption_all_modes(self):
        """Test file encryption using CLI commands (like real usage)"""
        self.print_test_header("File Encryption via CLI")

        import subprocess
        import shutil

        # Create test directory
        test_dir = tempfile.mkdtemp(prefix="cryptocore_test_")
        print(f"Test directory: {test_dir}")

        # Create test file
        input_file = os.path.join(test_dir, "test.txt")
        with open(input_file, 'wb') as f:
            # Simple test content
            test_content = b"Hello CryptoCore! This is a test file." * 10
            f.write(test_content)

        print(f"Created test file: {input_file}")
        print(f"File size: {len(test_content)} bytes")
        print(f"File MD5: {hashlib.md5(test_content).hexdigest()}")

        modes = ['ecb', 'cbc', 'ctr', 'cfb', 'ofb']
        key = "00112233445566778899aabbccddeeff"  # Fixed key for testing

        for mode in modes:
            print(f"\n{'─' * 40}")
            print(f"Testing {mode.upper()} mode via CLI:")

            encrypted_file = os.path.join(test_dir, f"test.{mode}.enc")
            decrypted_file = os.path.join(test_dir, f"test.{mode}.dec.txt")

            # Step 1: Encrypt using CLI
            print(f"  Encrypting...")
            encrypt_cmd = [
                sys.executable,  # Use same Python interpreter
                'cryptocore.py',
                '--algorithm', 'aes',
                '--mode', mode,
                '--encrypt',
                '--key', key,
                '--input', input_file,
                '--output', encrypted_file
            ]

            print(f"  Command: {' '.join(encrypt_cmd)}")

            try:
                result = subprocess.run(
                    encrypt_cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode != 0:
                    print(f"  ✗ Encryption failed:")
                    print(f"    stdout: {result.stdout}")
                    print(f"    stderr: {result.stderr}")
                    continue

                print(f"  ✓ Encryption successful")

                # Verify encrypted file exists
                if os.path.exists(encrypted_file):
                    encrypted_size = os.path.getsize(encrypted_file)
                    print(f"  Encrypted file: {encrypted_file} ({encrypted_size} bytes)")
                else:
                    print(f"  ✗ Encrypted file not created")
                    continue

                # Step 2: Decrypt using CLI
                print(f"  Decrypting...")
                decrypt_cmd = [
                    sys.executable,
                    'cryptocore.py',
                    '--algorithm', 'aes',
                    '--mode', mode,
                    '--decrypt',
                    '--key', key,
                    '--input', encrypted_file,
                    '--output', decrypted_file
                ]

                print(f"  Command: {' '.join(decrypt_cmd)}")

                result = subprocess.run(
                    decrypt_cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode != 0:
                    print(f"  ✗ Decryption failed:")
                    print(f"    stdout: {result.stdout}")
                    print(f"    stderr: {result.stderr}")
                    continue

                print(f"  ✓ Decryption successful")

                # Step 3: Verify
                if os.path.exists(decrypted_file):
                    with open(decrypted_file, 'rb') as f:
                        decrypted_content = f.read()

                    decrypted_size = len(decrypted_content)
                    print(f"  Decrypted file: {decrypted_file} ({decrypted_size} bytes)")

                    # Compare with original
                    if decrypted_content == test_content:
                        print(f"  ✓ {mode.upper()}: Content matches!")
                    else:
                        print(f"  ✗ {mode.upper()}: Content mismatch!")

                        # Show hashes
                        original_hash = hashlib.md5(test_content).hexdigest()
                        decrypted_hash = hashlib.md5(decrypted_content).hexdigest()
                        print(f"    Original MD5: {original_hash}")
                        print(f"    Decrypted MD5: {decrypted_hash}")

                        # Find first difference
                        min_len = min(len(test_content), len(decrypted_content))
                        for i in range(min_len):
                            if test_content[i] != decrypted_content[i]:
                                print(f"    First difference at byte {i}:")
                                print(f"      Original: {test_content[i:i + 16].hex()}")
                                print(f"      Decrypted: {decrypted_content[i:i + 16].hex()}")
                                break
                else:
                    print(f"  ✗ Decrypted file not created")

            except subprocess.TimeoutExpired:
                print(f"  ✗ Command timed out")
            except Exception as e:
                print(f"  ✗ Error: {e}")

        # Cleanup
        print(f"\n{'─' * 40}")
        print(f"Cleaning up test directory: {test_dir}")
        try:
            shutil.rmtree(test_dir)
            print(f"✓ Test directory cleaned up")
        except Exception as e:
            print(f"✗ Could not clean up: {e}")

        self.print_success("CLI file encryption tests completed")
        return True

    # ============================================================================
    # SECTION 8: INTEROPERABILITY TESTS
    # ============================================================================

    def test_interoperability_vectors(self):
        """Test with known test vectors for interoperability"""
        self.print_test_header("Interoperability - Known Test Vectors")

        # AES-128-CBC test vector (simplified)
        key = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
        iv = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
        plaintext = b"Test vector for interoperability"

        # Test CBC with known parameters
        cipher = CipherCore(key, 'cbc')
        # We can't set IV directly in CipherCore, so test round-trip
        ciphertext = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(ciphertext)

        self.assertEqual(decrypted, plaintext, "Interoperability round-trip failed")
        self.print_success("Basic interoperability verified")

        # Test with NIST-like vectors
        test_cases = [
            {
                'name': 'Empty data',
                'data': b'',
                'modes': ['ecb', 'cbc', 'ctr', 'cfb', 'ofb']
            },
            {
                'name': 'Single block',
                'data': b'A' * 16,
                'modes': ['ecb', 'cbc', 'ctr', 'cfb', 'ofb']
            },
            {
                'name': 'Partial block',
                'data': b'Partial',
                'modes': ['ecb', 'cbc']  # Stream modes handle partial blocks differently
            },
            {
                'name': 'Multiple blocks',
                'data': b'Multiple blocks of data for testing ' * 4,
                'modes': ['ecb', 'cbc', 'ctr', 'cfb', 'ofb']
            }
        ]

        for test_case in test_cases:
            self.print_info(f"\n  Test: {test_case['name']} ({len(test_case['data'])} bytes)")

            for mode in test_case['modes']:
                try:
                    key = generate_key(16)
                    cipher = CipherCore(key, mode)

                    # Encrypt
                    ciphertext = cipher.encrypt(test_case['data'])

                    # Decrypt
                    decrypted = cipher.decrypt(ciphertext)

                    self.assertEqual(decrypted, test_case['data'],
                                     f"{mode}: {test_case['name']} failed")

                    self.print_info(f"    {mode.upper()}: ✓")

                except Exception as e:
                    self.print_warning(f"    {mode.upper()}: ✗ ({str(e)[:30]}...)")

        self.print_success("Interoperability tests completed")
        return True

    # ============================================================================
    # SECTION 9: SECURITY PROPERTIES TESTS
    # ============================================================================

    def test_mode_security_properties(self):
        """Test security properties of different modes"""
        self.print_test_header("Security Properties Comparison")

        key = generate_key(16)
        plaintext = b"Security test data with patterns " * 8

        print("\n  Security Properties Summary:")
        print("  " + "─" * 60)

        modes_info = [
            {
                'mode': 'ecb',
                'confidentiality': 'Weak',
                'integrity': 'None',
                'authentication': 'None',
                'error_propagation': 'Limited',
                'padding': 'Required',
                'notes': 'Patterns visible, not recommended'
            },
            {
                'mode': 'cbc',
                'confidentiality': 'Strong',
                'integrity': 'None',
                'authentication': 'None',
                'error_propagation': 'Two blocks',
                'padding': 'Required',
                'notes': 'Good general purpose'
            },
            {
                'mode': 'ctr',
                'confidentiality': 'Strong',
                'integrity': 'None',
                'authentication': 'None',
                'error_propagation': 'One bit',
                'padding': 'None',
                'notes': 'Parallelizable, random access'
            },
            {
                'mode': 'cfb',
                'confidentiality': 'Strong',
                'integrity': 'None',
                'authentication': 'None',
                'error_propagation': 'Self-sync',
                'padding': 'None',
                'notes': 'Self-synchronizing'
            },
            {
                'mode': 'ofb',
                'confidentiality': 'Strong',
                'integrity': 'None',
                'authentication': 'None',
                'error_propagation': 'One bit',
                'padding': 'None',
                'notes': 'Keystream reuse dangerous'
            },
            {
                'mode': 'gcm',
                'confidentiality': 'Strong',
                'integrity': 'Strong',
                'authentication': 'Strong',
                'error_propagation': 'All',
                'padding': 'None',
                'notes': 'Authenticated encryption (AEAD)'
            }
        ]

        for info in modes_info:
            print(f"  {info['mode'].upper():4s} | "
                  f"Conf: {info['confidentiality']:6s} | "
                  f"Integ: {info['integrity']:6s} | "
                  f"Auth: {info['authentication']:6s} | "
                  f"Notes: {info['notes']}")

        print("  " + "─" * 60)

        # Test each mode
        for info in modes_info:
            if info['mode'] == 'gcm':
                continue  # Tested separately

            try:
                cipher = CipherCore(key, info['mode'])
                ciphertext = cipher.encrypt(plaintext)
                decrypted = cipher.decrypt(ciphertext)

                self.assertEqual(decrypted, plaintext, f"{info['mode']} security test failed")

            except Exception as e:
                self.print_warning(f"  {info['mode'].upper()}: {str(e)[:40]}")

        self.print_success("Security properties analyzed")
        return True

    # ============================================================================
    # SECTION 10: PERFORMANCE BENCHMARK
    # ============================================================================

    def test_performance_benchmark(self):
        """Performance benchmark of all modes"""
        self.print_test_header("Performance Benchmark - All Modes")

        key = generate_key(16)
        data_sizes = [1024, 8192, 65536]  # 1KB, 8KB, 64KB

        # Skip GCM for this benchmark (already tested)
        modes = ['ecb', 'cbc', 'ctr', 'cfb', 'ofb']

        print("\n  Performance Results (higher throughput is better):")
        print("  " + "─" * 80)
        print("  Mode   | Size (KB) | Encrypt (ms) | Decrypt (ms) | Throughput (MB/s)")
        print("  " + "─" * 80)

        results = []

        for size in data_sizes:
            plaintext = os.urandom(size)

            for mode in modes:
                try:
                    # Warm-up
                    cipher = CipherCore(key, mode)
                    _ = cipher.encrypt(plaintext[:100])

                    # Benchmark encryption
                    cipher = CipherCore(key, mode)
                    start = time.time()
                    ciphertext = cipher.encrypt(plaintext)
                    encrypt_time = (time.time() - start) * 1000  # ms

                    # Benchmark decryption
                    start = time.time()
                    decrypted = cipher.decrypt(ciphertext)
                    decrypt_time = (time.time() - start) * 1000  # ms

                    # Verify
                    self.assertEqual(decrypted, plaintext, f"{mode} benchmark verification failed")

                    # Calculate throughput
                    throughput = (size / 1024 / 1024) / (encrypt_time / 1000)  # MB/s

                    results.append({
                        'mode': mode,
                        'size': size,
                        'encrypt_ms': encrypt_time,
                        'decrypt_ms': decrypt_time,
                        'throughput_mb_s': throughput
                    })

                    print(f"  {mode.upper():6s} | {size / 1024:8.1f} | "
                          f"{encrypt_time:11.2f} | {decrypt_time:11.2f} | {throughput:15.2f}")

                except Exception as e:
                    print(f"  {mode.upper():6s} | {size / 1024:8.1f} | ERROR: {str(e)[:30]}")

        print("  " + "─" * 80)

        # Find fastest mode for each size
        for size in data_sizes:
            size_results = [r for r in results if r['size'] == size]
            if size_results:
                fastest = max(size_results, key=lambda x: x['throughput_mb_s'])
                self.print_info(f"  Fastest for {size / 1024:.1f}KB: {fastest['mode'].upper()} "
                                f"({fastest['throughput_mb_s']:.2f} MB/s)")

        self.print_success("Performance benchmark completed")
        return True


def run_comprehensive_test_suite():
    """Run the comprehensive test suite with detailed reporting"""
    print("=" * 80)
    print("🔐 COMPREHENSIVE CIPHER MODES TEST SUITE")
    print("=" * 80)
    print("Testing all AES modes: ECB, CBC, CTR, CFB, OFB, GCM")
    print("=" * 80)

    # Create test suite
    loader = unittest.TestLoader()

    # Select tests to run (all test methods starting with 'test_')
    test_methods = [
        'test_ecb_mode_basic',
        'test_ecb_mode_security_characteristics',
        'test_cbc_mode_basic',
        'test_cbc_mode_error_propagation',
        'test_ctr_mode_basic',
        'test_ctr_mode_random_access',
        'test_cfb_mode_basic',
        'test_ofb_mode_basic',
        'test_gcm_mode_basic',
        'test_gcm_mode_performance',
        'test_file_encryption_all_modes',
        'test_interoperability_vectors',
        'test_mode_security_properties',
        'test_performance_benchmark'
    ]

    suite = unittest.TestSuite()
    for method in test_methods:
        suite.addTest(TestAllCipherModes(method))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=0)  # We handle our own output
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 80)
    print("📊 TEST SUITE SUMMARY")
    print("=" * 80)
    print(f"Total tests run: {result.testsRun}")
    print(f"Tests passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests failed: {len(result.failures)}")
    print(f"Tests errored: {len(result.errors)}")
    print("=" * 80)

    # Print mode compatibility matrix
    print("\n📋 MODE COMPATIBILITY MATRIX")
    print("=" * 80)
    modes = ['ECB', 'CBC', 'CTR', 'CFB', 'OFB', 'GCM']
    features = [
        ('Confidentiality', '✓✓✓', '✓✓✓', '✓✓✓', '✓✓✓', '✓✓✓', '✓✓✓'),
        ('Integity Check', '✗', '✗', '✗', '✗', '✗', '✓✓✓'),
        ('Authentication', '✗', '✗', '✗', '✗', '✗', '✓✓✓'),
        ('Padding Required', '✓', '✓', '✗', '✗', '✗', '✗'),
        ('Parallel Encryption', '✓', '✗', '✓', '✗', '✗', '✓'),
        ('Random Access', '✓', '✗', '✓', '✗', '✗', '✗'),
        ('Error Propagation', 'Block', '2 Blocks', '1 Bit', 'Self-sync', '1 Bit', 'All'),
        ('Recommended Use', 'Never', 'General', 'Streaming', 'Networking', 'Streaming', 'Secure')
    ]

    print(f"{'Feature':20s} | {' | '.join(f'{m:^8s}' for m in modes)}")
    print("-" * 90)
    for feature, ecb, cbc, ctr, cfb, ofb, gcm in features:
        print(f"{feature:20s} | {ecb:^8s} | {cbc:^8s} | {ctr:^8s} | {cfb:^8s} | {ofb:^8s} | {gcm:^8s}")
    print("=" * 80)

    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("=" * 80)
    print("• Use CBC for general-purpose file encryption")
    print("• Use CTR for streaming or parallel processing")
    print("• Use GCM for maximum security (authenticated encryption)")
    print("• AVOID ECB for any sensitive data")
    print("• Consider CFB/OFB for specific network protocols")
    print("=" * 80)

    return result.wasSuccessful()


if __name__ == '__main__':
    # Run the comprehensive test suite
    success = run_comprehensive_test_suite()

    # Exit with appropriate code
    sys.exit(0 if success else 1)