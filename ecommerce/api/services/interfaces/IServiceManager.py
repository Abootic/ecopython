from abc import ABC, abstractmethod
from api.services.interfaces.IcustomerService import ICustomerService
from api.services.interfaces.ImarketService import IMarketService
from api.services.interfaces.IorderService import IOrderService
from api.services.interfaces.IPercentageService import IPercentageService
from api.services.interfaces.IproductService import IProductService
from api.services.interfaces.ISupplierProfitService import ISupplierProfitService
from api.services.interfaces.ISupplierService import ISupplierService
from api.services.interfaces.IUplaodFileService import IUplaodFileService
from api.services.interfaces.IuserService import IUserService

class IServiceManager(ABC):
    @property
    @abstractmethod
    def customer_service(self) -> ICustomerService: ...

    @property
    @abstractmethod
    def market_service(self) -> IMarketService: ...

    @property
    @abstractmethod
    def order_service(self) -> IOrderService: ...

    @property
    @abstractmethod
    def percentage_service(self) -> IPercentageService: ...

    @property
    @abstractmethod
    def product_service(self) -> IProductService: ...

    @property
    @abstractmethod
    def supplier_profit_service(self) -> ISupplierProfitService: ...

    @property
    @abstractmethod
    def supplier_service(self) -> ISupplierService: ...

    @property
    @abstractmethod
    def upload_file_service(self) -> IUplaodFileService: ...

    @property
    @abstractmethod
    def user_service(self) -> IUserService: ...
