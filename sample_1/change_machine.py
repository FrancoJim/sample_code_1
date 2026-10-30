from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

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

CENT = Decimal("0.01")
MAX_AMOUNT = Decimal("1000000000.00")


def parse_amount(raw: str | int | float | Decimal | None) -> Decimal | str:
    """Turn user input into a positive, cent-rounded Decimal, or return an error message.

    Strings go straight to Decimal so "1.15" never passes through float.
    """
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return "Please enter an amount"
    try:
        amount = Decimal(raw.strip() if isinstance(raw, str) else str(raw))
    except InvalidOperation:
        return "Amount must be a number"
    if not amount.is_finite():
        return "Amount must be a finite number"
    if amount > MAX_AMOUNT:
        return f"Amount must be no more than {MAX_AMOUNT:,}"
    amount = amount.quantize(CENT, rounding=ROUND_HALF_UP)
    if amount <= 0:
        return "Please enter a positive number"
    return amount


def make_change(total: str | int | float | Decimal | None = 0) -> dict:
    amount = parse_amount(total)
    if isinstance(amount, str):
        return {"error": amount}

    remaining = amount
    breakdown = []

    for name, denom in USD_DENOMS:
        count = int(remaining // denom)
        if count > 0:
            remaining -= count * denom
            breakdown.append({"denom_name": name, "count": count, "denom_amount": denom})

    return {"total": amount, "change": breakdown}
