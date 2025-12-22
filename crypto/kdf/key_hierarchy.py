"""
Key Hierarchy Function - Deriving multiple keys from a master key
Deterministic HMAC-based key derivation following RFC 5869 HKDF pattern
"""

import struct
from typing import Union, List, Dict

# Импорт нашей реализации HMAC
from mac.hmac import HMAC


class KeyHierarchy:
    """
    Key hierarchy for deriving multiple keys from a master key
    Uses HMAC-based key derivation similar to HKDF
    """

    @staticmethod
    def derive_key(master_key: bytes,
                   context: Union[str, bytes],
                   length: int = 32) -> bytes:
        """
        Derive a key from a master key using HMAC-based method

        Args:
            master_key: Master key (bytes)
            context: Context string (e.g., "encryption", "authentication")
            length: Desired key length in bytes (default: 32)

        Returns:
            bytes: Derived key
        """
        if not master_key:
            raise ValueError("Master key cannot be empty")

        if isinstance(context, str):
            context = context.encode('utf-8')

        if length <= 0:
            raise ValueError("Key length must be positive")

        # HKDF Extract: PRK = HMAC(salt, IKM) where salt is empty
        hmac_extract = HMAC(b'', 'sha256')
        prk = hmac_extract.compute(master_key)  # Extract with master key as message

        # HKDF Expand: Generate enough output
        derived = b''
        counter = 1
        output_length = 0

        while output_length < length:
            # T(i) = HMAC(PRK, T(i-1) || info || counter)
            # where T(0) is empty
            if counter == 1:
                # First iteration: HMAC(PRK, info || 0x01)
                block_data = context + struct.pack('B', counter)
            else:
                # Subsequent iterations: HMAC(PRK, T(i-1) || info || counter)
                prev_block = derived[-32:]  # Last 32 bytes (SHA-256 output)
                block_data = prev_block + context + struct.pack('B', counter)

            hmac_expand = HMAC(prk, 'sha256')
            block = hmac_expand.compute(block_data)
            derived += block
            output_length += len(block)
            counter += 1

        # Return exactly requested length
        return derived[:length]

    @staticmethod
    def derive_keys(master_key: bytes,
                    contexts: List[str],
                    length: int = 32) -> Dict[str, bytes]:
        """
        Derive multiple keys for different contexts

        Args:
            master_key: Master key (bytes)
            contexts: List of context strings
            length: Key length for all contexts

        Returns:
            dict: {context: derived_key}
        """
        keys = {}
        for context in contexts:
            keys[context] = KeyHierarchy.derive_key(master_key, context, length)

        return keys


# Convenience functions
def derive_key(master_key: bytes,
               context: Union[str, bytes],
               length: int = 32) -> bytes:
    """Convenience function for key derivation"""
    return KeyHierarchy.derive_key(master_key, context, length)


def derive_keys(master_key: bytes,
                contexts: List[str],
                length: int = 32) -> Dict[str, bytes]:
    """Convenience function for deriving multiple keys"""
    return KeyHierarchy.derive_keys(master_key, contexts, length)