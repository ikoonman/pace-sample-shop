from orders.domain.order import Order, OrderLine
from orders.services.pricing import line_total, price_order


def test_discount_rounds_half_up():
    assert line_total(OrderLine("MUG-1", 1, 999, 15)) == 849


def test_free_shipping_from_fifty_pounds():
    order = Order(id="o1", customer_id="c1", customer_region="GB", lines=[OrderLine("LAMP-1", 1, 5000)])
    assert price_order(order).shipping_cents == 0
