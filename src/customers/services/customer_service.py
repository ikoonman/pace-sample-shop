"""Customer use cases."""
import uuid
from typing import Optional

from customers.domain.customer import Customer
from customers.storage.customer_repo import CustomerRepo


class CustomerNotFound(Exception):
    pass


class CustomerService:
    def __init__(self, repo: CustomerRepo) -> None:
        self.repo = repo

    def register(self, name: str, email: str, region: str, vat_number: Optional[str] = None) -> Customer:
        customer = Customer(
            id=str(uuid.uuid4()),
            name=name,
            email=email.strip().lower(),
            region=region.upper(),
            vat_number=vat_number,
        )
        return self.repo.save(customer)

    def get(self, customer_id: str) -> Customer:
        customer = self.repo.get(customer_id)
        if customer is None:
            raise CustomerNotFound(customer_id)
        return customer
