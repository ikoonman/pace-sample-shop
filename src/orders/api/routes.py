"""HTTP handlers for orders."""
from orders.services.order_service import OrderError, OrderService
from shared.utils.money import format_cents


def create_order(service: OrderService, body: dict) -> dict:
    order = service.create(body["customer_id"])
    return {"status": 201, "body": {"id": order.id}}


def add_line(service: OrderService, order_id: str, body: dict) -> dict:
    try:
        order = service.add_line(order_id, body["sku"], int(body["quantity"]), int(body["unit_price_cents"]),
                                 int(body.get("discount_percent", 0)))
    except OrderError as e:
        return {"status": 400, "body": {"error": str(e)}}
    return {"status": 200, "body": {"id": order.id, "total": format_cents(order.total_cents)}}


def place_order(service: OrderService, order_id: str) -> dict:
    try:
        order = service.place(order_id)
    except OrderError as e:
        return {"status": 400, "body": {"error": str(e)}}
    return {"status": 200, "body": {"id": order.id, "status": order.status}}
