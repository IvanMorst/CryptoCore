#!/usr/bin/env python3
"""
Performance and Comparison Tests for CryptoCore Hash Functions
Упрощенная версия с фокусом на корректность
"""

import sys
import os
import time
import tempfile
import subprocess

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hash.sha256 import sha256, sha256_file
from hash.sha3_256 import sha3_256, sha3_256_file


class SimpleHashTests:
    """Упрощенные тесты для проверки корректности"""

    def __init__(self):
        self.results = []

    def print_result(self, test_name, success, details=""):
        """Печать результата теста"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        self.results.append((test_name, success))

    def test_basic_correctness(self):
        """Тест базовой корректности на известных тестовых векторах"""
        print("\n" + "=" * 50)
        print("🧪 ТЕСТ БАЗОВОЙ КОРРЕКТНОСТИ")
        print("=" * 50)

        # NIST тестовые векторы
        test_vectors = [
            (b"",
             "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
             "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"),
            (b"abc",
             "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
             "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"),
            (b"hello world",
             "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
             "644bcc7e564373040999aac89e7622f3ca71fba1d972fd94a31c3bfbf24e3938")
        ]

        all_passed = True
        for i, (data, expected_sha256, expected_sha3) in enumerate(test_vectors):
            print(f"\nТест {i + 1}: {data if data else 'empty string'}")

            # SHA-256
            actual_sha256 = sha256(data)
            sha256_ok = actual_sha256 == expected_sha256
            print(f"  SHA-256:    {actual_sha256}")
            print(f"  Ожидалось:  {expected_sha256}")
            print(f"  SHA-256:    {'✅' if sha256_ok else '❌'}")

            # SHA3-256
            actual_sha3 = sha3_256(data)
            sha3_ok = actual_sha3 == expected_sha3
            print(f"  SHA3-256:   {actual_sha3}")
            print(f"  Ожидалось:  {expected_sha3}")
            print(f"  SHA3-256:   {'✅' if sha3_ok else '❌'}")

            if not (sha256_ok and sha3_ok):
                all_passed = False

        self.print_result("Basic Correctness", all_passed,
                          "Проверка известных тестовых векторов NIST")
        return all_passed

    def test_avalanche_simple(self):
        """Упрощенный тест лавинообразного эффекта"""
        print("\n" + "=" * 50)
        print(" ТЕСТ ЛАВИНООБРАЗНОГО ЭФФЕКТА")
        print("=" * 50)

        message = b"Test message for avalanche"
        modified = bytearray(message)
        modified[0] ^= 0x01  # Меняем один бит

        original_sha256 = sha256(message)
        modified_sha256 = sha256(bytes(modified))
        original_sha3 = sha3_256(message)
        modified_sha3 = sha3_256(bytes(modified))

        # Подсчет отличающихся битов
        def count_diff_bits(hex1, hex2):
            int1 = int(hex1, 16)
            int2 = int(hex2, 16)
            return bin(int1 ^ int2).count('1')

        sha256_diff = count_diff_bits(original_sha256, modified_sha256)
        sha3_diff = count_diff_bits(original_sha3, modified_sha3)

        print(f"Исходное сообщение: {message}")
        print(f"Измененное: {bytes(modified)}")
        print(f"SHA-256 отличается на: {sha256_diff}/256 битов ({sha256_diff / 256 * 100:.1f}%)")
        print(f"SHA3-256 отличается на: {sha3_diff}/256 битов ({sha3_diff / 256 * 100:.1f}%)")

        # Считаем успешным если изменилось >100 битов
        sha256_ok = sha256_diff > 100
        sha3_ok = sha3_diff > 100

        self.print_result("SHA-256 Avalanche", sha256_ok,
                          f"Изменено {sha256_diff}/256 битов")
        self.print_result("SHA3-256 Avalanche", sha3_ok,
                          f"Изменено {sha3_diff}/256 битов")

        return sha256_ok and sha3_ok

    def test_file_hashing(self):
        """Тест хэширования файлов"""
        print("\n" + "=" * 50)
        print("📁 ТЕСТ ХЭШИРОВАНИЯ ФАЙЛОВ")
        print("=" * 50)

        # Создаем тестовый файл
        test_content = b"File content for testing hash functions"
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            f.write(test_content)
            test_file = f.name

        try:
            # Вычисляем хэши
            file_sha256 = sha256_file(test_file)
            file_sha3 = sha3_256_file(test_file)

            # Вычисляем хэши напрямую из содержимого для проверки
            direct_sha256 = sha256(test_content)
            direct_sha3 = sha3_256(test_content)

            sha256_ok = file_sha256 == direct_sha256
            sha3_ok = file_sha3 == direct_sha3

            print(f"Содержимое файла: {test_content}")
            print(f"SHA-256 файл:     {file_sha256}")
            print(f"SHA-256 прямой:   {direct_sha256}")
            print(f"SHA-256:          {'✅' if sha256_ok else '❌'}")

            print(f"SHA3-256 файл:    {file_sha3}")
            print(f"SHA3-256 прямой:  {direct_sha3}")
            print(f"SHA3-256:         {'✅' if sha3_ok else '❌'}")

            self.print_result("SHA-256 File Hashing", sha256_ok)
            self.print_result("SHA3-256 File Hashing", sha3_ok)

            return sha256_ok and sha3_ok

        finally:
            os.unlink(test_file)

    def test_performance_simple(self):
        """Упрощенный тест производительности"""
        print("\n" + "=" * 50)
        print("⚡ ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("=" * 50)

        # Тестируем на небольшом файле
        test_content = b"X" * (100 * 1024)  # 100KB
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            f.write(test_content)
            test_file = f.name

        try:
            # SHA-256
            start_time = time.time()
            sha256_result = sha256_file(test_file)
            sha256_time = time.time() - start_time

            # SHA3-256
            start_time = time.time()
            sha3_result = sha3_256_file(test_file)
            sha3_time = time.time() - start_time

            file_size_kb = len(test_content) / 1024

            print(f"Размер файла: {file_size_kb:.1f} KB")
            print(f"SHA-256 время: {sha256_time:.2f} сек ({file_size_kb / sha256_time:.1f} KB/сек)")
            print(f"SHA3-256 время: {sha3_time:.2f} сек ({file_size_kb / sha3_time:.1f} KB/сек)")
            print(f"Хэш SHA-256: {sha256_result}")
            print(f"Хэш SHA3-256: {sha3_result}")

            # Для учебной реализации приемлемая скорость - хотя бы 10 KB/сек
            sha256_ok = sha256_time < 10  # Не более 10 секунд на 100KB
            sha3_ok = sha3_time < 10

            self.print_result("SHA-256 Performance", sha256_ok,
                              f"{file_size_kb / sha256_time:.1f} KB/сек")
            self.print_result("SHA3-256 Performance", sha3_ok,
                              f"{file_size_kb / sha3_time:.1f} KB/сек")

            return sha256_ok and sha3_ok

        finally:
            os.unlink(test_file)

    def run_diagnostic(self):
        """Диагностика проблем"""
        print("\n" + "=" * 50)
        print("🔍 ДИАГНОСТИКА ПРОБЛЕМ")
        print("=" * 50)

        # Проверяем простейший случай
        test_data = b"a"
        print(f"Тестовые данные: {test_data}")

        sha256_result = sha256(test_data)
        sha3_result = sha3_256(test_data)

        print(f"SHA-256('a'):  {sha256_result}")
        print(f"SHA3-256('a'): {sha3_result}")

        # Ожидаемые значения (можно проверить онлайн)
        expected_sha256_a = "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
        expected_sha3_a = "80084bf2fba02475726feb2cab2d8215eab14bc6bdd8bfb2c8151257032ecd8b"

        print(f"Ожидаемый SHA-256:  {expected_sha256_a}")
        print(f"Ожидаемый SHA3-256: {expected_sha3_a}")

        sha256_match = sha256_result == expected_sha256_a
        sha3_match = sha3_result == expected_sha3_a

        print(f"SHA-256 совпадает:  {'✅' if sha256_match else '❌'}")
        print(f"SHA3-256 совпадает: {'✅' if sha3_match else '❌'}")

        if not sha256_match:
            print("\n⚠️  ПРОБЛЕМА: SHA-256 выдает некорректные значения!")
            print("   Проверьте реализацию в hash/sha256.py")

        if not sha3_match:
            print("\n⚠️  ПРОБЛЕМА: SHA3-256 выдает некорректные значения!")
            print("   Проверьте реализацию в hash/sha3_256.py")

    def run_all_tests(self):
        """Запуск всех упрощенных тестов"""
        print(" ЗАПУСК  ТЕСТОВ ХЭШ-ФУНКЦИЙ")
        print("Фокус на корректность вместо производительности")

        # Диагностика сначала
        self.run_diagnostic()

        # Затем основные тесты
        tests = [
            self.test_basic_correctness,
            self.test_avalanche_simple,
            self.test_file_hashing,
            self.test_performance_simple
        ]

        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Тест упал с ошибкой: {e}")

        # Итоги
        print("\n" + "=" * 50)
        print("📊 ИТОГИ ТЕСТИРОВАНИЯ")
        print("=" * 50)

        total = len(self.results)
        passed = sum(1 for _, success in self.results if success)

        print(f"Всего тестов: {total}")
        print(f"Пройдено: {passed}")
        print(f"Успешность: {passed / total * 100:.1f}%")

        # Рекомендации
        if passed < total:
            print("\n РЕКОМЕНДАЦИИ:")
            print("1. Сначала исправьте корректность хэшей (тест Basic Correctness)")
            print("2. Убедитесь, что известные тестовые векторы проходят")
            print("3. Затем можно оптимизировать производительность")

        return passed == total


if __name__ == '__main__':
    tester = SimpleHashTests()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)