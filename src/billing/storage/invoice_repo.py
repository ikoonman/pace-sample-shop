"""In-memory invoice storage."""
from typing import Dict, Optional

from billing.domain.invoice import Invoice


class InvoiceRepo:
    def __init__(self) -> None:
        self._rows: Dict[str, Invoice] = {}
        self._last_number = 0

    def next_number(self) -> str:
        self._last_number += 1
        return f"INV-{self._last_number:06d}"

    def save(self, invoice: Invoice) -> Invoice:
        self._rows[invoice.number] = invoice
        return invoice

    def by_number(self, number: str) -> Optional[Invoice]:
        return self._rows.get(number)
