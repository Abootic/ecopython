# api/repositories/implementations/GenericRepository.py
from typing import TypeVar, Generic, Type, List, Optional
from django.db.models import Model
from api.repositories.interfaces.IGenericRepository import IGenericRepository

T = TypeVar('T', bound=Model)

class GenericRepository(IGenericRepository[T], Generic[T]):
    def __init__(self, model: Type[T]):
        self._model = model

    def get_by_id(self, obj_id: int) -> Optional[T]:
        try:
            return self._model.objects.get(id=obj_id)
        except self._model.DoesNotExist:
            return None

    def all(self) -> List[T]:
        return list(self._model.objects.all())

    def add(self, obj: T) -> T:
        if obj.pk is None:
            obj.save()
            return obj
        raise ValueError("Object already exists. Use update to modify.")

    def update(self, obj: T) -> T:
        if obj.pk is not None:
            obj.save()
            return obj
        raise ValueError("Object does not exist. Use add to insert.")

    def delete(self, obj: T) -> bool:
        if obj:
            obj.delete()
            return True
        return False