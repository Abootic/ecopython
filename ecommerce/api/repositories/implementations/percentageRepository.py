from api.repositories.interfaces.IpercentageRepository import IPercentageRepository
from api.models.percentage import Percentage
from typing import List
from datetime import datetime
from api.models import Supplier
from api.models import Market

class PercentageRepository(IPercentageRepository):
  def __init__(self):
        self.model = Percentage  
  def get_by_id(self, Percentage_id: int) -> Percentage:
    try:
      return Percentage.objects.get(id=Percentage_id)
    except Percentage.DoesNotExist:
      return None

  def all(self) -> List[Percentage]:
    return Percentage.objects.all()

  def add(self, Percentage: Percentage) -> Percentage:
    if Percentage.pk is None:
      Percentage.save()
      return Percentage
    else:
      raise ValueError("Percentage already exists. Use update Percentage to update an existing Percentage.")

  def update(self, Percentage: Percentage) -> Percentage:
    if Percentage.pk is not None:
      Percentage.save()
      return Percentage
    else:
      raise ValueError("Percentage does not exist. Use add Percentage to add a new Percentage.")

  def delete(self, Percentage: Percentage) -> bool:
    if Percentage:
      Percentage.delete()
      return True
    return False
  def exists_by_code(self, code: str) -> bool:
        # Check if a Percentage with the given code exists
        return self.model.objects.filter(code=code).exists()
  def get_by_supplier(self, supplier_id: int):
    try:
        # Query the database for the percentage record for the given supplier
        return Percentage.objects.filter(supplier_id=supplier_id).first()
    except Exception as e:
        # Log the error or handle it as appropriate
        return None


 
  def assign_percentage_value_to_suppliers(self, market_id: int) -> int:
    # Get all suppliers for the given market, ordered by join_date (earliest first)
    suppliers = Supplier.objects.filter(market_id=market_id).order_by('join_date')

    # Total percentage to be distributed
    total_percentage = 100  # Example total percentage value

    # Calculate the number of suppliers
    num_suppliers = len(suppliers)

    if num_suppliers == 0:
        return 3  # No suppliers to process

    # We will distribute the percentage in a way that earlier suppliers get more, and no one gets 0
    percentage_entries = []
    remaining_percentage = total_percentage  # Track remaining percentage to ensure total sum equals 100

    # Assign higher percentage to earlier suppliers and avoid 0 percentage
    for i, supplier in enumerate(suppliers):
        # Calculate percentage value for this supplier, ensuring no one gets 0.0
        # The first supplier gets a larger share, and each subsequent supplier gets less
        multiplier = 1 + ((num_suppliers - i - 1) * 0.5)  # Adjust this multiplier based on your preference

        # Calculate the percentage for this supplier
        supplier_percentage = (total_percentage * multiplier) / (num_suppliers * 2)
        supplier_percentage = max(supplier_percentage, 0.1)  # Ensure no one gets 0.0%

        remaining_percentage -= supplier_percentage
        supplier.percentage_value = supplier_percentage

        # Set priority based on the order in the list (join_date order)
        supplier.priority = i + 1  # The first one to join gets priority 1, second one gets 2, etc.
        supplier.save()

        # Check if Percentage entry already exists for this supplier and market
        existing_percentage = Percentage.objects.filter(market_id=market_id, supplier_id=supplier.id).first()

        if existing_percentage:
            # Update the existing Percentage entry if found
            existing_percentage.percentage_value = supplier.percentage_value
            existing_percentage.priority = supplier.priority
            existing_percentage.save()
        else:
            # Create a new Percentage entry if not found
            percentage_entry = Percentage(
                supplier=supplier,
                market_id=market_id,
                priority=supplier.priority,
                percentage_value=supplier.percentage_value
            )
            percentage_entries.append(percentage_entry)

    # Bulk insert all percentage entries at once to minimize database hits
    if percentage_entries:
        Percentage.objects.bulk_create(percentage_entries)

    return 2  # Successfully processed and assigned percentages


