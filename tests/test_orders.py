from customers.services.customer_service import CustomerService
from customers.storage.customer_repo import CustomerRepo
from orders.services.order_service import OrderError, OrderService
from orders.storage.order_repo import OrderRepo

import pytest


def _service():
    customers = CustomerService(CustomerRepo())
    return OrderService(OrderRepo(), customers), customers.register("Ada", "ada@example.com", "GB")


def test_lines_update_the_total():
    orders, customer = _service()
    order = orders.create(customer.id)
    order = orders.add_line(order.id, "MUG-1", 2, 1250)
    assert order.total_cents == 2500 + 495


def test_empty_order_cannot_be_placed():
    orders, customer = _service()
    order = orders.create(customer.id)
    with pytest.raises(OrderError):
        orders.place(order.id)
