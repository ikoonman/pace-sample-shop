"""In-memory customer storage."""
from typing import Dict, Optional

from customers.domain.customer import Customer


class CustomerRepo:
    def __init__(self) -> None:
        self._rows: Dict[str, Customer] = {}

    def get(self, customer_id: str) -> Optional[Customer]:
        return self._rows.get(customer_id)

    def save(self, customer: Customer) -> Customer:
        self._rows[customer.id] = customer
        return customer
