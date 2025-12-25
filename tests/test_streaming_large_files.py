#!/usr/bin/env python3
"""
Простой тест потоковой обработки
"""

import os
import time
import hashlib
from crypto.file_processor import FileProcessor
from csprng import generate_key


def test_streaming():
    """Тестирование потоковой обработки"""
    print("Testing streaming file processing...")

    # Создаем тестовый файл 150 MB (больше порога в 100 MB)
    test_file = "streaming_test.bin"
    size_mb = 150

    print(f"\nCreating test file ({size_mb} MB)...")

    with open(test_file, 'wb') as f:
        chunk_size = 64 * 1024 * 1024
        total_size = size_mb * 1024 * 1024
        written = 0

        while written < total_size:
            chunk = os.urandom(min(chunk_size, total_size - written))
            f.write(chunk)
            written += len(chunk)
            progress = (written / total_size) * 100
            print(f"\rProgress: {progress:.1f}%", end='')

    print(f"\n✅ Test file created: {os.path.getsize(test_file) / (1024 * 1024*1024):.1f} MB")

    # Генерируем ключ
    key = generate_key(16)
    print(f"\nTest key: {key.hex()}")

    # Тестируем все режимы
    modes = ["ecb", "cbc", "ctr", "cfb", "ofb"]

    for mode in modes:
        print(f"\n{'=' * 60}")
        print(f"Testing {mode.upper()} mode")
        print(f"{'=' * 60}")

        encrypted_file = f"streaming_test_{mode}_encrypted.bin"
        decrypted_file = f"streaming_test_{mode}_decrypted.bin"

        try:
            # Шифрование
            print(f"\n🔒 Encrypting...")
            start_time = time.time()
            FileProcessor.process_file_streaming(
                input_path=test_file,
                output_path=encrypted_file,
                key=key,
                mode=mode,
                encrypt=True
            )
            encrypt_time = time.time() - start_time
            print(f"Encryption time: {encrypt_time:.2f}s")

            # Дешифрование
            print(f"\n🔓 Decrypting...")
            start_time = time.time()
            FileProcessor.process_file_streaming(
                input_path=encrypted_file,
                output_path=decrypted_file,
                key=key,
                mode=mode,
                encrypt=False
            )
            decrypt_time = time.time() - start_time
            print(f"Decryption time: {decrypt_time:.2f}s")

            # Проверка целостности
            print(f"\n🔍 Verifying integrity...")
            with open(test_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
                original_hash = hashlib.sha256(f1.read()).hexdigest()
                decrypted_hash = hashlib.sha256(f2.read()).hexdigest()

            if original_hash == decrypted_hash:
                print(f"✅ {mode.upper()} SUCCESS!")
            else:
                print(f"❌ {mode.upper()} FAILED!")
                print(f"  Original: {original_hash}")
                print(f"  Decrypted: {decrypted_hash}")

            # Очистка
            for f in [encrypted_file, decrypted_file]:
                if os.path.exists(f):
                    os.remove(f)

        except Exception as e:
            print(f"❌ Error in {mode.upper()}: {e}")
            import traceback
            traceback.print_exc()

    # Очистка тестового файла
    if os.path.exists(test_file):
        os.remove(test_file)

    print(f"\n{'=' * 60}")
    print("Streaming test completed!")


def test_legacy_compatibility():
    """Тестирование совместимости с legacy кодом"""
    print(f"\n\nTesting legacy compatibility...")

    # Создаем маленький тестовый файл (меньше 100 MB)
    test_file = "legacy_test.bin"
    test_data = os.urandom(10 * 1024 * 1024)  # 10 MB

    with open(test_file, 'wb') as f:
        f.write(test_data)

    print(f"Created test file: {len(test_data) / (1024 * 1024):.1f} MB")

    key = generate_key(16)
    print(f"Test key: {key.hex()}")

    # Тестируем legacy режим (должен работать как раньше)
    for mode in ["cbc", "ctr"]:
        print(f"\nTesting {mode.upper()} legacy mode...")

        encrypted_file = f"legacy_test_{mode}_encrypted.bin"
        decrypted_file = f"legacy_test_{mode}_decrypted.bin"

        # Шифрование
        from crypto.cipher_core import CipherCore

        cipher = CipherCore(key, mode)
        with open(test_file, 'rb') as f:
            data = f.read()

        encrypted = cipher.encrypt(data)
        with open(encrypted_file, 'wb') as f:
            f.write(encrypted)

        # Дешифрование
        cipher2 = CipherCore(key, mode)
        with open(encrypted_file, 'rb') as f:
            encrypted_data = f.read()

        decrypted = cipher2.decrypt(encrypted_data)
        with open(decrypted_file, 'wb') as f:
            f.write(decrypted)

        # Проверка
        with open(test_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
            original = f1.read()
            decrypted_data = f2.read()

        if original == decrypted_data:
            print(f"✅ {mode.upper()} legacy compatibility OK!")
        else:
            print(f"❌ {mode.upper()} legacy compatibility FAILED!")

        # Очистка
        for f in [encrypted_file, decrypted_file]:
            if os.path.exists(f):
                os.remove(f)

    # Очистка
    if os.path.exists(test_file):
        os.remove(test_file)


if __name__ == "__main__":
    try:
        test_streaming()
        test_legacy_compatibility()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nTest failed: {e}")
        import traceback

        traceback.print_exc()