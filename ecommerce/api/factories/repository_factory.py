from api.repositories.implementations.RepositoryManager import RepositoryManager  # ✅ Fixed import
from api.repositories.interfaces.IRepositoryManager import IRepositoryManager

from api.repositories.interfaces.IUserRepository import IUserRepository
from api.repositories.implementations.userRepository import UserRepository

from api.repositories.interfaces.IMarketRepository import IMarketRepository
from api.repositories.implementations.marketRepository import MarketRepository

from api.repositories.interfaces.ISupplierRepository import ISupplierRepository
from api.repositories.implementations.SupplierRepository import SupplierRepository

from api.repositories.interfaces.ICustomerRepository import ICustomerRepository
from api.repositories.implementations.customerRepository import CustomerRepository

from api.repositories.interfaces.IProductRepository import IProductRepository
from api.repositories.implementations.productRepository import ProductRepository

from api.repositories.interfaces.IOrderRepository import IOrderRepository
from api.repositories.implementations.orderRepository import OrderRepository

from api.repositories.interfaces.IPercentageRepository import IPercentageRepository
from api.repositories.implementations.percentageRepository import PercentageRepository

from api.repositories.interfaces.ISupplierProfitRepository import ISupplierProfitRepository
from api.repositories.implementations.SupplierProfitRepository import SupplierProfitRepository


class RepositoryFactory:
    def __init__(self):
        self._singleton_instances = {}

    def get_repository(self, repository_class, singleton=False):
        if singleton:
            if repository_class not in self._singleton_instances:
                self._singleton_instances[repository_class] = repository_class()
            return self._singleton_instances[repository_class]
        return repository_class()

    def create_user_repository(self, singleton=False) -> IUserRepository:
        return self.get_repository(UserRepository, singleton)

    def create_market_repository(self, singleton=False) -> IMarketRepository:
        return self.get_repository(MarketRepository, singleton)

    def create_supplier_repository(self, singleton=False) -> ISupplierRepository:
        return self.get_repository(SupplierRepository, singleton)

    def create_customer_repository(self, singleton=False) -> ICustomerRepository:
        return self.get_repository(CustomerRepository, singleton)

    def create_product_repository(self, singleton=False) -> IProductRepository:
        return self.get_repository(ProductRepository, singleton)

    def create_order_repository(self, singleton=False) -> IOrderRepository:
        return self.get_repository(OrderRepository, singleton)

    def create_percentage_repository(self, singleton=False) -> IPercentageRepository:
        return self.get_repository(PercentageRepository, singleton)

    def create_supplier_profit_repository(self, singleton=False) -> ISupplierProfitRepository:
        return self.get_repository(SupplierProfitRepository, singleton)

    def create_repository_manager(self, singleton=False) -> IRepositoryManager:
        return self.get_repository(RepositoryManager, singleton)


def get_repository_factory() -> RepositoryFactory:
    if not hasattr(get_repository_factory, "_instance"):
        get_repository_factory._instance = RepositoryFactory()
    return get_repository_factory._instance
