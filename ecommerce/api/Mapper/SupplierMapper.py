from django.apps import apps
from api.dto.Supplier_dto import SupplierDTO

class SupplierMapper:

    @staticmethod
    def to_model(supplier_dto: SupplierDTO):
        """Convert SupplierDTO to Supplier model."""
        Supplier = apps.get_model('api', 'Supplier')
        return Supplier(
            code=supplier_dto.code,
            market_id=supplier_dto.market_id,
            join_date=supplier_dto.join_date
            # Add other fields if necessary
        )

    @staticmethod
    def to_dto(supplier, user_dto=None) -> SupplierDTO:
        """Convert Supplier model to SupplierDTO."""
        # Ensure user_dto is only passed for serialization, not logic
        return SupplierDTO(
            id=supplier.id,
            user_id=supplier.user.id if supplier.user else None,  # Directly get user_id from the supplier's user field
            market_id=supplier.market_id,
            code=supplier.code,
            user_dto=user_dto.to_dict() if user_dto else None,  # Serialize user_dto if it's passed
            join_date=supplier.join_date
        )

    @staticmethod
    def to_dto_list(suppliers: list, user_dto=None) -> list:
        """Convert a list of Supplier models to a list of SupplierDTOs."""
        # Ensure that suppliers is a list, and map them to DTOs
        return [SupplierMapper.to_dto(supplier, user_dto) for supplier in suppliers]
