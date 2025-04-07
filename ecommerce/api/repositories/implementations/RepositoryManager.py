from api.repositories.interfaces.IRepositoryManager import IRepositoryManager

from api.repositories.implementations.userRepository import UserRepository
from api.repositories.implementations.customerRepository import CustomerRepository
from api.repositories.implementations.marketRepository import MarketRepository
from api.repositories.implementations.orderRepository import OrderRepository
from api.repositories.implementations.percentageRepository import PercentageRepository
from api.repositories.implementations.productRepository import ProductRepository
from api.repositories.implementations.SupplierProfitRepository import SupplierProfitRepository
from api.repositories.implementations.SupplierRepository import SupplierRepository

from api.repositories.interfaces.IUserRepository import IUserRepository
from api.repositories.interfaces.ICustomerRepository import ICustomerRepository
from api.repositories.interfaces.IMarketRepository import IMarketRepository
from api.repositories.interfaces.IOrderRepository import IOrderRepository
from api.repositories.interfaces.IPercentageRepository import IPercentageRepository
from api.repositories.interfaces.IProductRepository import IProductRepository
from api.repositories.interfaces.ISupplierProfitRepository import ISupplierProfitRepository
from api.repositories.interfaces.ISupplierRepository import ISupplierRepository


class RepositoryManager(IRepositoryManager):
    def __init__(self):
        self._user_repository = None
        self._customer_repository = None
        self._market_repository = None
        self._order_repository = None
        self._percentage_repository = None
        self._product_repository = None
        self._supplier_profit_repository = None
        self._supplier_repository = None

    def _lazy_load(self, attr_name, cls):
        if getattr(self, attr_name) is None:
            setattr(self, attr_name, cls())
        return getattr(self, attr_name)

    @property
    def user_repository(self) -> IUserRepository:
        return self._lazy_load('_user_repository', UserRepository)

    @property
    def customer_repository(self) -> ICustomerRepository:
        return self._lazy_load('_customer_repository', CustomerRepository)

    @property
    def market_repository(self) -> IMarketRepository:
        return self._lazy_load('_market_repository', MarketRepository)

    @property
    def order_repository(self) -> IOrderRepository:
        return self._lazy_load('_order_repository', OrderRepository)

    @property
    def percentage_repository(self) -> IPercentageRepository:
        return self._lazy_load('_percentage_repository', PercentageRepository)

    @property
    def product_repository(self) -> IProductRepository:
        return self._lazy_load('_product_repository', ProductRepository)

    @property
    def supplier_profit_repository(self) -> ISupplierProfitRepository:
        return self._lazy_load('_supplier_profit_repository', SupplierProfitRepository)

    @property
    def supplier_repository(self) -> ISupplierRepository:
        return self._lazy_load('_supplier_repository', SupplierRepository)
