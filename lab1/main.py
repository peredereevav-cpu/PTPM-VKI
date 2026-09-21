"""Лабораторная работа №1. Вариант 1.

Подготовка проекта для тестирования, работа с СКВ, логирование и отладка.
"""

import logging
import os
import sys

# --- Настройка логирования (выполняется ДО импорта модулей проекта) ---
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(LOG_DIR, "file_txt.log"), encoding="utf-8"),
    ],
)

from triangle import process_triangle  # noqa: E402  (импорт после настройки логов)


def Main():
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    # Пример входных данных. Можно заменить на input() для интерактивного режима.
    test_cases = [
        ("3", "3", "3"),        # равносторонний
        ("3", "3", "5"),        # равнобедренный
        ("3", "4", "5"),        # разносторонний
        ("1", "1", "10"),       # не треугольник
        ("abc", "4", "5"),      # нечисловые данные
        ("-3", "4", "5"),       # не положительное число
    ]

    for case in test_cases:
        try:
            logging.info("Входные данные: %s", case)
            triangle_type, vertices = process_triangle(*case)
            logging.info("Результат: тип=%r, вершины=%s", triangle_type, vertices)
        except Exception:
            logging.error("Ошибка при обработке случая %s", case)
            logging.exception("Трассировка:")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    Main()