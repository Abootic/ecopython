from django.utils import timezone
from typing import List, Optional
from datetime import date
from api.models.order import Order
from api.models.product import Product
from api.models.supplier import Supplier
from api.models.supplierProfit import SupplierProfit
from api.models.percentage import Percentage
from api.repositories.interfaces.IOrderRepository import IOrderRepository
from api.repositories.implementations.GenericRepository import GenericRepository

class OrderRepository(GenericRepository[Order], IOrderRepository):

    def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        return list(self._model.objects.filter(customer_id=customer_id))

    def get_supplier_by_product(self, product: Product) -> Supplier:
        return product.supplier

    def get_or_create_supplier_profit(self, supplier: Supplier, month: date) -> SupplierProfit:
        return SupplierProfit.objects.get_or_create(
            supplier=supplier,
            month=month
        )[0]  # Return just the object, not the tuple

    def update_supplier_profit(self, supplier_profit: SupplierProfit, profit_value: float) -> SupplierProfit:
        supplier_profit.profit += profit_value
        supplier_profit.save()
        return supplier_profit

    def get_orders_by_supplier(self, supplier: Supplier) -> List[Order]:
        return list(self._model.objects.filter(product__supplier=supplier))

    def get_supplier_profit_for_month(self, supplier_id: int) -> Optional[SupplierProfit]:
        return SupplierProfit.objects.filter(
            supplier_id=supplier_id
        ).order_by('-id').first()

    def update_or_create_supplier_profit(self, supplier: Supplier, order_profit: float) -> float:
        current_month = timezone.now().date().replace(day=1)
        
        try:
            percentage = Percentage.objects.get(supplier=supplier)
            supplier_percentage = percentage.percentage_value
        except Percentage.DoesNotExist:
            supplier_percentage = 0.0

        supplier_profit, created = SupplierProfit.objects.update_or_create(
            supplier=supplier,
            month=current_month,
            defaults={'profit': order_profit}
        )

        if not created:
            supplier_profit.profit += order_profit
            supplier_profit.save()

        return supplier_profit.profit * (1 + supplier_percentage / 100)