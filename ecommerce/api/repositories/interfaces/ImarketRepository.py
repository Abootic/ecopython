
from api.models.market import Market
from api.repositories.interfaces.IGenericRepository import IGenericRepository

class IMarketRepository(IGenericRepository[Market]):
        pass