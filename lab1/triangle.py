
from math import isfinite


class TriangleCalculator:
    """Класс проверки сторон и определения типа треугольника."""

    def calculate(self, side_a, side_b, side_c):
        try:
            a, b, c = float(side_a), float(side_b), float(side_c)
        except (ValueError, TypeError):
            return {
                "type": "",
                "error": "Стороны должны быть числами"
            }

        if not all(isfinite(side) for side in (a, b, c)):
            return {
                "type": "",
                "error": "Стороны должны быть конечными числами"
            }

        if a <= 0 or b <= 0 or c <= 0:
            return {
                "type": "не треугольник",
                "error": "Длины сторон должны быть положительными"
            }

        if a + b <= c or a + c <= b or b + c <= a:
            return {
                "type": "не треугольник",
                "error": "Треугольник с такими сторонами не существует"
            }

        if a == b == c:
            triangle_type = "равносторонний"
        elif a == b or a == c or b == c:
            triangle_type = "равнобедренный"
        else:
            triangle_type = "разносторонний"

        return {
            "type": triangle_type,
            "error": None
        }
