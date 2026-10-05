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

from triangle import process_triangle  # noqa: E402


# Команды для выхода из программы
EXIT_COMMANDS = {"exit", "quit", "q", "выход"}


def _read_side(prompt: str) -> str:
    """
    Запрашивает у пользователя сторону.
    Если пользователь ввёл команду выхода — возвращает её же (обработается выше).
    """
    return input(prompt).strip()


def Main():
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    print("=" * 60)
    print("Вычисление вида треугольника и координат его вершин")
    print("Введите длины трёх сторон (можно дробные числа, например 3.5).")
    print("Для выхода введите: exit, quit, q или выход.")
    print("=" * 60)

    while True:  # <-- бесконечный цикл
        try:
            side_a = _read_side("Сторона A: ")
            if side_a.lower() in EXIT_COMMANDS:
                logging.info("Пользователь запросил выход (на стороне A)")
                break

            side_b = _read_side("Сторона B: ")
            if side_b.lower() in EXIT_COMMANDS:
                logging.info("Пользователь запросил выход (на стороне B)")
                break

            side_c = _read_side("Сторона C: ")
            if side_c.lower() in EXIT_COMMANDS:
                logging.info("Пользователь запросил выход (на стороне C)")
                break

            logging.info(
                "Входные данные: A=%r, B=%r, C=%r", side_a, side_b, side_c
            )

            triangle_type, vertices = process_triangle(side_a, side_b, side_c)

            # Красивый вывод результата пользователю
            print("-" * 60)
            if triangle_type == "":
                print("Результат: ошибка входных данных (не число)")
            elif triangle_type == "не треугольник":
                print("Результат: треугольник с такими сторонами не существует")
            else:
                print(f"Тип треугольника: {triangle_type}")
                print(f"Координаты вершин: {vertices}")
            print("-" * 60)

            logging.info(
                "Результат: тип=%r, вершины=%s", triangle_type, vertices
            )

        except KeyboardInterrupt:
            # Ctrl+C — вежливо выходим
            logging.info("Прервано пользователем (Ctrl+C)")
            print("\nВыход по Ctrl+C.")
            break

        except Exception:
            # Ловим всё остальное, чтобы программа не падала
            logging.error("Непредвиденная ошибка в цикле")
            logging.exception("Трассировка:")
            print("Произошла непредвиденная ошибка, попробуйте снова.\n")

    logging.info("Приложение завершено")
    print("До свидания!")


if __name__ == "__main__":
    Main()