from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')  # Entity Type

class IGenericRepository(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, obj_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def all(self) -> List[T]:
        pass

    @abstractmethod
    def add(self, obj: T) -> T:
        pass

    @abstractmethod
    def update(self, obj: T) -> T:
        pass

    @abstractmethod
    def delete(self, obj: T) -> bool:
        pass
