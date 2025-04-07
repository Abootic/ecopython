from api.services.implementations.CustomerService import CustomerService
from api.services.implementations.PercentageService import PercentageService
from api.services.implementations.SupplierProfitService import SupplierProfitService
from api.services.implementations.SupplierService import SupplierService
from api.services.implementations.UplaodFileService import UploadFileService
from api.services.implementations.marketService import MarketService
from api.services.implementations.orderService import OrderService
from api.services.implementations.productService import ProductService
from api.services.interfaces.IPercentageService import IPercentageService
from api.services.interfaces.IServiceManager import IServiceManager

from api.services.implementations.userService import UserService
from api.repositories.interfaces.IRepositoryManager import IRepositoryManager
from api.services.interfaces.ISupplierProfitService import ISupplierProfitService
from api.services.interfaces.ISupplierService import ISupplierService
from api.services.interfaces.IUplaodFileService import IUplaodFileService
from api.services.interfaces.IcustomerService import ICustomerService
from api.services.interfaces.ImarketService import IMarketService
from api.services.interfaces.IorderService import IOrderService
from api.services.interfaces.IproductService import IProductService
from api.services.interfaces.IuserService import IUserService

class ServiceManager(IServiceManager):
    def __init__(self, repository_manager: IRepositoryManager):
        self.repository_manager = repository_manager
        self._customer_service = None
        self._market_service = None
        self._order_service = None
        self._percentage_service = None
        self._product_service = None
        self._supplier_profit_service = None
        self._supplier_service = None
        self._upload_file_service = None
        self._user_service = None

    def _lazy_load(self, service_name, service_class):
        if getattr(self, service_name) is None:
            service_instance = service_class(self.repository_manager)
            setattr(self, service_name, service_instance)
        return getattr(self, service_name)

    @property
    def customer_service(self) -> ICustomerService:
        return self._lazy_load('_customer_service', CustomerService)

    @property
    def market_service(self) -> IMarketService:
        return self._lazy_load('_market_service', MarketService)

    @property
    def order_service(self) -> IOrderService:
        return self._lazy_load('_order_service', OrderService)

    @property
    def percentage_service(self) -> IPercentageService:
        return self._lazy_load('_percentage_service', PercentageService)

    @property
    def product_service(self) -> IProductService:
        return self._lazy_load('_product_service', ProductService)

    @property
    def supplier_profit_service(self) -> ISupplierProfitService:
        return self._lazy_load('_supplier_profit_service', SupplierProfitService)

    @property
    def supplier_service(self) -> ISupplierService:
        return self._lazy_load('_supplier_service', SupplierService)

    @property
    def upload_file_service(self) -> IUplaodFileService:
        return self._lazy_load('_upload_file_service', UploadFileService)

    @property
    def user_service(self) -> IUserService:
        return self._lazy_load('_user_service', UserService)
