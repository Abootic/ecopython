from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class PercentageDTO:
    supplier_id: Optional[int]
    market_id: Optional[int]
    priority: int
    percentage_value: Decimal
