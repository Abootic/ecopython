from typing import  Optional
from api.models.percentage import Percentage
from api.models.supplier import Supplier
from api.repositories.interfaces.IPercentageRepository import IPercentageRepository
from api.repositories.implementations.GenericRepository import GenericRepository

class PercentageRepository(GenericRepository[Percentage], IPercentageRepository):

    def exists_by_code(self, code: str) -> bool:
        return self._model.objects.filter(code=code).exists()

    def get_by_supplier(self, supplier_id: int) -> Optional[Percentage]:
        return self._model.objects.filter(supplier_id=supplier_id).first()

    def assign_percentage_value_to_suppliers(self, market_id: int) -> int:
        suppliers = Supplier.objects.filter(market_id=market_id).order_by('join_date')
        total_percentage = 100
        num_suppliers = len(suppliers)

        if num_suppliers == 0:
            return 3  # No suppliers to process

        percentage_entries = []
        remaining_percentage = total_percentage

        for i, supplier in enumerate(suppliers):
            multiplier = 1 + ((num_suppliers - i - 1) * 0.5)
            supplier_percentage = (total_percentage * multiplier) / (num_suppliers * 2)
            supplier_percentage = max(supplier_percentage, 0.1)
            remaining_percentage -= supplier_percentage

            supplier.percentage_value = supplier_percentage
            supplier.priority = i + 1
            supplier.save()

            existing_percentage = self._model.objects.filter(
                market_id=market_id,
                supplier_id=supplier.id
            ).first()

            if existing_percentage:
                existing_percentage.percentage_value = supplier.percentage_value
                existing_percentage.priority = supplier.priority
                existing_percentage.save()
            else:
                percentage_entries.append(
                    Percentage(
                        supplier=supplier,
                        market_id=market_id,
                        priority=supplier.priority,
                        percentage_value=supplier.percentage_value
                    )
                )

        if percentage_entries:
            self._model.objects.bulk_create(percentage_entries)

        return 2  # Successfully processed