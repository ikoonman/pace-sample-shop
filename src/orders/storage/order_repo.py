"""In-memory order storage."""
from typing import Dict, List, Optional

from orders.domain.order import Order


class OrderRepo:
    def __init__(self) -> None:
        self._rows: Dict[str, Order] = {}

    def get(self, order_id: str) -> Optional[Order]:
        return self._rows.get(order_id)

    def save(self, order: Order) -> Order:
        self._rows[order.id] = order
        return order

    def for_customer(self, customer_id: str) -> List[Order]:
        return [order for order in self._rows.values() if order.customer_id == customer_id]
