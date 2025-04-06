from datetime import date
from api.dto.Supplier_dto import SupplierDTO  # Assuming SupplierDTO exists

class SupplierProfitDTO:
    def __init__(self, supplier: SupplierDTO, month: date, profit: float):
        self.supplier = supplier
        self.month = month
        self.profit = profit

    def to_dict(self):
        """
        Convert the DTO instance to a dictionary, which is suitable for API response.
        """
        return {
            "supplier": self.supplier.to_dict() if self.supplier else None,
            "month": self.month.isoformat(),  # Convert to string format YYYY-MM-DD
            "profit": str(self.profit),  # Convert to string for proper JSON serialization
        }

    @classmethod
    def from_model(cls, model_instance):
        """
        Convert a `SupplierProfit` model instance to a `SupplierProfitDTO`.
        """
        supplier_dto = SupplierDTO.from_model(model_instance.supplier)  # Assuming SupplierDTO has a `from_model` method
        return cls(
            supplier=supplier_dto,
            month=model_instance.month,
            profit=model_instance.profit,
        )