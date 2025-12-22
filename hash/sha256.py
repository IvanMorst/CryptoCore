"""
SHA-256 implementation from scratch according to NIST FIPS 180-4
"""

import struct
import binascii


class SHA256:
    """
    SHA-256 hash function implementation
    """

    def __init__(self, data: bytes = None):
        # Initialize hash values (first 32 bits of fractional parts of square roots of first 8 primes)
        self.h = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]

        # Initialize round constants (first 32 bits of fractional parts of cube roots of first 64 primes)
        self.k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        self.message_length = 0
        self.buffer = bytearray()

        if data:
            self.update(data)

    def _rotr(self, x, n):
        """Right rotate"""
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    def _shr(self, x, n):
        """Right shift"""
        return x >> n

    def _ch(self, x, y, z):
        """Choice function"""
        return (x & y) ^ (~x & z)

    def _maj(self, x, y, z):
        """Majority function"""
        return (x & y) ^ (x & z) ^ (y & z)

    def _sigma0(self, x):
        """σ0 function"""
        return self._rotr(x, 2) ^ self._rotr(x, 13) ^ self._rotr(x, 22)

    def _sigma1(self, x):
        """σ1 function"""
        return self._rotr(x, 6) ^ self._rotr(x, 11) ^ self._rotr(x, 25)

    def _gamma0(self, x):
        """γ0 function"""
        return self._rotr(x, 7) ^ self._rotr(x, 18) ^ self._shr(x, 3)

    def _gamma1(self, x):
        """γ1 function"""
        return self._rotr(x, 17) ^ self._rotr(x, 19) ^ self._shr(x, 10)

    def _padding(self, message_length: int) -> bytes:
        """
        SHA-256 padding according to FIPS 180-4

        Args:
            message_length: Total message length in bits

        Returns:
            bytes: Padding bytes
        """
        # Start with bit '1'
        padding = b'\x80'

        # Calculate how many zeros we need
        # Total message length after padding must be 448 mod 512 bits (56 mod 64 bytes)
        message_len_bytes = message_length // 8  # Convert bits to bytes
        zero_padding_len = (56 - (message_len_bytes + 1) % 64) % 64

        # Add zero bytes
        padding += b'\x00' * zero_padding_len

        # Add original message length as 64-bit big-endian integer
        padding += struct.pack('>Q', message_length)

        return padding

    def _process_block(self, block, current_hash):
        """
        Process one 512-bit block

        Args:
            block: 64-byte block to process
            current_hash: Current hash values to update

        Returns:
            list: Updated hash values
        """
        if len(block) != 64:
            raise ValueError("Block must be exactly 64 bytes")

        # Prepare message schedule
        w = [0] * 64

        # Copy block into first 16 words of message schedule
        for i in range(16):
            w[i] = struct.unpack('>I', block[i * 4:(i + 1) * 4])[0]

        # Extend the first 16 words into the remaining 48 words
        for i in range(16, 64):
            s0 = self._gamma0(w[i - 15])
            s1 = self._gamma1(w[i - 2])
            w[i] = (s0 + w[i - 7] + s1 + w[i - 16]) & 0xFFFFFFFF

        # Initialize working variables with current hash values
        a, b, c, d, e, f, g, h = current_hash

        # Main compression loop
        for i in range(64):
            t1 = (h + self._sigma1(e) + self._ch(e, f, g) + self.k[i] + w[i]) & 0xFFFFFFFF
            t2 = (self._sigma0(a) + self._maj(a, b, c)) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF

        # Add compressed chunk to current hash value
        return [
            (current_hash[0] + a) & 0xFFFFFFFF,
            (current_hash[1] + b) & 0xFFFFFFFF,
            (current_hash[2] + c) & 0xFFFFFFFF,
            (current_hash[3] + d) & 0xFFFFFFFF,
            (current_hash[4] + e) & 0xFFFFFFFF,
            (current_hash[5] + f) & 0xFFFFFFFF,
            (current_hash[6] + g) & 0xFFFFFFFF,
            (current_hash[7] + h) & 0xFFFFFFFF
        ]

    def update(self, data):
        """
        Update hash with new data

        Args:
            data: Data to hash (must be bytes)
        """
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes")

        self.buffer.extend(data)
        self.message_length += len(data) * 8  # Convert bytes to bits

        # Process complete blocks
        while len(self.buffer) >= 64:
            block = bytes(self.buffer[:64])
            self.buffer = self.buffer[64:]
            self.h = self._process_block(block, self.h)

    def digest(self):
        """
        Return final hash digest without modifying internal state

        Returns:
            bytes: Final hash value
        """
        # Create copies to avoid modifying the original state
        buffer_copy = self.buffer.copy()
        hash_copy = self.h[:]
        msg_len_copy = self.message_length

        # Apply padding to the remaining data
        padding = self._padding(msg_len_copy)
        buffer_copy.extend(padding)

        # Process all padded blocks
        for i in range(0, len(buffer_copy), 64):
            block = bytes(buffer_copy[i:i + 64])
            hash_copy = self._process_block(block, hash_copy)

        # Produce final hash value
        digest = b''
        for h_val in hash_copy:
            digest += struct.pack('>I', h_val)

        return digest

    def hexdigest(self):
        """
        Return final hash as hexadecimal string

        Returns:
            str: Hexadecimal representation of hash
        """
        return self.digest().hex()


def sha256(data: bytes) -> str:
    """
    Convenience function for one-shot SHA-256 hashing

    Args:
        data: Data to hash

    Returns:
        str: Hexadecimal hash string
    """
    hasher = SHA256()
    hasher.update(data)
    return hasher.hexdigest()


def sha256_file(filename: str, chunk_size: int = 8192) -> str:
    """
    Compute SHA-256 hash of a file

    Args:
        filename: Path to file
        chunk_size: Size of chunks to read

    Returns:
        str: Hexadecimal hash string
    """
    hasher = SHA256()

    try:
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except IOError as e:
        raise IOError(f"Error reading file {filename}: {e}")

    return hasher.hexdigest()


# Test vectors for verification
if __name__ == "__main__":
    # Test empty string
    assert sha256(b"") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    # Test "abc"
    assert sha256(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

    # Test two-block message
    long_msg = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
    assert sha256(long_msg) == "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"

    print("✅ All SHA-256 test vectors passed!")