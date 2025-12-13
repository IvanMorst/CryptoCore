"""
MAC (Message Authentication Code) module for CryptoCore
"""

from .hmac import HMAC, hmac_sha256, hmac_sha256_file

__all__ = ['HMAC', 'hmac_sha256', 'hmac_sha256_file']