from django.utils import timezone # type: ignore
from typing import List
from api.models.order import Order
from api.models.product import Product
from api.models.supplier import Supplier
from api.models.supplierProfit import SupplierProfit
from datetime import date
from api.models.percentage import Percentage



from api.repositories.interfaces.IorderRepository import IOrderRepository

class OrderRepository(IOrderRepository):

    def get_by_id(self, order_id: int) -> Order:
        return Order.objects.get(id=order_id)

    def all(self) -> List[Order]:
        return Order.objects.all()

    def add(self, order: Order) -> Order:
        order.save()
        return order

    def update(self, order: Order) -> Order:
        order.save()
        return order

    def delete(self, order: Order) -> Order:
        order.delete()
        return order
    def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        print("get_orders_by_customer repositoey")
        print("customer id is customer_id ")
        return Order.objects.filter(customer_id=customer_id)
    

    def get_supplier_by_product(self, product: Product) -> Supplier:
        return product.supplier

    def get_or_create_supplier_profit(self, supplier: Supplier, month: date) -> SupplierProfit:
        return SupplierProfit.objects.get_or_create(supplier=supplier, month=month)
    

    def update_supplier_profit(self, supplier_profit: SupplierProfit, profit_value: float) -> SupplierProfit:
        supplier_profit.profit += profit_value
        supplier_profit.save()
        return supplier_profit

    def get_orders_by_supplier(self, supplier: Supplier) -> List[Order]:
        return Order.objects.filter(product__supplier=supplier)
    
    

    def get_supplier_profit_for_month(self, supplier_id: int) -> float:
        try:
            # Fetch the most recent profit record for the supplier
            profit_record = SupplierProfit.objects.filter(
                supplier_id=supplier_id
            ).order_by('-id').first()  # Assuming a higher ID means the latest entry
            
            return profit_record.profit if profit_record else 0  # Return profit if found, otherwise 0
        except Exception as e:
            print(f"Error retrieving supplier profit: {str(e)}")  # Log the error
            return 0
    def update_or_create_supplier_profit(self, supplier, order_profit):
     
        current_month = timezone.now().date().replace(day=1)  # Get the first day of the current month

        # Get the percentage_value from the Percentage table for the given supplier
        try:
            percentage = Percentage.objects.get(supplier=supplier)
            supplier_percentage = percentage.percentage_value  # Get the percentage_value
        except Percentage.DoesNotExist:
            # Handle the case where no percentage is set for the supplier
            supplier_percentage = 0.0  # Default to 0% if not found, or handle it differently

        # Update or create the supplier profit record
        supplier_profit, created = SupplierProfit.objects.update_or_create(
            supplier=supplier,
            month=current_month,
            defaults={'profit': order_profit}
        )

        if not created:
            # If the record exists, add the new profit to the existing one
            supplier_profit.profit += order_profit
            supplier_profit.save()

        # Now apply the percentage to the profit (if needed)
        final_profit = supplier_profit.profit * (1 + supplier_percentage / 100)

        # Return the final_profit
        return final_profit

