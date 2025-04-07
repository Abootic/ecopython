
from api.models.product import Product
from api.repositories.interfaces.IGenericRepository import IGenericRepository

class IProductRepository(IGenericRepository[Product]):
    # No additional methods needed unless you have product-specific operations
    pass