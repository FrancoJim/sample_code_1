from decimal import Decimal

from sample_1.change_machine import make_change


def _breakdown(result):
    return {item["denom_name"]: item["count"] for item in result["change"]}


def test_dollar_and_coins():
    result = make_change(1.23)
    assert result["total"] == Decimal("1.23")
    b = _breakdown(result)
    assert b["One Dollar Bill"] == 1
    assert b["Dime"] == 2
    assert b["Penny"] == 3


def test_exact_single_bill():
    result = make_change(5.00)
    assert result["total"] == Decimal("5.00")
    assert len(result["change"]) == 1
    assert _breakdown(result)["Five Dollar Bill"] == 1


def test_large_mixed_amount():
    result = make_change(187.43)
    assert result["total"] == Decimal("187.43")
    total_computed = sum(
        item["denom_amount"] * item["count"] for item in result["change"]
    )
    assert total_computed == Decimal("187.43")


def test_float_precision_trap():
    # 1.15 * 100 = 114.999... in float arithmetic — Decimal must handle this correctly
    result = make_change(1.15)
    assert "error" not in result
    total_computed = sum(
        item["denom_amount"] * item["count"] for item in result["change"]
    )
    assert total_computed == Decimal("1.15")


def test_zero_returns_error():
    result = make_change(0)
    assert "error" in result


def test_negative_returns_error():
    result = make_change(-5)
    assert "error" in result


def test_pennies_only():
    result = make_change(0.03)
    assert result["total"] == Decimal("0.03")
    assert _breakdown(result)["Penny"] == 3


def test_half_dollar():
    result = make_change(0.50)
    assert len(result["change"]) == 1
    assert _breakdown(result)["Half Dollar"] == 1


def test_two_dollar_bill():
    result = make_change(2.00)
    assert len(result["change"]) == 1
    assert _breakdown(result)["Two Dollar Bill"] == 1
