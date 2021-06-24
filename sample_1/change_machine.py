USD_DENOMS = (
    ("Hundred Dollar Bill", 100),
    ("Fifty Dollar Bill", 50),
    ("Twenty Dollar Bill", 20),
    ("Ten Dollar Bill", 10),
    ("Five Dollar Bill", 5),
    ("Two Dollar Bill", 2),
    ("One Dollar Bill", 1),
    ("Half Dollar", 0.5),
    ("Quarter", 0.25),
    ("Dime", 0.1),
    ("Nickel", 0.05),
    ("Penny", 0.01),
)


def make_change(total: float | int = 0) -> dict:
    """
    This function takes a float or integer and returns the total amount of change in USD coins and bills.
    total: float or int
    return: dict
    """

    total = round(total, 2)

    if total <= 0:
        return {"error": "Please, enter a positive number"}

    total_sum = total * 100
    collect = ()
    for coin_bill, denom in USD_DENOMS:

        if total_sum >= denom:
            denom *= 100
            change_count = int(total_sum // denom)

            if change_count > 0:
                change = {}
                total_sum -= change_count * denom

                change["denom_name"] = coin_bill
                change["count"] = change_count
                change["denom_amount"] = denom / 100

                collect += (change,)

    return {"total": total, "change": collect}
