### **docs/USERGUIDE.md**

# CryptoCore User Guide

## Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Encryption & Decryption](#encryption--decryption)
4. [Hashing](#hashing)
5. [Message Authentication](#message-authentication)
6. [Key Derivation](#key-derivation)
7. [Authenticated Encryption](#authenticated-encryption)
8. [Troubleshooting](#troubleshooting)
9. [Security Best Practices](#security-best-practices)
10. [Cheat Sheet](#cheat-sheet)

## Installation

### From Source
```bash

# Clone the repository

git clone https://github.com/IvanMorst/CryptoCore.git

cd CryptoCore
```
### Create virtual environment
```bash

python -m venv venv
```
### Activate virtual environment
```bash

 On Windows:
venv\Scripts\activate
 On Linux/Mac:
source venv/bin/activate
```

## Basic Usage
### CryptoCore provides a command-line interface (CLI) with subcommands:

```bash
# General syntax
python <command> [options]

# Get help

```bash
python --help
````

### Available commands:
````
encrypt: File encryption/decryption

dgst: Hash and HMAC computation

derive: Key derivation from passwords
````
## Encryption & Decryption

### Basic Encryption

### Encrypt file with AES-128 in CBC mode
```bash
python encrypt --algorithm aes --mode cbc --encrypt \
  --key 00112233445566778899aabbccddeeff \
  --input plaintext.txt --output ciphertext.bin
```
### Decrypt file
```bash
python encrypt --algorithm aes --mode cbc --decrypt \
  --key 00112233445566778899aabbccddeeff \
  --input ciphertext.bin --output decrypted.txt
  ```

### Using Different Modes
```bash
# CTR mode (stream cipher, no padding)
python encrypt --algorithm aes --mode ctr --encrypt \
  --key aabbccddeeff00112233445566778899 \
  --input data.bin
```
# CFB mode
```bash
python encrypt --algorithm aes --mode cfb --encrypt \
  --key 11223344556677889900aabbccddeeff \
  --input document.pdf
```
# OFB mode
```bash
python encrypt --algorithm aes --mode ofb --encrypt \
  --key 223344556677889900aabbccddeeff11 \
  --input image.jpg
  ```

### Key Generation

### Generate random key and encrypt
```bash
python encrypt --algorithm aes --mode cbc --encrypt \
  --input secret.txt
  ```
### Key will be generated and displayed: "Generated random key: xxxx..."

### Different Key Sizes
```bash
# AES-256 (32-byte key, 64 hex characters)
python encrypt --algorithm aes --mode cbc --encrypt \
  --key 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff \
  --input important.docx
```
### AES-192 (24-byte key, 48 hex characters)
```bash
python encrypt --algorithm aes --mode ctr --encrypt \
  --key 00112233445566778899aabbccddeeff001122334455 \
  --input backup.tar
  ```
## Hashing

### File Hashing

### Compute SHA-256 hash
```bash
python dgst --algorithm sha256 --input document.pdf
```
### Compute SHA3-256 hash
```bash
python dgst --algorithm sha3-256 --input data.bin
```
### Save hash to file
```bash
python dgst --algorithm sha256 --input file.txt --output file.sha256
```
## Hash Verification

### Create hash file
```bash
python dgst --algorithm sha256 --input original.txt --output original.sha256
```
### Verify hash (manually)
```bash
python dgst --algorithm sha256 --input downloaded.txt
````

### Compare output with saved hash

### Or let python verify
```bash
echo "expected_hash  downloaded.txt" > expected.sha256
```
# You would compare manually in current version

## Message Authentication
### HMAC Generation
```bash
# Generate HMAC-SHA256 for file
python dgst --algorithm sha256 --hmac \
  --key 00112233445566778899aabbccddeeff \
  --input message.txt
```
# Save HMAC to file
```bash
python dgst --algorithm sha256 --hmac \
  --key mysecretkey1234567890abcdef \
  --input data.csv --output data.hmac
  ```
## HMAC Verification
```bash
# Generate HMAC for verification
echo "correct_hmac_value_here  file.txt" > expected.hmac
```
# In practice, you would compare the output:
```bash
python dgst --algorithm sha256 --hmac \
  --key mysecretkey1234567890abcdef \
  --input file.txt
  ```
### Manually compare with expected.hmac
## Key Derivation
### From Password
```bash
# Derive key from password with specific salt
python derive --password "MySecurePassword123!" \
  --salt a1b2c3d4e5f601234567890123456789 \
  --iterations 100000 --length 32
```
# Derive key with auto-generated salt
```bash
python derive --password "AnotherPassword" \
  --iterations 500000 --length 16
  ```
# Output: DERIVED_KEY_HEX GENERATED_SALT_HEX

# Save derived key to file

```bash

python derive --password "app_key" \
  --iterations 100000 --length 32 --output app.key
  ```

## Practical Example
```bash
# Generate encryption key from password
python derive --password "$(cat ~/.secure_password)" \
  --iterations 100000 --length 32 > derived_key.txt
```

### Extract key and use for encryption
````
KEY=$(cut -d' ' -f1 derived_key.txt)
SALT=$(cut -d' ' -f2 derived_key.txt)
````

python encrypt --algorithm aes --mode gcm --encrypt \
  --key $KEY --input sensitive.dat

## Authenticated Encryption
### GCM Encryption with AAD
```bash
# Encrypt with Additional Authenticated Data (AAD)
python encrypt --algorithm aes --mode gcm --encrypt \
  --key 00112233445566778899aabbccddeeff \
  --input plaintext.txt --output ciphertext.bin \
  --aad aabbccddeeff00112233445566778899
```
### Decrypt with same AAD
```bash
python encrypt --algorithm aes --mode gcm --decrypt \
  --key 00112233445566778899aabbccddeeff \
  --input ciphertext.bin --output decrypted.txt \
  --aad aabbccddeeff00112233445566778899
  ```
## AAD Examples

### Enable verbose output
``````
export CRYPTOCORE_DEBUG=1
python encrypt --algorithm aes --mode cbc --encrypt \
  --key 00112233445566778899aabbccddeeff \
  --input test.txt
``````
# Check log file
tail -f crypto.log
## Security Best Practices
### Key Management
````
Never hardcode keys in scripts or source code

Use password-based key derivation (PBKDF2) for user passwords

Store keys securely - use key management systems in production

Rotate keys regularly for long-term data protection

Use different keys for different purposes
````
Encryption Practices
Prefer GCM mode for authenticated encryption

Always use unique IV/nonce for each encryption

Include AAD when context matters (metadata protection)

Avoid ECB mode - it reveals data patterns

Validate all inputs before cryptographic operations

Password Security
Use strong passwords (≥12 characters, mixed character sets)

High iteration counts for PBKDF2 (≥100,000)

Unique salts for each password derivation

Never reuse passwords across different systems

Operational Security
Clear sensitive data from memory after use

Secure deletion of temporary files

Audit logs for cryptographic operations

Regular updates to address vulnerabilities

## Cheat Sheet
### Quick Reference
### Encryption
```bash
### AES-CBC encryption
python encrypt --algorithm aes --mode cbc --encrypt --key HEX_KEY --input FILE

###  AES-CTR encryption (no padding)
python encrypt --algorithm aes --mode ctr --encrypt --key HEX_KEY --input FILE

### AES-GCM with AAD
python encrypt --algorithm aes --mode gcm --encrypt --key HEX_KEY --input FILE --aad HEX_AAD
Hashing
bash
### SHA-256
python dgst --algorithm sha256 --input FILE

### SHA3-256
python dgst --algorithm sha3-256 --input FILE
HMAC
bash
### HMAC-SHA256
python dgst --algorithm sha256 --hmac --key HEX_KEY --input FILE
Key Derivation
bash
### PBKDF2
python derive --password "PASSWORD" --iterations 100000 --length 32
Common Key Sizes
AES-128: 16 bytes (32 hex characters)

AES-192: 24 bytes (48 hex characters)

AES-256: 32 bytes (64 hex characters)

IV/nonce: 16 bytes (typically), 12 bytes for GCM

SHA-256 hash: 32 bytes (64 hex characters)

HMAC-SHA256: 32 bytes (64 hex characters)

GCM tag: 16 bytes (32 hex characters)
```

## File Extensions Convention
````
.enc - Encrypted files

.dec - Decrypted files

.sha256 - SHA-256 hash files

.hmac - HMAC files

.key - Key files
````
Example Workflow
```bash
### 1. Generate strong key
KEY=$(openssl rand -hex 32)

### 2. Encrypt file
python encrypt --algorithm aes --mode gcm --encrypt \
  --key $KEY --input document.pdf --output document.pdf.enc

### 3. Create hash for verification
python dgst --algorithm sha256 --input document.pdf > document.pdf.sha256

### 4. Decrypt when needed
python encrypt --algorithm aes --mode gcm --decrypt \
  --key $KEY --input document.pdf.enc --output document_restored.pdf

### 5. Verify integrity
python dgst --algorithm sha256 --input document_restored.pdf
# Compare with saved hash
```
### Getting Help
``````
Check --help for any command

Review this user guide

Examine example commands in README.md

Check log file crypto.log for detailed information

File issues on GitHub for bugs or questions

Remember: Cryptography is complex. When in doubt, consult with security professionals for critical applications.
``````
text
