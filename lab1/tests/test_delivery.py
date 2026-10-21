import os
import sys
import datetime

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

import pytest
from delivery import calculate_delivery_cost


def test_calculate_cost_for_standard_package():
    cost, _ = calculate_delivery_cost(1, 100, "обычный")
    assert cost == 700


def test_add_fragile_package_fee():
    cost, _ = calculate_delivery_cost(1, 100, "хрупкий")
    assert cost == 1000


def test_add_dangerous_package_fee():
    cost, _ = calculate_delivery_cost(1, 100, "опасный")
    assert cost == 1700


def test_apply_weight_coefficient_for_medium_package():
    cost, _ = calculate_delivery_cost(10, 100, "обычный")
    assert cost == 840


def test_apply_weight_coefficient_for_heavy_package():
    cost, _ = calculate_delivery_cost(20, 100, "обычный")
    assert cost == 1050


def test_reject_weight_below_minimum():
    result = calculate_delivery_cost(0.09, 100, "обычный")
    assert result == (-1, "0000-00-00")


def test_reject_weight_above_maximum():
    result = calculate_delivery_cost(50.1, 100, "обычный")
    assert result == (-1, "0000-00-00")


def test_reject_distance_below_minimum():
    result = calculate_delivery_cost(1, 0, "обычный")
    assert result == (-1, "0000-00-00")


def test_reject_distance_above_maximum():
    result = calculate_delivery_cost(1, 5001, "обычный")
    assert result == (-1, "0000-00-00")


def test_reject_unknown_package_type():
    result = calculate_delivery_cost(1, 100, "нестандартный")
    assert result == (-1, "0000-00-00")


def test_delivery_time_increases_after_each_500_km():
    _, date_500 = calculate_delivery_cost(1, 500, "обычный")
    _, date_501 = calculate_delivery_cost(1, 501, "обычный")

    assert date_500 == "2026-09-04"
    assert date_501 == "2026-09-05"


def test_express_delivery_takes_at_least_one_day():
    _, delivery_date = calculate_delivery_cost(
        1, 100, "обычный", is_express=True
    )

    start_date = datetime.date(2026, 9, 3)
    result_date = datetime.date.fromisoformat(delivery_date)

    assert (result_date - start_date).days >= 1
