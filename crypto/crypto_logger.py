import logging
import datetime
import os
import time  # <-- Добавляем импорт time


class CryptoLogger:
    LOG_FILE = "crypto.log"
    _is_initialized = False

    @staticmethod
    def setup_logging():
        """Настройка системы логирования"""
        if CryptoLogger._is_initialized:
            return

        # Создаем директорию для логов если её нет
        log_dir = os.path.dirname(CryptoLogger.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Настраиваем логирование
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(CryptoLogger.LOG_FILE, mode='a', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        CryptoLogger._is_initialized = True

        # Логируем запуск системы
        CryptoLogger.log("=" * 60)
        CryptoLogger.log("CryptoCore System Started")
        CryptoLogger.log(f"Timestamp: {datetime.datetime.now()}")
        CryptoLogger.log("=" * 60)

    @staticmethod
    def log(message: str, is_error: bool = False):
        """Запись в лог"""
        if not CryptoLogger._is_initialized:
            CryptoLogger.setup_logging()

        if is_error:
            logging.error(message)
        else:
            logging.info(message)

    @staticmethod
    def log_performance(operation: str, bytes_processed: int, start_time: float):
        """Логирование производительности"""
        elapsed = time.time() - start_time
        if elapsed > 0:
            speed_mbps = (bytes_processed * 8) / elapsed / 1e6
            speed_mb_s = bytes_processed / elapsed / 1e6
        else:
            speed_mbps = 0
            speed_mb_s = 0

        message = (f"{operation}: {bytes_processed} bytes processed in "
                   f"{elapsed:.2f}s ({speed_mbps:.2f} Mbps, {speed_mb_s:.2f} MB/s)")
        CryptoLogger.log(message)

    @staticmethod
    def log_operation(operation: str, details: dict):
        """Логирование криптографической операции"""
        if not CryptoLogger._is_initialized:
            CryptoLogger.setup_logging()

        log_msg = f"OPERATION: {operation}\n"
        for key, value in details.items():
            log_msg += f"  {key}: {value}\n"

        CryptoLogger.log(log_msg)

    @staticmethod
    def log_key_generation(key_info: dict):
        """Логирование генерации ключа"""
        if not CryptoLogger._is_initialized:
            CryptoLogger.setup_logging()

        log_msg = "KEY GENERATION:\n"
        for key, value in key_info.items():
            log_msg += f"  {key}: {value}\n"

        CryptoLogger.log(log_msg)

    @staticmethod
    def log_file_operation(operation: str, input_file: str, output_file: str = None,
                           key_info: dict = None):
        """Логирование файловой операции"""
        if not CryptoLogger._is_initialized:
            CryptoLogger.setup_logging()

        log_msg = f"FILE {operation.upper()}:\n"
        log_msg += f"  Input: {input_file}\n"
        if output_file:
            log_msg += f"  Output: {output_file}\n"
        if key_info:
            log_msg += f"  Key: {key_info.get('hex', 'N/A')}\n"
            log_msg += f"  Algorithm: {key_info.get('algorithm', 'N/A')}\n"
            log_msg += f"  Mode: {key_info.get('mode', 'N/A')}\n"

        CryptoLogger.log(log_msg)