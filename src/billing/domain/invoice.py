"""Invoice entity."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class InvoiceLine:
    description: str
    net_cents: int
    tax_rate_percent: int
    tax_cents: int


@dataclass
class Invoice:
    number: str
    order_id: str
    customer_id: str
    lines: List[InvoiceLine] = field(default_factory=list)
    net_cents: int = 0
    tax_cents: int = 0
    total_cents: int = 0

    def recalculate(self) -> None:
        self.net_cents = sum(line.net_cents for line in self.lines)
        self.tax_cents = sum(line.tax_cents for line in self.lines)
        self.total_cents = self.net_cents + self.tax_cents
