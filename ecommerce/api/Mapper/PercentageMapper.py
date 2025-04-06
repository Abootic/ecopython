from typing import List
from django.apps import apps
from api.dto.percentage_dto import PercentageDTO

class PercentageMapper:
    @staticmethod
    def to_dto(percentage) -> PercentageDTO:
        return PercentageDTO(
            supplier_id=percentage.supplier.id,
            market_id=percentage.market.id,
            priority=percentage.priority,
            percentage_value=percentage.percentage_value
        )

    @staticmethod
    def to_model(dto: PercentageDTO):
        Percentage = apps.get_model('api', 'Percentage')
        return Percentage(
            supplier_id=dto.supplier_id,
            market_id=dto.market_id,
            priority=dto.priority,
            percentage_value=dto.percentage_value
        )

    @staticmethod
    def to_dto_list(percentages: List) -> List[PercentageDTO]:
        """Convert a list of Percentage models to a list of PercentageDTOs."""
        return [PercentageMapper.to_dto(p) for p in percentages]