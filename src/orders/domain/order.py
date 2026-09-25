"""Order and order line entities."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class OrderLine:
    sku: str
    quantity: int
    unit_price_cents: int
    discount_percent: int = 0


@dataclass
class Order:
    id: str
    customer_id: str
    customer_region: str  # copied from the customer when the order is created (ADR-0003)
    customer_is_business: bool = False
    lines: List[OrderLine] = field(default_factory=list)
    status: str = "draft"  # draft, placed, paid, cancelled
    shipping_cents: int = 0
    total_cents: int = 0
