from api.repositories.interfaces.IproductRepository import IProductRepository
from api.models.product import Product
from typing import List

class ProductRepository(IProductRepository):

  def get_by_id(self, product_id: int) -> Product:
    try:
      return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
      return None

  def all(self) -> List[Product]:
     return Product.objects.select_related('supplier').all() 
  def add(self, product: Product) -> Product:
    if product.pk is None:
      product.save()
      return product
    else:
      raise ValueError("Product already exists. Use update product to update an existing product.")

  def update(self, product: Product) -> Product:
    if product.pk is not None:
      product.save()
      return product
    else:
      raise ValueError("Product does not exist. Use add product to add a new product.")

  def delete(self, product: Product) -> bool:
    if product and product.pk is not None:
      product.delete()
      return True
    return False
