"""Invoices for placed orders."""
from typing import Optional

from billing.domain.invoice import Invoice, InvoiceLine
from billing.storage.invoice_repo import InvoiceRepo
from orders.domain.order import Order
from orders.services.pricing import line_total
from shared.utils.money import percent_of

VAT_PERCENT = 20


class InvoiceError(Exception):
    pass


class InvoiceService:
    def __init__(self, repo: InvoiceRepo) -> None:
        self.repo = repo

    def get(self, number: str) -> Optional[Invoice]:
        return self.repo.by_number(number)

    def invoice_order(self, order: Order) -> Invoice:
        if order.status not in ("placed", "paid"):
            raise InvoiceError("only placed or paid orders are invoiced")
        lines = []
        for line in order.lines:
            net = line_total(line)
            lines.append(InvoiceLine(line.sku, net, VAT_PERCENT, percent_of(net, VAT_PERCENT)))
        if order.shipping_cents:
            lines.append(InvoiceLine("Shipping", order.shipping_cents, VAT_PERCENT,
                                     percent_of(order.shipping_cents, VAT_PERCENT)))
        invoice = Invoice(number=self.repo.next_number(), order_id=order.id,
                          customer_id=order.customer_id, lines=lines)
        invoice.recalculate()
        return self.repo.save(invoice)
