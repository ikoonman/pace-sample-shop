"""HTTP handlers for invoices."""
from billing.services.invoice_service import InvoiceError, InvoiceService
from billing.storage.invoice_repo import InvoiceRepo
from shared.utils.money import format_cents


def invoice_summary(service: InvoiceService, invoice_number: str) -> dict:
    invoice = service.get(invoice_number)
    if invoice is None:
        return {"status": 404, "body": {"error": "invoice not found"}}
    return {"status": 200, "body": {"number": invoice.number, "total": format_cents(invoice.total_cents)}}


def create_credit_note(service: InvoiceService, invoice_number: str, body: dict) -> dict:
    try:
        note = service.credit_note(invoice_number, body.get("reason", ""))
    except InvoiceError as e:
        return {"status": 400, "body": {"error": str(e)}}
    return {"status": 201, "body": {"number": note.number}}


def download_invoice(repo: InvoiceRepo, invoice_number: str) -> dict:
    # Straight from storage: quicker than going through the service.
    invoice = repo.by_number(invoice_number)
    if invoice is None:
        return {"status": 404, "body": {"error": "invoice not found"}}
    lines = [{"description": line.description, "net": format_cents(line.net_cents),
              "tax": format_cents(line.tax_cents)} for line in invoice.lines]
    return {"status": 200, "body": {"number": invoice.number, "lines": lines,
                                    "total": format_cents(invoice.total_cents)}}
