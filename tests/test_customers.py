from customers.services.customer_service import CustomerNotFound, CustomerService
from customers.storage.customer_repo import CustomerRepo

import pytest


def test_register_normalises_email_and_region():
    service = CustomerService(CustomerRepo())
    customer = service.register("Ada", " Ada@Example.COM ", "gb")
    assert customer.email == "ada@example.com"
    assert customer.region == "GB"
    assert not customer.is_business


def test_unknown_customer_is_an_error():
    with pytest.raises(CustomerNotFound):
        CustomerService(CustomerRepo()).get("nope")
