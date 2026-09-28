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

    print("ВВедите длины сторон треугольника")
    side_a = input("Сторона A:")
    side_b = input("Сторона B:")
    side_c = input("Сторона C:")

    logging.info("Пользовательский ввод: A=%r, B=%r, C=%r", side_a, side_b, side_c)

    try:
        triangle_type, vertices = process_triangle(side_a, side_b, side_c)
        logging.info("Результат: тип=%r, вершины=%s", triangle_type, vertices)
        print("\n--- Результат ---")
        print(f"Тип треугольника: {triangle_type if triangle_type else '(пусто)'}")
        print(f"Координаты вершин: {vertices}")

    except Exception:
        logging.error("Ошибка при обработке ввода")
        logging.exception("Трассировка:")
        print("Произошла непредвиденная ошибка. Подробности в логе.")
    #Пример входных данных. Можно заменить на input() для интерактивного режима.
    # test_cases = [
    #     ("0.2", "0.3", "0.5"),        # равносторонний
    #     ("3", "3", "5"),        # равнобедренный
    #     ("3", "4", "5"),        # разносторонний
    #     ("1", "1", "10"),       # не треугольник
    #     ("abc", "4", "5"),      # нечисловые данные
    #     ("-3", "4", "5"),       # не положительное число
    # ]
    #
    # for case in test_cases:
    #     try:
    #         logging.info("Входные данные: %s", case)
    #         triangle_type, vertices = process_triangle(*case)
    #         logging.info("Результат: тип=%r, вершины=%s", triangle_type, vertices)
    #     except Exception:
    #         logging.error("Ошибка при обработке случая %s", case)
    #         logging.exception("Трассировка:")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    Main()