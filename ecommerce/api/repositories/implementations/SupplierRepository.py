from typing import Optional
from api.models.supplier import Supplier
from api.repositories.interfaces.ISupplierRepository import ISupplierRepository
from api.repositories.implementations.GenericRepository import GenericRepository

class SupplierRepository(GenericRepository[Supplier], ISupplierRepository):

    def exists_by_code(self, code: str) -> bool:
        return self._model.objects.filter(code=code).exists()

    def count_by_market_id(self, market_id: int) -> int:
        return self._model.objects.filter(market_id=market_id).count()

    def get_by_code(self, code: str) -> Optional[Supplier]:
        return self._model.objects.filter(code=code).first()

    def get_by_userId(self, userid: str) -> Optional[Supplier]:
        try:
            user_id = int(userid)
            supplier = self._model.objects.select_related('user').filter(user_id=user_id).first()
            return supplier
        except ValueError:
            return None