from django.apps import apps
from api.dto.supplierProfit_dto import SupplierProfitDTO
from api.Mapper.SupplierMapper import SupplierMapper

class SupplierProfitMapper:
    @staticmethod
    def from_model(supplier_profit):
        """
        Convert a SupplierProfit model instance to a SupplierProfitDTO.
        """
        supplier_dto = SupplierMapper.to_dto(supplier_profit.supplier)  # Use SupplierMapper to convert supplier model to DTO
        return SupplierProfitDTO(
            supplier=supplier_dto,  # Convert the supplier model to a SupplierDTO
            month=supplier_profit.month,
            profit=supplier_profit.profit
        )
    
    @staticmethod
    def to_dict(supplier_profit_dto):
        """
        Convert a SupplierProfitDTO instance to a dictionary representation.
        """
        return supplier_profit_dto.to_dict()
    
    @staticmethod
    def from_dto(supplier_profit_dto):
        """
        Convert a SupplierProfitDTO to a SupplierProfit model instance.
        """
        SupplierProfit = apps.get_model('api', 'SupplierProfit')
        return SupplierProfit(
            supplier=supplier_profit_dto.supplier.to_model(),  # Convert SupplierDTO to Supplier model
            month=supplier_profit_dto.month,
            profit=supplier_profit_dto.profit
        )