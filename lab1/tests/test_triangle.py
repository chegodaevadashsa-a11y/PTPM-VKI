import math
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

import pytest
from triangle import calculat, calculate_coordinates


def test_determine_equilateral_triangle():
    triangle_type, _ = calculat("5", "5", "5")
    assert triangle_type == "равносторонний"


def test_determine_isosceles_triangle_by_first_two_sides():
    triangle_type, _ = calculat("5", "5", "6")
    assert triangle_type == "равнобедренный"


def test_determine_isosceles_triangle_by_first_and_third_sides():
    triangle_type, _ = calculat("5", "6", "5")
    assert triangle_type == "равнобедренный"


def test_determine_isosceles_triangle_by_last_two_sides():
    triangle_type, _ = calculat("6", "5", "5")
    assert triangle_type == "равнобедренный"


def test_determine_scalene_triangle():
    triangle_type, _ = calculat("4", "5", "6")
    assert triangle_type == "разносторонний"


def test_accept_integer_side_lengths():
    triangle_type, _ = calculat("3", "4", "5")
    assert triangle_type == "разносторонний"


def test_accept_fractional_side_lengths():
    triangle_type, _ = calculat("2.5", "2.5", "2.5")
    assert triangle_type == "равносторонний"


def test_reject_non_numeric_first_side():
    triangle_type, coordinates = calculat("abc", "4", "5")
    assert triangle_type == ""
    assert coordinates == [(-2, -2)] * 3


def test_reject_non_numeric_second_side():
    triangle_type, coordinates = calculat("3", "abc", "5")
    assert triangle_type == ""
    assert coordinates == [(-2, -2)] * 3


def test_reject_non_numeric_third_side():
    triangle_type, coordinates = calculat("3", "4", "abc")
    assert triangle_type == ""
    assert coordinates == [(-2, -2)] * 3


def test_reject_empty_side():
    triangle_type, _ = calculat("", "4", "5")
    assert triangle_type == ""


def test_reject_zero_side():
    triangle_type, coordinates = calculat("0", "4", "5")
    assert triangle_type == "не треугольник"
    assert coordinates == [(-1, -1)] * 3


def test_reject_negative_side():
    triangle_type, _ = calculat("-3", "4", "5")
    assert triangle_type == "не треугольник"


def test_reject_triangle_when_sum_of_first_two_sides_is_too_small():
    triangle_type, _ = calculat("2", "3", "5")
    assert triangle_type == "не треугольник"


def test_reject_triangle_when_sum_of_first_and_third_sides_is_too_small():
    triangle_type, _ = calculat("2", "5", "3")
    assert triangle_type == "не треугольник"


def test_reject_triangle_when_sum_of_last_two_sides_is_too_small():
    triangle_type, _ = calculat("5", "2", "3")
    assert triangle_type == "не треугольник"


def test_accept_triangle_near_valid_boundary():
    triangle_type, _ = calculat("2", "3", "4.999")
    assert triangle_type == "разносторонний"


# def test_calculate_coordinates_for_three_four_five_triangle():
#     coordinates = calculate_coordinates(5, 4, 3)
#     assert len(coordinates) == 3
#     assert coordinates[0][1] == 95
#     assert coordinates[1][1] == 95



def test_calculate_coordinates_for_three_four_five_triangle():
    coordinates = calculate_coordinates(5, 4, 3)

    assert len(coordinates) == 3
    assert coordinates[0][1] == coordinates[1][1]
    assert coordinates[0] != coordinates[1]
    assert all(
        0 <= x <= 100 and 0 <= y <= 100
        for x, y in coordinates
    )





def test_all_coordinates_fit_inside_drawing_area():
    coordinates = calculate_coordinates(3, 4, 5)
    for x, y in coordinates:
        assert 0 <= x <= 100
        assert 0 <= y <= 100


def test_calculate_coordinates_for_equilateral_triangle():
    coordinates = calculate_coordinates(5, 5, 5)
    assert len(coordinates) == 3
    assert coordinates[0] != coordinates[1]
    assert coordinates[1] != coordinates[2]
    assert coordinates[0] != coordinates[2]
