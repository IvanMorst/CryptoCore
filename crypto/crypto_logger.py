import logging
import datetime
import os


class CryptoLogger:
    LOG_FILE = "crypto.log"

    @staticmethod
    def setup_logging():
        """Настройка системы логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(CryptoLogger.LOG_FILE),
                logging.StreamHandler()
            ]
        )

    @staticmethod
    def log(message: str, is_error: bool = False):
        """Запись в лог"""
        if is_error:
            logging.error(message)
        else:
            logging.info(message)

    @staticmethod
    def log_performance(operation: str, bytes_processed: int, start_time: float):
        """Логирование производительности"""
        elapsed = time.time() - start_time
        speed = (bytes_processed * 8) / elapsed / 1e6
        CryptoLogger.log(
            f"{operation}: {speed:.2f} Mbps, {bytes_processed} bytes, {elapsed:.2f} s"
        )