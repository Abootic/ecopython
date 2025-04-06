from abc import ABC, abstractmethod
from typing import List
from api.models.percentage import Percentage

class IPercentageRepository(ABC):

	@abstractmethod
	def get_by_id(self, percentage_id: int) -> Percentage:
		pass

	@abstractmethod
	def all(self) -> List[Percentage]:
		pass

	@abstractmethod
	def add(self, percentage: Percentage) -> Percentage:
		pass

	@abstractmethod
	def update(self, percentage: Percentage) -> Percentage:
		pass

	@abstractmethod
	def delete(self, percentage: Percentage) -> bool:
		pass
	@abstractmethod
	def exists_by_code(self, code: str) -> bool:
		pass
	@abstractmethod
	def get_by_supplier(self, supplier_id: int):
		pass
	@abstractmethod
	def  assign_percentage_value_to_suppliers(market_id: int):
		pass
