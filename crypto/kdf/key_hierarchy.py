"""
Key Hierarchy Function - Deriving multiple keys from a master key
Deterministic HMAC-based key derivation
"""

import struct  # <-- ДОБАВИТЬ ИМПОРТ
from typing import Union
from mac.hmac import HMAC


class KeyHierarchy:
    """
    Key hierarchy for deriving multiple keys from a master key
    """

    @staticmethod
    def derive_key(master_key: bytes,
                   context: Union[str, bytes],
                   length: int = 32) -> bytes:
        """
        Derive a key from a master key using deterministic HMAC-based method

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

        derived = b''
        counter = 1

        # Generate enough HMAC output to meet length requirement
        while len(derived) < length:
            # T_i = HMAC(master_key, context || INT_32_BE(counter))
            block_data = context + struct.pack('>I', counter)
            hmac = HMAC(master_key, 'sha256')
            block = hmac.compute(block_data)
            derived += block
            counter += 1

        # Return exactly requested length
        return derived[:length]

    @staticmethod
    def derive_keys(master_key: bytes,
                    contexts: list,
                    length: int = 32) -> dict:
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
                contexts: list,
                length: int = 32) -> dict:
    """Convenience function for deriving multiple keys"""
    return KeyHierarchy.derive_keys(master_key, contexts, length)