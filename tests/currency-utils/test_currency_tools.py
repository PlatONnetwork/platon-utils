import decimal

from hypothesis import given
from hypothesis import strategies as st
import pytest

from platon_utils.currency import MAX_VON, MIN_VON, from_von, to_von, units


@given(
    amount_in_von=st.integers(min_value=MIN_VON, max_value=MAX_VON),
    intermediate_unit=st.sampled_from(tuple(units.keys())),
)
def test_conversion_round_trip(amount_in_von, intermediate_unit):
    intermediate_amount = from_von(amount_in_von, intermediate_unit)
    result_amount = to_von(intermediate_amount, intermediate_unit)
    assert result_amount == amount_in_von


MAX_ETHER_WHOLE = 115792089237316195423570985008687907853269984665640564039457
MAX_ETHER_DECIMAL_MAX = 584007913129639935
MAX_ETHER_DECIMAL = 999999999999999999


def make_lat_string_value(amount_in_von):
    s_amount_in_von = str(amount_in_von)
    whole_part = s_amount_in_von[:-18] or "0"
    decimal_part = s_amount_in_von[-18:]

    s_amount_in_lat = "{0}.{1}".format(
        whole_part, decimal_part.zfill(18).rstrip("0")
    ).rstrip(".")
    return s_amount_in_lat


@given(st.integers(min_value=0, max_value=MAX_VON).map(make_lat_string_value))
def test_conversion_revers_round_trip_trip(amount_in_lat):
    intermediate_amount = to_von(amount_in_lat, "lat")
    result_amount = from_von(intermediate_amount, "lat")
    assert decimal.Decimal(result_amount) == decimal.Decimal(str(amount_in_lat))


@pytest.mark.parametrize(
    "value,expected",
    [
        ([1000000000000000000, "von"], "1000000000000000000"),
        ([1000000000000000000, "kvon"], "1000000000000000"),
        ([1000000000000000000, "mvon"], "1000000000000"),
        ([1000000000000000000, "gvon"], "1000000000"),
        ([1000000000000000000, "microlat"], "1000000"),
        ([1000000000000000000, "millilat"], "1000"),
        ([1000000000000000000, "lat"], "1"),
        ([1000000000000000000, "klat"], "0.001"),
        ([1000000000000000000, "klat"], "0.001"),
        ([1000000000000000000, "mlat"], "0.000001"),
        ([1000000000000000000, "glat"], "0.000000001"),
        ([1000000000000000000, "tlat"], "0.000000000001"),
    ],
)
def test_from_von(value, expected):
    assert from_von(*value) == decimal.Decimal(expected)


@pytest.mark.parametrize(
    "value,expected",
    [
        ([1, "von"], "1"),
        ([1, "kvon"], "1000"),
        ([1, "Kvon"], "1000"),
        ([1, "kvon"], "1000"),
        ([1, "mvon"], "1000000"),
        ([1, "Mvon"], "1000000"),
        ([1, "mvon"], "1000000"),
        ([1, "gvon"], "1000000000"),
        ([1, "Gvon"], "1000000000"),
        ([1, "gvon"], "1000000000"),
        ([1, "microlat"], "1000000000000"),
        ([1, "millilat"], "1000000000000000"),
        ([1, "lat"], "1000000000000000000"),
        ([1, "klat"], "1000000000000000000000"),
        ([1, "klat"], "1000000000000000000000"),
        ([1, "mlat"], "1000000000000000000000000"),
        ([1, "glat"], "1000000000000000000000000000"),
        ([1, "tlat"], "1000000000000000000000000000000"),
        ([0.05, "lat"], "50000000000000000"),
        ([1.2, "lat"], "1200000000000000000"),
    ],
)
def test_to_von(value, expected):
    assert to_von(*value) == decimal.Decimal(expected)


@pytest.mark.parametrize("value,unit", ((1, "von1"), (1, "not-a-unit"), (-1, "lat")))
def test_invalid_to_von_values(value, unit):
    with pytest.raises(ValueError):
        to_von(value, unit)

    with pytest.raises(ValueError):
        from_von(value, unit)
