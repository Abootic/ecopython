from abc import ABC, abstractmethod
from typing import List
from api.models.customer import Customer

class ICustomerRepository(ABC):

	@abstractmethod
	def get_by_id(self, Customer_id: int) -> Customer:
		pass

	@abstractmethod
	def all(self) -> List[Customer]:
		pass

	@abstractmethod
	def add(self, Customer: Customer) -> Customer:
		pass

	@abstractmethod
	def update(self, Customer: Customer) -> Customer:
		pass

	@abstractmethod
	def delete(self, Customer: Customer) -> bool:
		pass
	@abstractmethod
	def exists_by_code(self, code: str) -> bool:
		pass
	@abstractmethod
	def  get_by_code(self, code: str) -> Customer | None:
		pass
	@abstractmethod
	def  get_by_code(self, code: str) -> Customer | None:
		pass
	@abstractmethod
	def get_by_userId(self, userid: str) -> Customer | None:
		pass