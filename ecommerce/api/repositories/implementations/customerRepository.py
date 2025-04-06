from api.repositories.interfaces.IcustomerRepository import ICustomerRepository
from api.models.customer import Customer
from typing import List

class CustomerRepository(ICustomerRepository):
  def __init__(self):
        self.model = Customer  
  def get_by_id(self, Customer_id: int) -> Customer:
    try:
      return Customer.objects.get(id=Customer_id)
    except Customer.DoesNotExist:
      return None

  def all(self) -> List[Customer]:
    return Customer.objects.all()

  def add(self, Customer: Customer) -> Customer:
    if Customer.pk is None:
      Customer.save()
      return Customer
    else:
      raise ValueError("Customer already exists. Use update Customer to update an existing Customer.")

  def update(self, Customer: Customer) -> Customer:
    if Customer.pk is not None:
      Customer.save()
      return Customer
    else:
      raise ValueError("Customer does not exist. Use add Customer to add a new Customer.")

  def delete(self, Customer: Customer) -> bool:
    if Customer:
      Customer.delete()
      return True
    return False
  def exists_by_code(self, code: str) -> bool:
        # Check if a Customer with the given code exists
        return self.model.objects.filter(code=code).exists()
  def get_by_code(self, code: str) -> Customer | None:
    return Customer.objects.filter(code=code).first()
  def get_by_userId(self, userid: str) -> Customer | None:
      try:
          user_id = int(userid)
      except ValueError:
          return None  # Handle invalid user_id format

      # Fetch supplier with the associated user, checking if the user is correctly populated
      customer = Customer.objects.select_related('user').filter(user_id=user_id).first()
      
      if customer:
          print(f"customer user: {customer.user}")  # Debug print
      else:
          print(f"No customer found for user_id: {user_id}")  # Debug print
      
      return customer
