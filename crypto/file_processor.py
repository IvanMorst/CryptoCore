import os
import sys
import time
import hashlib
from crypto.cipher_core import CipherCore
from crypto.crypto_logger import CryptoLogger

try:
    from crypto.crypto_logger import CryptoLogger

    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    print("Warning: CryptoLogger not available, logging disabled")


class FileProcessor:
    CHUNK_SIZE = 64 * 1024 * 1024  # 64 МБ

    @staticmethod
    def _init_logging():
        if LOGGING_AVAILABLE:
            CryptoLogger.setup_logging()

    @staticmethod
    def _print_progress(current: int, total: int, speed: float = None,
                        chunk_num: int = None, total_chunks: int = None):
        """Вывод прогресса без использования CryptoLogger.log_progress"""
        percent = (current / total) * 100 if total > 0 else 0
        current_mb = current / (1024 * 1024)
        total_mb = total / (1024 * 1024)

        message = f"\rProgress: {current_mb:.1f}/{total_mb:.1f} MB ({percent:.1f}%)"

        if speed:
            message += f" | Speed: {speed:.1f} MB/s"

        if chunk_num and total_chunks:
            message += f" | Chunk: {chunk_num}/{total_chunks}"

        sys.stdout.write(message)
        sys.stdout.flush()

    @staticmethod
    def _process_ecb_cbc_streaming(input_path: str, output_path: str, key: bytes,
                                   mode: str, encrypt: bool, iv: bytes = None):
        """
        🆕 СПЕЦИАЛЬНАЯ ОБРАБОТКА ДЛЯ ECB И CBC
        Эти режимы требуют особой обработки из-за паддинга
        """
        FileProcessor._init_logging()

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        file_size = os.path.getsize(input_path)
        operation = "ENCRYPTION" if encrypt else "DECRYPTION"

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"Starting SPECIAL {operation} for {mode.upper()}\n"
                f"   Input: {input_path}\n"
                f"   Output: {output_path}\n"
                f"   Size: {file_size:,} bytes"
            )

        print(f"\n Starting {operation.lower()} in {mode.upper()} mode...")
        print(f"   File size: {file_size / (1024 * 1024):.2f} MB")

        start_time = time.time()

        try:
            # 🆕 Для ECB/CBC используем упрощенный подход
            if encrypt:
                # Шифрование: читаем весь файл и шифруем целиком
                # Это не потоково, но гарантирует корректность паддинга
                with open(input_path, 'rb') as f:
                    data = f.read()

                cipher = CipherCore(key, mode, iv)
                encrypted = cipher.encrypt(data)

                with open(output_path, 'wb') as f:
                    f.write(encrypted)

                if LOGGING_AVAILABLE:
                    CryptoLogger.log(f"Encrypted {len(data)} -> {len(encrypted)} bytes")

            else:
                # Дешифрование: также читаем весь файл
                with open(input_path, 'rb') as f:
                    data = f.read()

                cipher = CipherCore(key, mode, iv)
                decrypted = cipher.decrypt(data)

                with open(output_path, 'wb') as f:
                    f.write(decrypted)

                if LOGGING_AVAILABLE:
                    CryptoLogger.log(f"Decrypted {len(data)} -> {len(decrypted)} bytes")

            # Финальное сообщение
            total_time = time.time() - start_time
            speed = file_size / total_time / (1024 * 1024) if total_time > 0 else 0

            print(f"\n {operation} completed successfully!")
            print(f"   Total time: {total_time:.2f}s")
            print(f"   Speed: {speed:.2f} MB/s")

            if LOGGING_AVAILABLE:
                CryptoLogger.log(f" {operation} completed in {total_time:.2f}s")

        except Exception as e:
            error_msg = f"\n {operation} FAILED: {str(e)}"
            print(error_msg)

            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
                import traceback
                CryptoLogger.log(traceback.format_exc(), is_error=True)

            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass

            raise e

    @staticmethod
    def process_file_streaming(input_path: str, output_path: str, key: bytes,
                               mode: str, encrypt: bool, iv: bytes = None):
        """
        Потоковая обработка для режимов, которые её поддерживают (CFB, OFB, CTR)
        """
        FileProcessor._init_logging()

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # 🆕 Если режим ECB или CBC, используем специальную обработку
        if mode in ['ecb', 'cbc']:
            return FileProcessor._process_ecb_cbc_streaming(
                input_path, output_path, key, mode, encrypt, iv
            )

        file_size = os.path.getsize(input_path)
        operation = "ENCRYPTION" if encrypt else "DECRYPTION"
        total_chunks = (file_size + FileProcessor.CHUNK_SIZE - 1) // FileProcessor.CHUNK_SIZE

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f" Starting STREAMING {operation} in {mode.upper()} mode\n"
                f"   Input: {input_path}\n"
                f"   Output: {output_path}\n"
                f"   Size: {file_size:,} bytes\n"
                f"   Chunks: {total_chunks}"
            )

        print(f"\n Starting {operation.lower()} in {mode.upper()} mode...")
        print(f"   File size: {file_size / (1024 * 1024):.2f} MB")
        print(f"   Total chunks: {total_chunks}")

        start_time = time.time()

        try:
            with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
                # Инициализация шифра
                if encrypt:
                    cipher = CipherCore(key, mode, iv)
                    # Записываем IV в начало файла (кроме ECB)
                    if mode != 'ecb':
                        outfile.write(cipher.get_iv())
                        if LOGGING_AVAILABLE:
                            CryptoLogger.log(f"Written IV: {cipher.get_iv().hex()}")
                else:
                    if mode == 'ecb':
                        cipher = CipherCore(key, mode)
                    else:
                        # Читаем IV из файла
                        iv_from_file = infile.read(16)
                        if len(iv_from_file) != 16:
                            raise ValueError(f"Invalid IV in file: {len(iv_from_file)} bytes")
                        cipher = CipherCore(key, mode, iv_from_file)
                        if LOGGING_AVAILABLE:
                            CryptoLogger.log(f"Read IV: {iv_from_file.hex()}")

                processed_bytes = 0
                chunk_num = 0

                print(f"\n📊 Progress:")
                FileProcessor._print_progress(0, file_size, chunk_num=0, total_chunks=total_chunks)

                while True:
                    chunk_start_time = time.time()
                    chunk = infile.read(FileProcessor.CHUNK_SIZE)

                    if not chunk:
                        break

                    chunk_num += 1
                    chunk_size = len(chunk)
                    processed_bytes += chunk_size

                    # Определяем последний ли это чанк
                    is_last_chunk = (chunk_size < FileProcessor.CHUNK_SIZE) or (processed_bytes >= file_size)

                    # Обработка чанка
                    if encrypt:
                        processed_chunk = cipher.encrypt_chunk(chunk, is_final=is_last_chunk)
                    else:
                        processed_chunk = cipher.decrypt_chunk(chunk, is_final=is_last_chunk)

                    outfile.write(processed_chunk)

                    # Обновление прогресса
                    chunk_time = time.time() - chunk_start_time
                    speed = chunk_size / chunk_time / (1024 * 1024) if chunk_time > 0 else 0

                    FileProcessor._print_progress(
                        processed_bytes, file_size, speed, chunk_num, total_chunks
                    )

                    if LOGGING_AVAILABLE:
                        CryptoLogger.log(
                            f"Chunk {chunk_num}: {chunk_size / (1024 * 1024):.2f} MB, "
                            f"speed: {speed:.1f} MB/s"
                        )

                # Финальное сообщение
                print()  # Новая строка
                total_time = time.time() - start_time
                avg_speed = processed_bytes / total_time / (1024 * 1024) if total_time > 0 else 0

                print(f"\n {operation} completed successfully!")
                print(f"   Total time: {total_time:.2f}s")
                print(f"   Average speed: {avg_speed:.2f} MB/s")
                print(f"   Chunks processed: {chunk_num}")

                if LOGGING_AVAILABLE:
                    CryptoLogger.log(
                        f" STREAMING {operation} COMPLETED\n"
                        f"   Total time: {total_time:.2f}s\n"
                        f"   Average speed: {avg_speed:.2f} MB/s"
                    )

        except Exception as e:
            error_msg = f"\n {operation} FAILED: {str(e)}"
            print(error_msg)

            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
                import traceback
                CryptoLogger.log(traceback.format_exc(), is_error=True)

            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass

            raise e

    @staticmethod
    def process_file_legacy(input_path: str, output_path: str, key: bytes,
                            mode: str, encrypt: bool, iv: bytes = None):
        """Оригинальная обработка файла"""
        FileProcessor._init_logging()

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Using LEGACY processing for {input_path}")

        # Читаем весь файл в память
        with open(input_path, 'rb') as f:
            data = f.read()

        cipher = CipherCore(key, mode, iv)

        if encrypt:
            encrypted = cipher.encrypt(data)
            with open(output_path, 'wb') as f:
                f.write(encrypted)
        else:
            decrypted = cipher.decrypt(data)
            with open(output_path, 'wb') as f:
                f.write(decrypted)

    @staticmethod
    def process_file(input_path: str, output_path: str, key: bytes,
                     mode: str, encrypt: bool, iv: bytes = None):
        """
        Универсальная обработка файла
        """
        file_size = os.path.getsize(input_path)

        # 🆕 Для GCM всегда используем legacy режим
        if mode == 'gcm':
            if LOGGING_AVAILABLE:
                CryptoLogger.log(f"GCM mode detected, using legacy processing")
            return FileProcessor.process_file_legacy(input_path, output_path, key, mode, encrypt, iv)

        # 🆕 Для ECB и CBC всегда используем специальную обработку (не потоковую)
        if mode in ['ecb', 'cbc']:
            return FileProcessor._process_ecb_cbc_streaming(input_path, output_path, key, mode, encrypt, iv)

        # Для остальных режимов: если файл большой (>100MB), используем потоковую обработку
        if file_size > 100 * 1024 * 1024:  # 100 MB
            if LOGGING_AVAILABLE:
                CryptoLogger.log(f"File size {file_size / (1024 * 1024):.1f} MB > 100 MB, using STREAMING mode")
            return FileProcessor.process_file_streaming(input_path, output_path, key, mode, encrypt, iv)
        else:
            if LOGGING_AVAILABLE:
                CryptoLogger.log(f"File size {file_size / (1024 * 1024):.1f} MB <= 100 MB, using LEGACY mode")
            return FileProcessor.process_file_legacy(input_path, output_path, key, mode, encrypt, iv)


def encrypt_file(input_path: str, output_path: str, key: bytes, mode: str = 'ecb') -> bool:
    try:
        FileProcessor.process_file(input_path, output_path, key, mode, encrypt=True)
        return True
    except Exception as e:
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"File encryption failed: {e}", is_error=True)
        return False


def decrypt_file(input_path: str, output_path: str, key: bytes, mode: str = 'ecb') -> bool:
    try:
        FileProcessor.process_file(input_path, output_path, key, mode, encrypt=False)
        return True
    except Exception as e:
        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"File decryption failed: {e}", is_error=True)
        return False