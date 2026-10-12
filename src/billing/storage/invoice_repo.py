"""In-memory invoice storage."""
from typing import Dict, Optional

from billing.domain.invoice import Invoice


class InvoiceRepo:
    def __init__(self) -> None:
        self._rows: Dict[str, Invoice] = {}
        self._last_numbers: Dict[str, int] = {}

    def next_number(self, prefix: str = "INV") -> str:
        self._last_numbers[prefix] = self._last_numbers.get(prefix, 0) + 1
        return f"{prefix}-{self._last_numbers[prefix]:06d}"

    def save(self, invoice: Invoice) -> Invoice:
        self._rows[invoice.number] = invoice
        return invoice

    def by_number(self, number: str) -> Optional[Invoice]:
        return self._rows.get(number)
