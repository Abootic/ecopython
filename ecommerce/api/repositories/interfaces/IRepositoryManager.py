from abc import ABC, abstractmethod
from api.repositories.interfaces.IUserRepository import IUserRepository
from api.repositories.interfaces.ICustomerRepository import ICustomerRepository
from api.repositories.interfaces.IMarketRepository import IMarketRepository
from api.repositories.interfaces.IOrderRepository import IOrderRepository
from api.repositories.interfaces.IPercentageRepository import IPercentageRepository
from api.repositories.interfaces.IProductRepository import IProductRepository
from api.repositories.interfaces.ISupplierProfitRepository import ISupplierProfitRepository
from api.repositories.interfaces.ISupplierRepository import ISupplierRepository



class IRepositoryManager(ABC):
    @property
    @abstractmethod
    def user_repository(self) -> IUserRepository: ...

    @property
    @abstractmethod
    def customer_repository(self) -> ICustomerRepository: ...

    @property
    @abstractmethod
    def market_repository(self) -> IMarketRepository: ...

    @property
    @abstractmethod
    def order_repository(self) -> IOrderRepository: ...

    @property
    @abstractmethod
    def percentage_repository(self) -> IPercentageRepository: ...

    @property
    @abstractmethod
    def product_repository(self) -> IProductRepository: ...

    @property
    @abstractmethod
    def supplier_profit_repository(self) -> ISupplierProfitRepository: ...

    @property
    @abstractmethod
    def supplier_repository(self) -> ISupplierRepository: ...
