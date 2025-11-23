"""
SHA3-256 implementation from scratch according to NIST FIPS 202
"""

import struct

class SHA3_256:
    """
    SHA3-256 hash function implementation using Keccak sponge construction
    """

    # SHA3-256 parameters
    RATE = 1088  # bits (136 bytes)
    CAPACITY = 512  # bits (64 bytes)
    OUTPUT_LENGTH = 256  # bits (32 bytes)

    # Round constants
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
        0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]

    # Rotation offsets
    ROTATION_OFFSETS = [
        [0, 36, 3, 41, 18],
        [1, 44, 10, 45, 2],
        [62, 6, 43, 15, 61],
        [28, 55, 25, 21, 56],
        [27, 20, 39, 8, 14]
    ]

    def __init__(self):
        # Initialize state as 5x5 matrix of 64-bit integers
        self.state = [[0] * 5 for _ in range(5)]
        self.buffer = bytearray()
        self.total_length = 0

    def _rot64(self, x, n):
        """64-bit rotation"""
        n = n % 64
        return ((x >> (64 - n)) | (x << n)) & ((1 << 64) - 1)

    def _keccak_f(self):
        """Keccak-f permutation"""
        for round_num in range(24):
            # θ step
            c = [0] * 5
            d = [0] * 5

            for i in range(5):
                c[i] = self.state[i][0] ^ self.state[i][1] ^ self.state[i][2] ^ self.state[i][3] ^ self.state[i][4]

            for i in range(5):
                d[i] = c[(i - 1) % 5] ^ self._rot64(c[(i + 1) % 5], 1)

            for i in range(5):
                for j in range(5):
                    self.state[i][j] ^= d[i]

            # ρ and π steps
            temp_state = [[0] * 5 for _ in range(5)]
            for i in range(5):
                for j in range(5):
                    temp_state[j][(2 * i + 3 * j) % 5] = self._rot64(self.state[i][j], self.ROTATION_OFFSETS[i][j])

            # χ step
            for i in range(5):
                for j in range(5):
                    self.state[i][j] = temp_state[i][j] ^ ((~temp_state[(i + 1) % 5][j]) & temp_state[(i + 2) % 5][j])

            # ι step
            self.state[0][0] ^= self.RC[round_num]

    def _absorb(self):
        """Absorb data into sponge"""
        block_size = self.RATE // 8  # 136 bytes

        for i in range(0, len(self.buffer), block_size):
            block = self.buffer[i:i + block_size]

            # Pad block to full size if necessary
            if len(block) < block_size:
                block += b'\x00' * (block_size - len(block))

            # XOR block into state
            for j in range(len(block) // 8):
                lane_value = struct.unpack('<Q', block[j*8:(j+1)*8])[0]
                x = j % 5
                y = j // 5
                self.state[x][y] ^= lane_value

            # Apply Keccak-f permutation
            self._keccak_f()

        # Clear buffer after absorption
        self.buffer = bytearray()

    def update(self, data):
        """
        Update hash with new data
        """
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes")

        self.buffer.extend(data)
        self.total_length += len(data)

        # Absorb full blocks
        block_size = self.RATE // 8
        while len(self.buffer) >= block_size:
            self._absorb()

    def digest(self):
        """
        Return final hash digest
        """
        # Apply padding
        block_size = self.RATE // 8

        # SHA3 padding: append 0x06, then pad with zeros, then set last bit
        self.buffer.append(0x06)

        # Pad with zeros until we have block_size - 1 bytes
        while (len(self.buffer) % block_size) != (block_size - 1):
            self.buffer.append(0x00)

        # Set last bit
        self.buffer.append(0x80)

        # Absorb the padded data
        self._absorb()

        # Squeeze output
        output = bytearray()
        output_length = self.OUTPUT_LENGTH // 8  # 32 bytes

        while len(output) < output_length:
            # Extract lanes from state
            for j in range(block_size // 8):
                if len(output) >= output_length:
                    break

                x = j % 5
                y = j // 5
                lane_bytes = struct.pack('<Q', self.state[x][y])
                output.extend(lane_bytes)

            if len(output) < output_length:
                self._keccak_f()

        return bytes(output[:output_length])

    def hexdigest(self):
        """
        Return final hash as hexadecimal string
        """
        return self.digest().hex()


def sha3_256(data):
    """
    Convenience function for one-shot SHA3-256 hashing
    """
    hasher = SHA3_256()
    hasher.update(data)
    return hasher.hexdigest()


def sha3_256_file(filename, chunk_size=8192):
    """
    Compute SHA3-256 hash of a file
    """
    hasher = SHA3_256()

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