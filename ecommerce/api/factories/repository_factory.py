from api.repositories.interfaces.IuserRepository import IUserRepository
from api.repositories.implementations.userRepository import UserRepository
from api.repositories.interfaces.ImarketRepository import IMarketRepository
from api.repositories.implementations.marketRepository import MarketRepository
from api.repositories.interfaces.IsupplierRepository import ISupplierRepository
from api.repositories.implementations.SupplierRepository import SupplierRepository
from api.repositories.interfaces.IcustomerRepository import ICustomerRepository
from api.repositories.implementations.customerRepository import CustomerRepository
from api.repositories.interfaces.IproductRepository import IProductRepository
from api.repositories.implementations.productRepository import ProductRepository
from api.repositories.interfaces.IorderRepository import IOrderRepository
from api.repositories.implementations.orderRepository import OrderRepository
from api.repositories.interfaces.IpercentageRepository import IPercentageRepository
from api.repositories.implementations.percentageRepository import PercentageRepository
from api.repositories.interfaces.ISupplierProfitRepository import ISupplierProfitRepository
from api.repositories.implementations.SupplierProfitRepository import SupplierProfitRepository


class RepositoryFactory:
    def __init__(self):
        # Dictionary to store singleton instances
        self._singleton_instances = {}

    def get_repository(self, repository_class, singleton: bool = False):
        """
        Get a repository instance. If `singleton` is True, return a singleton instance.
        """
        if singleton:
            # Check if a singleton instance already exists
            if repository_class not in self._singleton_instances:
                # Create a new instance and store it
                self._singleton_instances[repository_class] = repository_class()
            return self._singleton_instances[repository_class]
        else:
            # Return a new instance each time
            return repository_class()

    # Convenience methods for each repository
    def create_user_repository(self, singleton: bool = False) -> IUserRepository:
        return self.get_repository(UserRepository, singleton)

    def create_market_repository(self, singleton: bool = False) -> IMarketRepository:
        return self.get_repository(MarketRepository, singleton)

    def create_supplier_repository(self, singleton: bool = False) -> ISupplierRepository:
        return self.get_repository(SupplierRepository, singleton)

    def create_customer_repository(self, singleton: bool = False) -> ICustomerRepository:
        return self.get_repository(CustomerRepository, singleton)

    def create_product_repository(self, singleton: bool = False) -> IProductRepository:
        return self.get_repository(ProductRepository, singleton)

    def create_order_repository(self, singleton: bool = False) -> IOrderRepository:
        return self.get_repository(OrderRepository, singleton)

    def create_percentage_repository(self, singleton: bool = False) -> IPercentageRepository:
        return self.get_repository(PercentageRepository, singleton)

    def create_supplier_profit_repository(self, singleton: bool = False) -> ISupplierProfitRepository:
        return self.get_repository(SupplierProfitRepository, singleton)


# Singleton instance of the RepositoryFactory (avoid global variable)
def get_repository_factory() -> RepositoryFactory:
    """
    Factory function to get a singleton instance of RepositoryFactory.
    """
    if not hasattr(get_repository_factory, "_instance"):
        get_repository_factory._instance = RepositoryFactory()
    return get_repository_factory._instance


