"""Order pricing: line totals, discounts and shipping."""
from orders.domain.order import Order, OrderLine
from shared.utils.money import percent_of

FREE_SHIPPING_FROM_CENTS = 5000
SHIPPING_CENTS = 495


def line_total(line: OrderLine) -> int:
    gross = line.quantity * line.unit_price_cents
    return gross - percent_of(gross, line.discount_percent)


def isFreeShipping(subtotal_cents: int) -> bool:
    return subtotal_cents >= FREE_SHIPPING_FROM_CENTS


def shipping_for(subtotal_cents: int) -> int:
    return 0 if isFreeShipping(subtotal_cents) else SHIPPING_CENTS


def price_order(order: Order) -> Order:
    subtotal = sum(line_total(line) for line in order.lines)
    order.shipping_cents = shipping_for(subtotal) if order.lines else 0
    order.total_cents = subtotal + order.shipping_cents
    return order
