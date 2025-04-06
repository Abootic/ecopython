
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

from api.factories.repository_factory import get_repository_factory


class ServiceFactory:
    def __init__(self):
        # Dictionary to store singleton instances
        self._singleton_instances = {}

    def get_service(self, service_class, *args, singleton: bool = False):
        """
        Generic method to get a service instance.
        If `singleton` is True, return a singleton instance.
        """
        if singleton:
            # Check if a singleton instance already exists
            if service_class not in self._singleton_instances:
                # Create a new instance and store it
                self._singleton_instances[service_class] = service_class(*args)
            return self._singleton_instances[service_class]
        else:
            # Return a new instance each time
            return service_class(*args)

    # Convenience methods for each service
    def create_user_service(self, singleton: bool = False) -> IUserService:
        user_repository = get_repository_factory().create_user_repository(singleton=singleton)
        return self.get_service(UserService, user_repository, singleton=singleton)

    def create_market_service(self, singleton: bool = False) -> IMarketService:
        market_repository = get_repository_factory().create_market_repository(singleton=singleton)
        return self.get_service(MarketService, market_repository, singleton=singleton)
    def create_supplier_service(self, singleton: bool = False) -> ISupplierService:
    # Create the repositories using the factory
        supplier_repository = get_repository_factory().create_supplier_repository(singleton=singleton)
        user_repository = get_repository_factory().create_user_repository(singleton=singleton)

        # If the service is a singleton, we should cache it in a singleton instance map
        if singleton:
            if SupplierService not in self._singleton_instances:
                self._singleton_instances[SupplierService] = SupplierService(supplier_repository, user_repository)
            return self._singleton_instances[SupplierService]
        
        # Otherwise, create a new instance of SupplierService
        return SupplierService(supplier_repository, user_repository)


    # Return the service instance, passing both repositories to the SupplierService constructor


    def create_customer_service(self, singleton: bool = False) -> ICustomerService:
        # Create the repositories using the factory
        customer_repository = get_repository_factory().create_customer_repository(singleton=singleton)
        user_repository = get_repository_factory().create_user_repository(singleton=singleton)

        # If the service is a singleton, we should cache it in a singleton instance map
        if singleton:
            if CustomerService not in self._singleton_instances:
                self._singleton_instances[CustomerService] = CustomerService(customer_repository, user_repository)
            return self._singleton_instances[CustomerService]
        
        # Otherwise, create a new instance of CustomerService
        return CustomerService(customer_repository, user_repository)

    def create_product_service(self, singleton: bool = False) -> IProductService:
        product_repository = get_repository_factory().create_product_repository(singleton=singleton)
        return self.get_service(ProductService, product_repository, singleton=singleton)

    def create_order_service(self, singleton: bool = False) -> IOrderService:
        order_repository = get_repository_factory().create_order_repository(singleton=singleton)
        return self.get_service(OrderService, order_repository, singleton=singleton)

    def create_percentage_service(self, singleton: bool = False) -> IPercentageService:
       
        percentage_repository = get_repository_factory().create_percentage_repository(singleton=singleton)

        # Return the service instance (singleton if requested)
        return self.get_service(PercentageService, percentage_repository, singleton=singleton)


    def create_supplier_profit_service(self, singleton: bool = False) -> ISupplierProfitService:
        supplier_profit_repository = get_repository_factory().create_supplier_profit_repository(singleton=singleton)
        return self.get_service(SupplierProfitService, supplier_profit_repository, singleton=singleton)
    
    def  create_upload_file_service(self, singleton: bool = False) -> IUplaodFileService:
        return self.get_service(UploadFileService, singleton=singleton)
    
  

    

    
    # Instead of importing at the top:
# from api.services.implementations.UplaodFileService import UplaodFileService

# Import it inside the method where it's used
  

    

   


# Singleton instance of the ServiceFactory
def get_service_factory() -> ServiceFactory:
    """
    Factory function to get a singleton instance of ServiceFactory.
    """
    if not hasattr(get_service_factory, "_instance"):
        get_service_factory._instance = ServiceFactory()
    return get_service_factory._instance


