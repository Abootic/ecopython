from typing import List
from api.models.product import Product
from api.repositories.interfaces.IProductRepository import IProductRepository
from api.repositories.implementations.GenericRepository import GenericRepository

class ProductRepository(GenericRepository[Product], IProductRepository):
    
    def all(self) -> List[Product]:
        """Get all products with their suppliers pre-fetched"""
        return list(self._model.objects.select_related('supplier').all())
    
    # All other methods (get_by_id, add, update, delete) are inherited from GenericRepository