"""Модуль для определения вида треугольника и расчёта координат его вершин."""

import math
import logging

logger = logging.getLogger(__name__)

# Размер поля для отрисовки
FIELD_SIZE = 100
MARGIN = 10  # отступ, чтобы треугольник помещался в поле 100x100


def _parse_side(value: str):
    """
    Пытается преобразовать строку в положительное число float.

    :return: (float, None) при успехе; (None, "not_a_number") если не число;
             (None, "not_positive") если число <= 0.
    """
    try:
        number = float(value.strip())
    except (ValueError, AttributeError, TypeError):
        return None, "not_a_number"

    if number <= 0:
        return None, "not_positive"

    return number, None


def _define_triangle_type(a: float, b: float, c: float) -> str:
    """Возвращает вид треугольника или 'не треугольник'."""
    # Проверка неравенства треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"

    if math.isclose(a, b) and math.isclose(b, c):
        return "равносторонний"
    if math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
        return "равнобедренный"
    return "разносторонний"


def _calc_vertices(a: float, b: float, c: float):
    """
    Вычисляет координаты трёх вершин треугольника (int, int)
    так, чтобы он помещался в поле 100x100 px.

    Вершины:
        A — левый нижний угол,
        B — правый нижний угол,
        C — верхняя вершина.
    """
    # Помещаем сторону c (AB) горизонтально у нижнего края поля
    # Масштабируем треугольник, чтобы он вписался в поле
    max_side = max(a, b, c)
    scale = (FIELD_SIZE - 2 * MARGIN) / max_side

    a_s = a * scale
    b_s = b * scale
    c_s = c * scale

    # Координаты вершины A (левый нижний угол)
    ax = MARGIN
    ay = FIELD_SIZE - MARGIN

    # Вершина B — на расстоянии c_s по горизонтали
    bx = ax + c_s
    by = ay

    # Вершина C — пересечение окружностей радиуса b_s из A и a_s из B
    # Формулы:
    #   x = (b^2 + c^2 - a^2) / (2c)
    #   y = sqrt(b^2 - x^2)
    x_local = (b_s ** 2 + c_s ** 2 - a_s ** 2) / (2 * c_s)
    y_local_sq = b_s ** 2 - x_local ** 2
    y_local = math.sqrt(max(y_local_sq, 0.0))

    cx = ax + x_local
    cy = ay - y_local  # вверх по экрану — уменьшение Y

    # Округление и ограничение координат полем
    def _clamp(value):
        return max(0, min(FIELD_SIZE, int(round(value))))

    return [
        (_clamp(ax), _clamp(ay)),
        (_clamp(bx), _clamp(by)),
        (_clamp(cx), _clamp(cy)),
    ]


def process_triangle(side_a: str, side_b: str, side_c: str):
    """
    Основной метод.

    :param side_a: строка с длиной стороны A
    :param side_b: строка с длиной стороны B
    :param side_c: строка с длиной стороны C
    :return: (тип_треугольника: str, координаты: list[tuple[int, int]])
    """
    logger.info(
        "Запрос на обработку треугольника: A=%r, B=%r, C=%r",
        side_a, side_b, side_c,
    )

    parsed = []
    for name, raw in zip("ABC", (side_a, side_b, side_c)):
        value, error = _parse_side(raw)
        if error == "not_a_number":
            logger.warning("Сторона %s: нечисловое значение %r", name, raw)
            # Нечисловые данные → пустая строка + координаты (-2, -2)
            return "", [(-2, -2), (-2, -2), (-2, -2)]
        if error == "not_positive":
            logger.warning("Сторона %s: не положительное число %r", name, raw)
            # Ошибочные числовые данные → координаты (-1, -1)
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]
        parsed.append(value)

    a, b, c = parsed
    triangle_type = _define_triangle_type(a, b, c)

    if triangle_type == "не треугольник":
        logger.warning("Треугольник с такими сторонами не существует: %s, %s, %s", a, b, c)
        return triangle_type, [(-1, -1), (-1, -1), (-1, -1)]

    vertices = _calc_vertices(a, b, c)
    logger.info("Тип треугольника: %s, координаты: %s", triangle_type, vertices)
    return triangle_type, vertices