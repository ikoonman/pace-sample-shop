"""Customer entity."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    id: str
    name: str
    email: str
    region: str  # ISO country code, e.g. "GB", "DE"
    vat_number: Optional[str] = None

    @property
    def is_business(self) -> bool:
        return bool(self.vat_number)
