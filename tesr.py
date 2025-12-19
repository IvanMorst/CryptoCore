#!/usr/bin/env python3
"""Simple HMAC debug"""

from mac.hmac import hmac_sha256
import hmac as py_hmac
import hashlib

print("Simple HMAC Debug")
print("=" * 60)

# Test 1: RFC 4231 Test Vector 1
key = b'\x0b' * 20
data = b'Hi There'

print(f"Test 1: RFC 4231 Vector 1")
print(f"  Key: {key.hex()}")
print(f"  Data: {data}")

our = hmac_sha256(key, data)
py = py_hmac.new(key, data, hashlib.sha256).digest()

print(f"  Our HMAC:   {our.hex()}")
print(f"  Python HMAC: {py.hex()}")
print(f"  Match: {our == py}")
print(f"  Expected RFC 4231: b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")

# Test 2: Simple test
key2 = b'key'
data2 = b'The quick brown fox jumps over the lazy dog'

print(f"\nTest 2: Simple test")
print(f"  Key: '{key2.decode()}'")
print(f"  Data: '{data2.decode()}'")

our2 = hmac_sha256(key2, data2)
py2 = py_hmac.new(key2, data2, hashlib.sha256).digest()

print(f"  Our HMAC:   {our2.hex()}")
print(f"  Python HMAC: {py2.hex()}")
print(f"  Match: {our2 == py2}")