"""
HMAC (Hash-based Message Authentication Code) implementation
RFC 2104 compliant implementation using SHA-256
"""

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
    OUTPUT_SIZE = 32  # SHA-256 output is 32 bytes

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
        Process key according to RFC 2104

        Args:
            key: Original key bytes

        Returns:
            bytes: Processed key (always BLOCK_SIZE bytes)
        """
        # Step 1: Keys longer than block size are hashed
        if len(key) > self.BLOCK_SIZE:
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
        return bytes(x ^ y for x, y in zip(a, b))

    def compute(self, message: bytes) -> bytes:
        """
        Compute HMAC for a message

        Formula: HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))
        where H is SHA-256

        Args:
            message: Message to authenticate

        Returns:
            bytes: HMAC value (32 bytes for SHA-256)
        """
        # Create inner and outer pads
        ipad = b'\x36' * self.BLOCK_SIZE  # inner pad (0x36 repeated)
        opad = b'\x5c' * self.BLOCK_SIZE  # outer pad (0x5c repeated)

        # XOR key with pads
        k_ipad = self._xor_bytes(self.key, ipad)
        k_opad = self._xor_bytes(self.key, opad)

        # Inner hash: H((K ⊕ ipad) || message)
        inner_hasher = self.hash_func()
        inner_hasher.update(k_ipad)
        inner_hasher.update(message)
        inner_hash = inner_hasher.digest()

        # Outer hash: H((K ⊕ opad) || inner_hash)
        outer_hasher = self.hash_func()
        outer_hasher.update(k_opad)
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
        k_ipad = self._xor_bytes(self.key, ipad)
        k_opad = self._xor_bytes(self.key, opad)

        # Inner hash: H((K ⊕ ipad) || message)
        inner_hasher = self.hash_func()
        inner_hasher.update(k_ipad)

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

        # Outer hash: H((K ⊕ opad) || inner_hash)
        outer_hasher = self.hash_func()
        outer_hasher.update(k_opad)
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


# RFC 4231 Test vectors for verification
if __name__ == "__main__":
    # Test Case 1
    key1 = bytes([0x0b] * 20)
    data1 = b"Hi There"
    expected1 = bytes.fromhex("b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")
    result1 = hmac_sha256(key1, data1)
    assert result1 == expected1, f"Test 1 failed: {result1.hex()} != {expected1.hex()}"
    print("✅ RFC 4231 Test Case 1 passed")

    # Test Case 2
    key2 = b"Jefe"
    data2 = b"what do ya want for nothing?"
    expected2 = bytes.fromhex("5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843")
    result2 = hmac_sha256(key2, data2)
    assert result2 == expected2, f"Test 2 failed: {result2.hex()} != {expected2.hex()}"
    print("✅ RFC 4231 Test Case 2 passed")

    # Test with empty key and data
    key3 = b""
    data3 = b""
    expected3 = bytes.fromhex("b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad")
    result3 = hmac_sha256(key3, data3)
    assert result3 == expected3, f"Test 3 failed: {result3.hex()} != {expected3.hex()}"
    print("✅ Empty key/data test passed")

    print("\n✅ All RFC 4231 test vectors passed successfully!")