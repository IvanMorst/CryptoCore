#!/usr/bin/env python3
"""
HMAC-SHA256 тесты для нашей реализации
"""

import unittest
import tempfile
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mac.hmac import hmac_sha256, hmac_sha256_file, verify_hmac, hmac_sha256_hex


class TestHMACRealValues(unittest.TestCase):
    """
    Тесты с реальными значениями нашей реализации
    """

    def test_actual_implementation_values(self):
        """Тест с реальными значениями реализации"""
        print("🔧 ТЕСТИРОВАНИЕ С РЕАЛЬНЫМИ ЗНАЧЕНИЯМИ РЕАЛИЗАЦИИ")
        print("=" * 60)

        # Test Case 1: Key = 20 bytes of 0x0b, Data = "Hi There"
        key = bytes([0x0b] * 20)
        data = b"Hi There"
        # Теперь ожидаем правильный RFC 4231 результат!
        expected_hex = "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"

        result_bytes = hmac_sha256(key, data)
        result_hex = result_bytes.hex()

        print(f"\nTest Case 1:")
        print(f"   Ключ: {key.hex()}")
        print(f"   Данные: {data}")
        print(f"   Наш HMAC (hex): {result_hex}")
        print(f"   Ожидаемый RFC 4231: {expected_hex}")
        print(f"   Наш совпадает с RFC 4231: {'✅ ДА' if result_hex == expected_hex else '❌ НЕТ'}")

        # Сравниваем байты с байтами
        self.assertEqual(result_bytes, bytes.fromhex(expected_hex))

    def test_hex_convenience_function(self):
        """Тест удобной функции hex"""
        print("\n🎨 ТЕСТ УДОБНОЙ HEX ФУНКЦИИ")
        print("=" * 60)

        key = b"test_key"
        data = b"test_data"

        # Используем hex функцию
        hex_result = hmac_sha256_hex(key, data)
        bytes_result = hmac_sha256(key, data).hex()

        print(f"   Ключ: {key.hex()}")
        print(f"   Данные: {data}")
        print(f"   HMAC (hex функция): {hex_result}")
        print(f"   HMAC (bytes->hex): {bytes_result}")
        print(f"   Совпадают: {'✅ ДА' if hex_result == bytes_result else '❌ НЕТ'}")

        self.assertEqual(hex_result, bytes_result)

    def test_verification_works_with_our_implementation(self):
        """Тест, что верификация работает с нашей реализацией"""
        print("\n🔐 ТЕСТ ВЕРИФИКАЦИИ С НАШЕЙ РЕАЛИЗАЦИЕЙ")
        print("=" * 60)

        key = b"secret_key"
        data = b"important message"

        # Генерируем HMAC нашей реализацией в hex формате
        hmac_bytes = hmac_sha256(key, data)
        hmac_hex = hmac_bytes.hex()

        # Проверяем нашей реализацией (нужна hex строка)
        verification_result = verify_hmac(key, data, hmac_hex)

        print(f"\nТест верификации:")
        print(f"   Ключ: {key}")
        print(f"   Данные: {data}")
        print(f"   Сгенерированный HMAC (hex): {hmac_hex}")
        print(f"   Верификация успешна: {'✅ ДА' if verification_result else '❌ НЕТ'}")

        self.assertTrue(verification_result)

        # Тест с неверным HMAC должен завершиться неудачей
        wrong_hmac = "0000000000000000000000000000000000000000000000000000000000000000"
        verification_failed = verify_hmac(key, data, wrong_hmac)
        self.assertFalse(verification_failed)
        print(f"   Неверный HMAC отклонён: {'✅ ДА' if not verification_failed else '❌ НЕТ'}")

    def test_file_hmac_consistency(self):
        """Тест согласованности файлового HMAC"""
        print("\n📁 ТЕСТ ФАЙЛОВОГО HMAC")
        print("=" * 60)

        test_content = b"File content for HMAC testing"

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.tmp') as f:
            f.write(test_content)
            temp_file = f.name

        try:
            key = b"file_test_key"

            # Compute HMAC for file (возвращает hex строку)
            file_hmac_hex = hmac_sha256_file(key, temp_file)

            # Compute HMAC for content directly (получаем байты, конвертируем в hex)
            content_hmac_bytes = hmac_sha256(key, test_content)
            content_hmac_hex = content_hmac_bytes.hex()

            print(f"\nТест файлового HMAC:")
            print(f"   Файл: {temp_file}")
            print(f"   Размер файла: {len(test_content)} байт")
            print(f"   HMAC из файла: {file_hmac_hex}")
            print(f"   HMAC из памяти: {content_hmac_hex}")
            print(f"   Совпадают: {'✅ ДА' if file_hmac_hex == content_hmac_hex else '❌ НЕТ'}")

            # Сравниваем hex строки
            self.assertEqual(file_hmac_hex, content_hmac_hex)
            print(f"   ✅ Файловый HMAC корректен")

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                print(f"   Файл удален: {temp_file}")

    def test_empty_data_and_key(self):
        """Тест с пустыми данными и ключами"""
        print("\n⚡ ТЕСТ С ПУСТЫМИ ДАННЫМИ")
        print("=" * 60)

        # Пустой ключ
        result1 = hmac_sha256(b"", b"data").hex()
        print(f"   Пустой ключ: {result1[:16]}...")

        # Пустые данные
        result2 = hmac_sha256(b"key", b"").hex()
        print(f"   Пустые данные: {result2[:16]}...")

        # Все пустое
        result3 = hmac_sha256(b"", b"").hex()
        print(f"   Все пустое: {result3[:16]}...")

        # Проверяем, что результаты различаются
        self.assertNotEqual(result1, result2)
        self.assertNotEqual(result1, result3)
        self.assertNotEqual(result2, result3)
        print(f"   ✅ Все результаты различны")

    def test_different_keys_produce_different_hmacs(self):
        """Тест, что разные ключи дают разные HMAC"""
        print("\n🔑 ТЕСТ РАЗНЫХ КЛЮЧЕЙ")
        print("=" * 60)

        data = b"same data"

        key1 = b"key1"
        key2 = b"key2"
        key3 = b"key3"

        hmac1 = hmac_sha256(key1, data).hex()
        hmac2 = hmac_sha256(key2, data).hex()
        hmac3 = hmac_sha256(key3, data).hex()

        print(f"   Данные: {data}")
        print(f"   Ключ1 HMAC: {hmac1[:16]}...")
        print(f"   Ключ2 HMAC: {hmac2[:16]}...")
        print(f"   Ключ3 HMAC: {hmac3[:16]}...")

        # Все HMAC должны быть разными
        self.assertNotEqual(hmac1, hmac2)
        self.assertNotEqual(hmac1, hmac3)
        self.assertNotEqual(hmac2, hmac3)
        print(f"   ✅ Все HMAC различны")

    def test_different_data_produce_different_hmacs(self):
        """Тест, что разные данные дают разные HMAC"""
        print("\n📝 ТЕСТ РАЗНЫХ ДАННЫХ")
        print("=" * 60)

        key = b"same_key"

        data1 = b"data1"
        data2 = b"data2"
        data3 = b"data3"

        hmac1 = hmac_sha256(key, data1).hex()
        hmac2 = hmac_sha256(key, data2).hex()
        hmac3 = hmac_sha256(key, data3).hex()

        print(f"   Ключ: {key}")
        print(f"   Данные1 HMAC: {hmac1[:16]}...")
        print(f"   Данные2 HMAC: {hmac2[:16]}...")
        print(f"   Данные3 HMAC: {hmac3[:16]}...")

        # Все HMAC должны быть разными
        self.assertNotEqual(hmac1, hmac2)
        self.assertNotEqual(hmac1, hmac3)
        self.assertNotEqual(hmac2, hmac3)
        print(f"   ✅ Все HMAC различны")

    def test_hmac_deterministic(self):
        """Тест, что HMAC детерминирован"""
        print("\n🔄 ТЕСТ ДЕТЕРМИНИРОВАННОСТИ")
        print("=" * 60)

        key = b"deterministic_key"
        data = b"test data for determinism"

        # Вычисляем HMAC дважды
        hmac1 = hmac_sha256(key, data).hex()
        hmac2 = hmac_sha256(key, data).hex()

        print(f"   Ключ: {key.hex()[:16]}...")
        print(f"   Данные: {data}")
        print(f"   HMAC 1: {hmac1}")
        print(f"   HMAC 2: {hmac2}")
        print(f"   Совпадают: {'✅ ДА' if hmac1 == hmac2 else '❌ НЕТ'}")

        self.assertEqual(hmac1, hmac2)
        print(f"   ✅ HMAC детерминирован")


def run_hmac_tests():
    """Запуск всех HMAC тестов"""
    print("🔐 HMAC-SHA256 РЕАЛИЗАЦИЯ - ТЕСТИРОВАНИЕ")
    print("=" * 60)
    print("Тестирование нашей реализации HMAC-SHA256")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавляем все тесты
    test_methods = [
        'test_actual_implementation_values',
        'test_hex_convenience_function',
        'test_verification_works_with_our_implementation',
        'test_file_hmac_consistency',
        'test_empty_data_and_key',
        'test_different_keys_produce_different_hmacs',
        'test_different_data_produce_different_hmacs',
        'test_hmac_deterministic'
    ]

    for method in test_methods:
        suite.addTest(TestHMACRealValues(method))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print("📊 HMAC ТЕСТЫ - СВОДКА")
    print("=" * 60)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")

    if result.wasSuccessful():
        print("✅ ВСЕ HMAC ТЕСТЫ ПРОЙДЕНЫ")
    else:
        print("❌ ЕСТЬ ПРОБЛЕМЫ В HMAC РЕАЛИЗАЦИИ")

    print("=" * 60)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_hmac_tests()
    sys.exit(0 if success else 1)