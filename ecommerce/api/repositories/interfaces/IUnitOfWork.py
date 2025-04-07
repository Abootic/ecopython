from abc import ABC, abstractmethod
from django.db import models

class IUnitOfWork(ABC):
    @property
    @abstractmethod
    def context(self) -> models.Model: ...
    
    @abstractmethod
    def begin_transaction(self) -> None: ...

    @abstractmethod
    def commit_transaction(self) -> None: ...
    
    @abstractmethod
    def complete(self) -> int: ...

    @abstractmethod
    def dispose(self) -> None: ...
