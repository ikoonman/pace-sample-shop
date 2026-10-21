"""Order use cases."""
import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from billing.domain.invoice import Invoice
from billing.services.invoice_service import InvoiceService
from customers.services.customer_service import CustomerService
from orders.domain.order import Order, OrderLine
from orders.services.pricing import price_order
from orders.storage.order_repo import OrderRepo
from shared.utils.events import publish
from shared.utils.money import format_cents

log = logging.getLogger(__name__)


class OrderError(Exception):
    pass


class OrderService:
    def __init__(self, repo: OrderRepo, customers: CustomerService,
                 invoices: Optional[InvoiceService] = None) -> None:
        self.repo = repo
        self.customers = customers
        self.invoices = invoices

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
        order = self.repo.save(order)
        if self.invoices is None:
            return order
        invoice: Invoice = self.invoices.invoice_order(order)
        publish("order.placed", {"order_id": order.id, "invoice": invoice.number,
                                 "at": datetime.now(timezone.utc).isoformat()})
        log.info("order %s placed, invoiced %s", order.id, format_cents(invoice.total_cents))
        return order

    def _get(self, order_id: str) -> Order:
        order = self.repo.get(order_id)
        if order is None:
            raise OrderError(f"order {order_id} not found")
        return order
