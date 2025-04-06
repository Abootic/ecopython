from api.repositories.interfaces.IsupplierRepository import ISupplierRepository
from api.models.supplier import Supplier
from typing import List

class SupplierRepository(ISupplierRepository):
  def __init__(self):
        self.model = Supplier  
  def get_by_id(self, supplier_id: int) -> Supplier:
    try:
      return Supplier.objects.get(id=supplier_id)
    except Supplier.DoesNotExist:
      return None

  def all(self) -> List[Supplier]:
    return Supplier.objects.all()

  def add(self, supplier: Supplier) -> Supplier:
    if supplier.pk is None:
      supplier.save()
      return supplier
    else:
      raise ValueError("supplier already exists. Use update supplier to update an existing supplier.")

  def update(self, supplier: Supplier) -> Supplier:
    if supplier.pk is not None:
      supplier.save()
      return supplier
    else:
      raise ValueError("supplier does not exist. Use add supplier to add a new supplier.")

  def delete(self, supplier: Supplier) -> bool:
    if supplier:
      supplier.delete()
      return True
    return False
  def exists_by_code(self, code: str) -> bool:
        # Check if a supplier with the given code exists
        return self.model.objects.filter(code=code).exists()
  def count_by_market_id(self, market_id: int) -> int:
        # This method returns the number of suppliers in the specified market
        return Supplier.objects.filter(market_id=market_id).count()
  def get_by_code(self, code: str) -> Supplier | None:
    return Supplier.objects.filter(code=code).first()
  def get_by_userId(self, userid: str) -> Supplier | None:
      try:
          user_id = int(userid)
      except ValueError:
          return None  # Handle invalid user_id format

      # Fetch supplier with the associated user, checking if the user is correctly populated
      supplier = Supplier.objects.select_related('user').filter(user_id=user_id).first()
      
      if supplier:
          print(f"Supplier user: {supplier.user}")  # Debug print
      else:
          print(f"No supplier found for user_id: {user_id}")  # Debug print
      
      return supplier


