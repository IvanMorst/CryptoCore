### **docs/DEVELOPMENT.md**
```markdown
# CryptoCore Development Guide

## Project Overview

CryptoCore is a comprehensive cryptographic toolkit implemented in pure Python. The project follows a modular architecture with clear separation of concerns.

## Architecture

### Module Structure
crypto/ # Core cryptographic functions
├── cipher_core.py # AES encryption/decryption core
├── aead/ # Authenticated Encryption
│ ├── gcm.py # GCM implementation
│ └── encrypt_then_mac.py
├── modes/ # Block cipher modes
│ ├── base_mode.py # Abstract base class
│ ├── cbc_mode.py
│ ├── ctr_mode.py
│ ├── cfb_mode.py
│ ├── ofb_mode.py
│ └── gcm_mode.py # GCM adapter
└── kdf/ # Key Derivation Functions
├── pbkdf2.py
└── key_hierarchy.py

hash/ # Hash functions
├── sha256.py # SHA-256 implementation
└── sha3_256.py # SHA3-256 implementation

mac/ # Message Authentication
└── hmac.py # HMAC-SHA256 implementation

csprng.py # Cryptographically Secure PRNG

text

### Design Principles

1. **Security First**: All implementations follow established standards
2. **Modularity**: Each component is independent and testable
3. **Education**: Code is readable and well-documented
4. **Practicality**: Includes real-world use cases and CLI

## Development Environment

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/CryptoCore.git
cd CryptoCore

# Create virtual environment
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
Development Tools
Code Formatting
bash
# Format code with Black
black .

# Check formatting without changes
black --check .
Linting
bash
# Run Flake8
flake8 .

# Run specific checks
flake8 --select=E9,F63,F7,F82  # Syntax and undefined names
flake8 --select=F401           # Unused imports
Type Checking
bash
# Run MyPy
mypy .
Testing
bash
# Run all tests
python tests/run_tests.py

# Run specific test modules
pytest tests/unit/test_aes.py -v

# Run with coverage
pytest --cov=. --cov-report=html
Coding Standards
Python Version
Target Python 3.8+

Use type hints for all function signatures

Use f-strings for string formatting

Use pathlib for file operations

Import Organization
python
# Standard library imports
import os
import sys
from typing import List, Optional

# Third-party imports
from Crypto.Cipher import AES

# Local imports
from crypto.cipher_core import CipherCore
from hash.sha256 import SHA256
Documentation Standards
Google Style Docstrings
python
def encrypt_data(key: bytes, plaintext: bytes, mode: str = 'cbc') -> bytes:
    """
    Encrypt data using specified key and mode.

    Args:
        key: Encryption key (16, 24, or 32 bytes)
        plaintext: Data to encrypt
        mode: Encryption mode ('ecb', 'cbc', 'ctr', 'cfb', 'ofb', 'gcm')

    Returns:
        Encrypted ciphertext

    Raises:
        ValueError: If key length is invalid
        TypeError: If inputs are not bytes

    Example:
        >>> key = b'0' * 16
        >>> data = b'secret'
        >>> encrypt_data(key, data, 'cbc')
        b'...encrypted bytes...'
    """
    # Implementation
Module Documentation
python
"""
AES Core Implementation

This module provides the core AES encryption/decryption functions.
Implementation follows NIST FIPS 197 specification.

Classes:
    CipherCore: Main AES cipher class supporting multiple modes

Functions:
    encrypt_block: Encrypt single 16-byte block
    decrypt_block: Decrypt single 16-byte block
    _key_expansion: Expand key for AES rounds

Constants:
    BLOCK_SIZE: AES block size (16 bytes)

References:
    NIST FIPS 197: Advanced Encryption Standard (AES)
"""
Error Handling
Use Specific Exceptions
python
def validate_key(key: bytes) -> None:
    """Validate AES key."""
    if not isinstance(key, bytes):
        raise TypeError(f"Key must be bytes, got {type(key)}")
    
    if len(key) not in (16, 24, 32):
        raise ValueError(
            f"Key must be 16, 24, or 32 bytes, got {len(key)} bytes"
        )
Custom Exceptions
python
class AuthenticationError(Exception):
    """Exception for authentication failures."""
    
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(message)
        self.original_exception = original_exception
Testing Strategy
Test Categories
Unit Tests
Test individual functions in isolation

Mock dependencies when necessary

Cover edge cases and error conditions

Integration Tests
Test component interactions

Test CLI commands end-to-end

Test file operations

Known-Answer Tests
Use official test vectors

Verify standard compliance

Ensure interoperability

Test Structure
python
"""
Tests for AES implementation.

Test cases from NIST SP 800-38A and FIPS 197.
"""

import unittest
from crypto.cipher_core import CipherCore


class TestAES(unittest.TestCase):
    """AES encryption/decryption tests."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.key = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
        self.cipher = CipherCore(self.key, 'ecb')
    
    def test_encrypt_decrypt(self):
        """Test encryption followed by decryption."""
        plaintext = b'Test message 123'
        ciphertext = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(ciphertext)
        self.assertEqual(decrypted, plaintext)
    
    def test_nist_vector_1(self):
        """Test NIST known-answer vector 1."""
        plaintext = bytes.fromhex('00112233445566778899aabbccddeeff')
        expected = bytes.fromhex('69c4e0d86a7b0430d8cdb78070b4c55a')
        ciphertext = self.cipher.encrypt(plaintext)
        self.assertEqual(ciphertext, expected)
    
    def test_invalid_key_length(self):
        """Test invalid key length raises error."""
        with self.assertRaises(ValueError):
            CipherCore(b'short', 'ecb')
    
    # ... more tests
Test Coverage Goals
90%+ line coverage for core modules

100% coverage for security-critical functions

Test all error conditions

Test all public API methods

Security Considerations
Code Review Checklist
Input Validation
All inputs validated before use

Type checking for all parameters

Length checking for cryptographic parameters

Range checking for numerical parameters

Memory Safety
Sensitive data cleared after use

No buffer overflows possible

Secure memory allocation patterns

Cryptographic Security
Algorithms implemented per standards

Test vectors from official sources

No weak defaults or configurations

Proper key management

Error Handling
No sensitive information in error messages

Errors don't reveal implementation details

Fail-secure behavior

Security Testing
Static Analysis
bash
# Run bandit for security issues
bandit -r .

# Run safety for dependency vulnerabilities
safety check
Dynamic Analysis
Fuzz testing for input validation

Memory profiling for leaks

Timing analysis for side channels

Performance Considerations
Optimization Guidelines
Use Built-in Functions
python
# Good: Use bytes methods
result = bytes(a ^ b for a, b in zip(x, y))

# Bad: Manual loops
result = bytearray()
for i in range(len(x)):
    result.append(x[i] ^ y[i])
Process Large Files in Chunks
python
def process_large_file(filename: str, chunk_size: int = 8192):
    """Process file in chunks to manage memory."""
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            # Process chunk
            yield process_chunk(chunk)
Cache Computations
python
class OptimizedCipher:
    """Cipher with computed values caching."""
    
    def __init__(self, key: bytes):
        self.key = key
        self._round_keys = self._compute_round_keys(key)  # Cache
    
    def _compute_round_keys(self, key: bytes):
        """Compute and cache round keys."""
        # Expensive computation once
        return expand_key(key)
Profiling
bash
# Profile execution
python -m cProfile -o profile.stats cryptocore.py encrypt --input largefile.bin

# Analyze profile
python -m pstats profile.stats
Release Process
Version Bumping
Update version in pyproject.toml

Update CHANGELOG.md

Create release tag

Testing Before Release
bash
# Run full test suite
python tests/run_tests.py

# Run security checks
bandit -r .
safety check

# Run type checking
mypy .

# Run linting
flake8 .
black --check .
Building Distribution
bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI (if applicable)
twine upload dist/*
Contributing
Workflow
Create issue describing the change

Fork repository and create feature branch

Make changes with tests

Run all checks and tests

Submit pull request

Pull Request Checklist
Code follows style guidelines

Tests added/updated

Documentation updated

CHANGELOG.md updated if needed

Security review completed

Code Review Focus Areas
Security implications

Test coverage

Documentation quality

Performance impact

Backward compatibility

Troubleshooting Development Issues
Common Problems
Import Errors
bash
# Ensure you're in the project root
pwd  # Should show CryptoCore directory

# Check Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .
Test Failures
bash
# Run specific failing test
pytest tests/unit/test_aes.py::TestAES::test_nist_vector_1 -v

# Run with debug output
pytest -v --tb=short

# Check test data
python -c "from tests.vectors.aes_vectors import TEST_VECTORS; print(TEST_VECTORS[0])"
Performance Issues
bash
# Profile specific function
python -m cProfile -s time my_script.py

# Memory profiling
python -m memory_profiler my_script.py
Resources
Cryptographic Standards
NIST FIPS 197: AES

NIST SP 800-38A: Block Cipher Modes

NIST SP 800-38D: GCM Mode

NIST FIPS 180-4: SHA-2

NIST FIPS 202: SHA-3

RFC 2104: HMAC

RFC 2898: PBKDF2

RFC 4231: HMAC Test Vectors

RFC 6070: PBKDF2 Test Vectors

Python Resources
Python Cryptographic Authority

PyCryptodome Documentation

Python Security

Tools
Black Code Formatter

Flake8

MyPy

Bandit

Safety

Getting Help
Check existing documentation

Search existing issues

Review test cases for usage examples

Contact maintainers through GitHub issues

Remember: Security is a process, not a product. Regular reviews and updates are essential.