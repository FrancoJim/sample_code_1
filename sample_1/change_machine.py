from decimal import ROUND_HALF_UP, Decimal

USD_DENOMS = (
    ("Hundred Dollar Bill", Decimal("100.00")),
    ("Fifty Dollar Bill", Decimal("50.00")),
    ("Twenty Dollar Bill", Decimal("20.00")),
    ("Ten Dollar Bill", Decimal("10.00")),
    ("Five Dollar Bill", Decimal("5.00")),
    ("Two Dollar Bill", Decimal("2.00")),
    ("One Dollar Bill", Decimal("1.00")),
    ("Half Dollar", Decimal("0.50")),
    ("Quarter", Decimal("0.25")),
    ("Dime", Decimal("0.10")),
    ("Nickel", Decimal("0.05")),
    ("Penny", Decimal("0.01")),
)


def make_change(total: float | int = 0) -> dict:
    amount = Decimal(str(total)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if amount <= 0:
        return {"error": "Please enter a positive number"}

    remaining = amount
    breakdown = []

    for name, denom in USD_DENOMS:
        count = int(remaining // denom)
        if count > 0:
            remaining -= count * denom
            breakdown.append({"denom_name": name, "count": count, "denom_amount": denom})

    return {"total": amount, "change": breakdown}
