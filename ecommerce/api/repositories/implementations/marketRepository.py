# api/repositories/implementations/marketRepository.py
from api.models.market import Market
from api.repositories.implementations.GenericRepository import GenericRepository
from api.repositories.interfaces.IMarketRepository import IMarketRepository

class MarketRepository(GenericRepository[Market], IMarketRepository):
    def __init__(self):
        super().__init__(Market)