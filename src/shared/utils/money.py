"""Money is held as integer cents (ADR-0002)."""


def to_cents(amount: str) -> int:
    whole, _, frac = amount.partition(".")
    return int(whole) * 100 + int((frac + "00")[:2])


def format_cents(cents: int, currency: str = "GBP") -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{currency} {cents // 100}.{cents % 100:02d}"


def percent_of(cents: int, percent: int) -> int:
    """A percentage of an amount, rounded half up to whole cents."""
    return (cents * percent + 50) // 100
