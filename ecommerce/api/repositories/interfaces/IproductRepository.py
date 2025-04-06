from abc import ABC, abstractmethod
from typing import List
from api.models.product import Product

class IProductRepository(ABC):

	@abstractmethod
	def get_by_id(self, product_id: int) -> Product:
		pass

	@abstractmethod
	def all(self) -> List[Product]:
		pass

	@abstractmethod
	def add(self, product: Product) -> Product:
		pass

	@abstractmethod
	def update(self, product: Product) -> Product:
		pass

	@abstractmethod
	def delete(self, product: Product) -> bool:
		pass
