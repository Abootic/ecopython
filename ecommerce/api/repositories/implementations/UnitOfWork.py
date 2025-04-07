from django.db import transaction
from api.repositories.interfaces.IUnitOfWork import IUnitOfWork
from django.db import models

class UnitOfWork(IUnitOfWork):
    def __init__(self, context: models.Model):
        self._context = context
        self._transaction = None  # Placeholder for the transaction

    @property
    def context(self) -> models.Model:
        return self._context

    def begin_transaction(self) -> None:
        """Begin a new transaction"""
        self._transaction = transaction.atomic()

    def commit_transaction(self) -> None:
        """Commit the transaction"""
        if self._transaction:
            self._transaction.commit()

    def complete(self) -> int:
        """Complete the transaction (save changes)"""
        if self._transaction:
            self._transaction.__enter__()  # Enter the atomic block
        try:
            return self._context.save()
        finally:
            if self._transaction:
                self._transaction.__exit__(None, None, None)  # Ensure we exit the transaction

    def dispose(self) -> None:
        """Dispose of the transaction and context"""
        if self._transaction:
            self._transaction.__exit__(None, None, None)
        self._context.close()
