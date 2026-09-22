"""HTTP handlers for customers. Each takes and returns plain dicts."""
from customers.services.customer_service import CustomerNotFound, CustomerService


def create_customer(service: CustomerService, body: dict) -> dict:
    customer = service.register(body["name"], body["email"], body["region"], body.get("vat_number"))
    return {"status": 201, "body": {"id": customer.id}}


def get_customer(service: CustomerService, customer_id: str) -> dict:
    try:
        customer = service.get(customer_id)
    except CustomerNotFound:
        return {"status": 404, "body": {"error": "customer not found"}}
    return {"status": 200, "body": {"id": customer.id, "name": customer.name, "region": customer.region}}
