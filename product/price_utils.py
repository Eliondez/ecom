from decimal import Decimal, ROUND_DOWN


def M(value):
    if not isinstance(value, Decimal):
        value = Decimal(value)
    return value.quantize(Decimal('.01'), rounding=ROUND_DOWN)
