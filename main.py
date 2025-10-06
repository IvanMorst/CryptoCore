#!/usr/bin/env python3
"""
Legacy main.py for backward compatibility
Use cryptocore.py for new CLI interface
"""

import sys
import os

# Добавляем путь для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))


def main():
    print("Note: This is the legacy interface.")
    print("For the new CLI interface, use: python cryptocore.py --help")
    print("Or install with: pip install . and use: cryptocore --help")

    # Здесь может остаться старый код для обратной совместимости
    # или перенаправление на новый интерфейс

    from cryptocore import main as new_main
    new_main()


if __name__ == "__main__":
    main()