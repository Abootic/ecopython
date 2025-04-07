from datetime import datetime
from typing import List, Dict
from django.db.models import Sum
from api.models.order import Order
from api.models.percentage import Percentage
from api.models.supplierProfit import SupplierProfit
from api.repositories.interfaces.ISupplierProfitRepository import ISupplierProfitRepository
from api.repositories.implementations.GenericRepository import GenericRepository

class SupplierProfitRepository(GenericRepository[SupplierProfit], ISupplierProfitRepository):

    def get_total_profit_for_market(self, market_id: int, month: datetime) -> float:
        if isinstance(month, str):
            month = datetime.strptime(month[:7], "%Y-%m")
            
        return Order.objects.filter(
            product__supplier__market__id=market_id,
            create_at__month=month.month,
            create_at__year=month.year
        ).aggregate(total_profit=Sum('price'))['total_profit'] or 0.0

    def get_supplier_percentages(self, market_id: int) -> List[Dict]:
        return list(Percentage.objects.filter(
            supplier__market__id=market_id
        ).values('supplier_id', 'percentage_value'))

    def update_or_create_supplier_profit(self, supplier, month: datetime, profit: float) -> SupplierProfit:
        supplier_profit, created = SupplierProfit.objects.update_or_create(
            supplier=supplier,
            month=month,
            defaults={'profit': profit}
        )
        
        if not created:
            supplier_profit.profit += profit
            supplier_profit.save()
            
        return supplier_profit