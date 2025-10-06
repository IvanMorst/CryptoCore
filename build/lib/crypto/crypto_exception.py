class CryptoException(Exception):
    """Кастомное исключение для криптосистемы"""
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(message)
        self.original_exception = original_exception
        from .crypto_logger import CryptoLogger
        CryptoLogger.log(f"CRYPTO ERROR: {message}", True)
        if original_exception:
            CryptoLogger.log(f"Original exception: {str(original_exception)}", True)