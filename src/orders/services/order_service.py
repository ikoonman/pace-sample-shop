"""Order use cases."""
import uuid

from customers.services.customer_service import CustomerService
from orders.domain.order import Order, OrderLine
from orders.services.pricing import price_order
from orders.storage.order_repo import OrderRepo


class OrderError(Exception):
    pass


class OrderService:
    def __init__(self, repo: OrderRepo, customers: CustomerService) -> None:
        self.repo = repo
        self.customers = customers

    def create(self, customer_id: str) -> Order:
        customer = self.customers.get(customer_id)
        order = Order(id=str(uuid.uuid4()), customer_id=customer.id, customer_region=customer.region,
                      customer_is_business=customer.is_business)
        return self.repo.save(order)

    def add_line(self, order_id: str, sku: str, quantity: int, unit_price_cents: int,
                 discount_percent: int = 0) -> Order:
        order = self._get(order_id)
        if order.status != "draft":
            raise OrderError("only draft orders can change")
        if quantity <= 0:
            raise OrderError("quantity must be positive")
        order.lines.append(OrderLine(sku, quantity, unit_price_cents, discount_percent))
        return self.repo.save(price_order(order))

    def place(self, order_id: str) -> Order:
        order = self._get(order_id)
        if not order.lines:
            raise OrderError("an order needs at least one line")
        order.status = "placed"
        return self.repo.save(order)

    def _get(self, order_id: str) -> Order:
        order = self.repo.get(order_id)
        if order is None:
            raise OrderError(f"order {order_id} not found")
        return order
