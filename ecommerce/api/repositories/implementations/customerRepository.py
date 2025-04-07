from api.repositories.interfaces.ICustomerRepository import ICustomerRepository
from api.repositories.implementations.GenericRepository import GenericRepository
from api.models.customer import Customer
from typing import Optional

class CustomerRepository(GenericRepository[Customer], ICustomerRepository):
    
    def exists_by_code(self, code: str) -> bool:
        return self._model.objects.filter(code=code).exists()
    
    def get_by_code(self, code: str) -> Optional[Customer]:
        return self._model.objects.filter(code=code).first()
    
    def get_by_userId(self, userid: str) -> Optional[Customer]:
        try:
            user_id = int(userid)
            return self._model.objects.select_related('user').filter(user_id=user_id).first()
        except ValueError:
            return None