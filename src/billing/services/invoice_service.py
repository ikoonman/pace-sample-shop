"""Invoices for placed orders."""
from typing import Optional

from billing.domain.invoice import Invoice, InvoiceLine
from billing.storage.invoice_repo import InvoiceRepo
from orders.domain.order import Order
from orders.services.pricing import line_total
from shared.utils.money import percent_of

EU_REGIONS = {"DE", "FR", "NL", "IE", "ES", "IT"}
STANDARD_RATES = {"GB": 20, "DE": 19, "FR": 20, "NL": 21, "IE": 23, "ES": 21, "IT": 22}
REDUCED_RATES = {"GB": 5, "DE": 7, "FR": 5}
REDUCED_SKUS = ("BOOK-", "FOOD-")


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
            rate = self._rate_for(line.sku, order.customer_region)
            lines.append(InvoiceLine(line.sku, net, rate, percent_of(net, rate)))
        if order.shipping_cents:
            rate = STANDARD_RATES.get(order.customer_region, 0)
            lines.append(InvoiceLine("Shipping", order.shipping_cents, rate,
                                     percent_of(order.shipping_cents, rate)))
        invoice = Invoice(number=self.repo.next_number(), order_id=order.id,
                          customer_id=order.customer_id, lines=lines)
        invoice.recalculate()
        return self.repo.save(invoice)

    def _rate_for(self, sku: str, region: str) -> int:
        if sku.startswith(REDUCED_SKUS):
            if region in REDUCED_RATES:
                return REDUCED_RATES[region]
            else:
                return STANDARD_RATES.get(region, 0)
        if region in STANDARD_RATES:
            return STANDARD_RATES[region]
        if region in EU_REGIONS:
            return 20
        return 0
