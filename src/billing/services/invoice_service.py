"""Invoices for placed orders."""
from typing import Optional

from billing.domain.invoice import Invoice, InvoiceLine
from billing.storage.invoice_repo import InvoiceRepo
from customers.storage.customer_repo import CustomerRepo
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
    def __init__(self, repo: InvoiceRepo, customers: Optional[CustomerRepo] = None) -> None:
        self.repo = repo
        self.customers = customers

    def get(self, number: str) -> Optional[Invoice]:
        return self.repo.by_number(number)

    def invoice_order(self, order: Order) -> Invoice:
        if order.status not in ("placed", "paid"):
            raise InvoiceError("only placed or paid orders are invoiced")
        reverse_charge = False
        customer = self.customers.get(order.customer_id) if self.customers else None
        if customer is not None and customer.vat_number and not order.customer_is_business:
            order.customer_is_business = True  # VAT number added after the order was placed
        if order.customer_is_business:
            if order.customer_region in EU_REGIONS and order.customer_region != "GB":
                reverse_charge = True
        lines = []
        for line in order.lines:
            net = line_total(line)
            rate = self._rate_for(line.sku, order.customer_region, reverse_charge)
            lines.append(InvoiceLine(line.sku, net, rate, percent_of(net, rate)))
        if order.shipping_cents:
            rate = 0 if reverse_charge else STANDARD_RATES.get(order.customer_region, 0)
            lines.append(InvoiceLine("Shipping", order.shipping_cents, rate,
                                     percent_of(order.shipping_cents, rate)))
        invoice = Invoice(number=self.repo.next_number(), order_id=order.id,
                          customer_id=order.customer_id, lines=lines, reverse_charge=reverse_charge)
        invoice.recalculate()
        return self.repo.save(invoice)

    def credit_note(self, invoice_number: str, reason: str) -> Invoice:
        original = self.repo.by_number(invoice_number)
        if original is None:
            raise InvoiceError(f"invoice {invoice_number} not found")
        if original.is_credit_note:
            raise InvoiceError("a credit note can't be credited")
        lines = [InvoiceLine(f"Credit: {line.description}", -line.net_cents, line.tax_rate_percent,
                             -line.tax_cents) for line in original.lines]
        note = Invoice(number=self.repo.next_number(prefix="CN"), order_id=original.order_id,
                       customer_id=original.customer_id, lines=lines, reverse_charge=original.reverse_charge,
                       is_credit_note=True, note=reason)
        note.recalculate()
        return self.repo.save(note)

    def _rate_for(self, sku: str, region: str, reverse_charge: bool) -> int:
        if reverse_charge:
            return 0
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
