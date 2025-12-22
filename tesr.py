# quick_test.py
from mac.hmac import hmac_sha256

# RFC 4231 Test Case 1
key = bytes([0x0b] * 20)
data = b"Hi There"
expected = "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"

result = hmac_sha256(key, data).hex()
print(f"HMAC результат: {result}")
print(f"Ожидаемый RFC 4231: {expected}")
print(f"Совпадает: {result == expected}")