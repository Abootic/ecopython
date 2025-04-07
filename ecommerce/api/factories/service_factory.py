from api.services.interfaces.IuserService import IUserService
from api.services.implementations.userService import UserService
from api.services.interfaces.ImarketService import IMarketService
from api.services.implementations.marketService import MarketService
from api.services.interfaces.ISupplierService import ISupplierService
from api.services.implementations.SupplierService import SupplierService
from api.services.interfaces.IcustomerService import ICustomerService
from api.services.implementations.CustomerService import CustomerService
from api.services.interfaces.IproductService import IProductService
from api.services.implementations.productService import ProductService
from api.services.interfaces.IorderService import IOrderService
from api.services.implementations.orderService import OrderService
from api.services.interfaces.IPercentageService import IPercentageService
from api.services.implementations.PercentageService import PercentageService
from api.services.interfaces.ISupplierProfitService import ISupplierProfitService
from api.services.implementations.SupplierProfitService import SupplierProfitService
from api.services.interfaces.IUplaodFileService import IUplaodFileService
from api.services.implementations.UplaodFileService import UploadFileService
from api.repositories.implementations.RepositoryManager import RepositoryManager  # Correct path
from api.repositories.interfaces.IRepositoryManager import IRepositoryManager
from api.services.interfaces.IServiceManager import IServiceManager
from api.services.implementations.ServiceManager import ServiceManager

class ServiceFactory:
    def __init__(self):
        self._singleton_instances = {}
        self._repo_manager = RepositoryManager()

    def get_service(self, service_class, singleton: bool = False):
        if singleton:
            if service_class not in self._singleton_instances:
                self._singleton_instances[service_class] = service_class(self._repo_manager)
            return self._singleton_instances[service_class]
        return service_class(self._repo_manager)

    def create_user_service(self, singleton: bool = False) -> IUserService:
        return self.get_service(UserService, singleton=singleton)

    def create_market_service(self, singleton: bool = False) -> IMarketService:
        return self.get_service(MarketService, singleton=singleton)

    def create_supplier_service(self, singleton: bool = False) -> ISupplierService:
        return self.get_service(SupplierService, singleton=singleton)

    def create_customer_service(self, singleton: bool = False) -> ICustomerService:
        return self.get_service(CustomerService, singleton=singleton)

    def create_product_service(self, singleton: bool = False) -> IProductService:
        return self.get_service(ProductService, singleton=singleton)

    def create_order_service(self, singleton: bool = False) -> IOrderService:
        return self.get_service(OrderService, singleton=singleton)

    def create_percentage_service(self, singleton: bool = False) -> IPercentageService:
        return self.get_service(PercentageService, singleton=singleton)

    def create_supplier_profit_service(self, singleton: bool = False) -> ISupplierProfitService:
        return self.get_service(SupplierProfitService, singleton=singleton)

    def create_upload_file_service(self, singleton: bool = False) -> IUplaodFileService:
        return self.get_service(UploadFileService, singleton=singleton)

    def create_service_manager(self, singleton: bool = False) -> IServiceManager:
        return self.get_service(ServiceManager, singleton=singleton)

def get_service_factory() -> ServiceFactory:
    if not hasattr(get_service_factory, "_instance"):
        get_service_factory._instance = ServiceFactory()
    return get_service_factory._instance
