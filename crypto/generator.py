import os
import time
import hashlib
import psutil
from typing import Optional

# Импорт для логирования
try:
    from crypto.crypto_logger import CryptoLogger

    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    print("Warning: CryptoLogger not available, logging disabled")


class Generator:

    @staticmethod
    def _init_logging():
        """Инициализация логирования"""
        if LOGGING_AVAILABLE:
            CryptoLogger.setup_logging()

    @staticmethod
    def generate_random_bytes(num_bytes: int) -> bytes:
        """Генерация криптографически безопасных случайных байтов"""
        Generator._init_logging()

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Generating {num_bytes} random bytes")

        result = Generator.generate_random_bits(num_bytes * 8)

        if LOGGING_AVAILABLE:
            # Проверка энтропии
            entropy = Generator._calculate_entropy(result)
            CryptoLogger.log(
                f"Random bytes generated: {num_bytes} bytes, "
                f"entropy estimate: {entropy:.2f} bits/byte"
            )

            # Логирование образца
            sample_size = min(16, num_bytes)
            sample = result[:sample_size].hex()
            CryptoLogger.log(f"Sample (first {sample_size} bytes): {sample}")

        return result

    @staticmethod
    def generate_random_bits(num_bits: int) -> bytes:
        """Генерация случайных битов с использованием энтропии системы"""
        Generator._init_logging()

        if num_bits <= 0:
            error_msg = f"Number of bits must be positive, got {num_bits}"
            if LOGGING_AVAILABLE:
                CryptoLogger.log(error_msg, is_error=True)
            raise ValueError(error_msg)

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Generating {num_bits} random bits")

        num_bytes = (num_bits + 7) // 8  # Округление вверх
        random_bits = bytearray(num_bytes)

        # Сбор системной энтропии
        if LOGGING_AVAILABLE:
            CryptoLogger.log("Collecting system entropy...")

        free_memory = psutil.virtual_memory().available
        time_entropy = time.time_ns()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"System entropy sources: "
                f"free_memory={free_memory}, "
                f"time_ns={time_entropy}, "
                f"cpu={cpu_percent:.1f}%, "
                f"disk_read={disk_io.read_bytes if disk_io else 0}, "
                f"net_sent={net_io.bytes_sent if net_io else 0}"
            )

        count = 0
        bits_generated = 0
        byte_index = 0
        bit_index = 0
        start_time = time.time()

        while bits_generated < num_bits:
            if count % 1000 == 0:  # Обновляем энтропию каждые 1000 итераций
                free_memory = psutil.virtual_memory().available
                time_entropy = time.time_ns()
                count = 0

            entropy = free_memory ^ time_entropy * count
            hash_result = Generator._hash(str(entropy))

            for i in range(8):
                if bits_generated >= num_bits:
                    break

                bit = (hash_result[i] & 0xFF) % 2
                random_bits[byte_index] |= (bit << (7 - bit_index))

                bits_generated += 1
                count += 1
                bit_index += 1

                if bit_index == 8:
                    byte_index += 1
                    bit_index = 0

        elapsed = time.time() - start_time

        if LOGGING_AVAILABLE:
            CryptoLogger.log_performance("Random bits generation", num_bytes, start_time)

            # Анализ качества случайных данных
            quality_info = Generator._analyze_random_quality(bytes(random_bits))
            CryptoLogger.log(f"Random data quality analysis: {quality_info}")

        return bytes(random_bits)

    @staticmethod
    def _hash(input_str: str) -> bytes:
        """Хеширование строки с использованием SHA-1"""
        # Используем SHA-256 вместо SHA-1 для большей безопасности
        return hashlib.sha256(input_str.encode()).digest()

    @staticmethod
    def generate_test_file(path: str, size: int):
        """Генерация тестового файла со случайными данными"""
        Generator._init_logging()

        if LOGGING_AVAILABLE:
            CryptoLogger.log(f"Generating test file: {path} ({size} bytes)")

        start_time = time.time()

        with open(path, 'wb') as f:
            remaining = size
            chunk_num = 0
            total_written = 0

            while remaining > 0:
                chunk_size = min(remaining, 8192)
                random_data = Generator.generate_random_bytes(chunk_size)
                f.write(random_data)
                remaining -= chunk_size
                total_written += chunk_size
                chunk_num += 1

                # Логирование прогресса
                if LOGGING_AVAILABLE and chunk_num % 100 == 0:
                    progress = ((size - remaining) / size) * 100
                    elapsed = time.time() - start_time
                    speed = total_written / elapsed / 1024 / 1024 if elapsed > 0 else 0

                    CryptoLogger.log(
                        f"Test file generation progress: {progress:.1f}%, "
                        f"speed: {speed:.2f} MB/s, "
                        f"written: {total_written}/{size} bytes"
                    )

        elapsed = time.time() - start_time
        speed_mbps = (size * 8) / elapsed / 1e6 if elapsed > 0 else 0
        speed_mb_s = size / elapsed / 1e6 if elapsed > 0 else 0

        if LOGGING_AVAILABLE:
            CryptoLogger.log_performance("Test file generation", size, start_time)

            CryptoLogger.log(
                f"Test file generated successfully: {path} "
                f"(size: {size} bytes, "
                f"time: {elapsed:.2f}s, "
                f"speed: {speed_mbps:.2f} Mbps / {speed_mb_s:.2f} MB/s)"
            )

            # Проверка созданного файла
            if os.path.exists(path):
                actual_size = os.path.getsize(path)
                if actual_size == size:
                    CryptoLogger.log(f"File verified: {actual_size} bytes written correctly")
                else:
                    CryptoLogger.log(
                        f"File size mismatch: expected {size}, got {actual_size}",
                        is_error=True
                    )

                # Вычисление хеша файла
                try:
                    with open(path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()[:32]
                    CryptoLogger.log(f"Test file SHA-256: {file_hash}")
                except Exception as e:
                    CryptoLogger.log(f"Failed to compute file hash: {e}", is_error=True)

    @staticmethod
    def _calculate_entropy(data: bytes) -> float:
        """Вычисление оценки энтропии данных"""
        if not data:
            return 0.0

        # Подсчет частот байтов
        freq = [0] * 256
        for byte in data:
            freq[byte] += 1

        # Вычисление энтропии Шеннона
        entropy = 0.0
        data_len = len(data)

        for count in freq:
            if count > 0:
                probability = count / data_len
                entropy -= probability * (probability.log2() if probability > 0 else 0)

        return entropy

    @staticmethod
    def _analyze_random_quality(data: bytes) -> str:
        """Анализ качества случайных данных"""
        if len(data) < 16:
            return "Insufficient data for analysis"

        # Проверка на однородность
        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1

        max_count = max(byte_counts)
        min_count = min(byte_counts)
        avg_count = len(data) / 256

        uniformity = 1.0 - (max_count - min_count) / (len(data) if len(data) > 0 else 1)

        # Проверка на последовательности
        sequential_count = 0
        for i in range(len(data) - 1):
            if abs(data[i] - data[i + 1]) == 1:
                sequential_count += 1

        sequential_ratio = sequential_count / (len(data) - 1) if len(data) > 1 else 0

        # Проверка на нули
        zero_count = sum(1 for byte in data if byte == 0)
        zero_ratio = zero_count / len(data) if len(data) > 0 else 0

        # Оценка качества
        quality_score = (
                uniformity * 0.4 +
                (1 - sequential_ratio) * 0.3 +
                (1 - abs(zero_ratio - 0.0039)) * 0.3  # 1/256 ≈ 0.0039
        )

        quality_level = "EXCELLENT" if quality_score > 0.9 else \
            "GOOD" if quality_score > 0.7 else \
                "FAIR" if quality_score > 0.5 else "POOR"

        return (f"quality={quality_level} ({quality_score:.3f}), "
                f"uniformity={uniformity:.3f}, "
                f"sequential={sequential_ratio:.3f}, "
                f"zeros={zero_ratio:.3f}")

    @staticmethod
    def benchmark_generation(iterations: int = 10, size_per_iteration: int = 1024 * 1024):
        """
        Бенчмарк генератора случайных чисел

        Args:
            iterations: количество итераций
            size_per_iteration: размер данных на итерацию в байтах
        """
        Generator._init_logging()

        if LOGGING_AVAILABLE:
            CryptoLogger.log(
                f"Starting benchmark: {iterations} iterations, "
                f"{size_per_iteration} bytes per iteration"
            )

        total_bytes = iterations * size_per_iteration
        start_time = time.time()

        speeds = []
        entropies = []

        for i in range(iterations):
            iter_start = time.time()

            if LOGGING_AVAILABLE:
                CryptoLogger.log(f"Benchmark iteration {i + 1}/{iterations}")

            data = Generator.generate_random_bytes(size_per_iteration)

            iter_time = time.time() - iter_start
            iter_speed = size_per_iteration / iter_time / 1024 / 1024  # MB/s

            speeds.append(iter_speed)
            entropy = Generator._calculate_entropy(data)
            entropies.append(entropy)

            if LOGGING_AVAILABLE:
                CryptoLogger.log(
                    f"Iteration {i + 1}: {size_per_iteration} bytes in {iter_time:.3f}s, "
                    f"speed: {iter_speed:.2f} MB/s, "
                    f"entropy: {entropy:.2f} bits/byte"
                )

        total_time = time.time() - start_time
        avg_speed = total_bytes / total_time / 1024 / 1024
        avg_entropy = sum(entropies) / len(entropies) if entropies else 0

        if LOGGING_AVAILABLE:
            CryptoLogger.log("=" * 60)
            CryptoLogger.log("BENCHMARK RESULTS:")
            CryptoLogger.log(f"  Total time: {total_time:.3f}s")
            CryptoLogger.log(f"  Total data: {total_bytes} bytes ({total_bytes / 1024 / 1024:.2f} MB)")
            CryptoLogger.log(f"  Average speed: {avg_speed:.2f} MB/s")
            CryptoLogger.log(f"  Min speed: {min(speeds):.2f} MB/s")
            CryptoLogger.log(f"  Max speed: {max(speeds):.2f} MB/s")
            CryptoLogger.log(f"  Average entropy: {avg_entropy:.2f} bits/byte")
            CryptoLogger.log("=" * 60)

        return {
            'total_time': total_time,
            'total_bytes': total_bytes,
            'avg_speed_mb_s': avg_speed,
            'avg_entropy': avg_entropy,
            'speeds': speeds,
            'entropies': entropies
        }