from datetime import datetime
from typing import List  # ✅ Correct way to import

from api.models.order import Order
from api.models.percentage import Percentage
from api.models.supplierProfit import SupplierProfit
from api.repositories.interfaces.ISupplierProfitRepository import ISupplierProfitRepository
from django.db.models import Sum, QuerySet  # type: ignore



class SupplierProfitRepository(ISupplierProfitRepository):
         
         def all(self) -> QuerySet[SupplierProfit, SupplierProfit]:
             return SupplierProfit.objects.all()

         def get_total_profit_for_market(self, market_id, month):
            if isinstance(month, str):
                month = month[:7]  # Keep only "YYYY-MM" if extra data exists
                month = datetime.strptime(month, "%Y-%m")  
      
            total_profit = Order.objects.filter(
                product__supplier__market__id=market_id,  # Traverse Order -> Product -> Supplier -> Market
                create_at__month=month.month,  # Filter orders by month
                create_at__year=month.year  # Filter orders by year
            ).aggregate(total_profit=Sum('price'))['total_profit'] or 0.0

            return total_profit

         def get_supplier_percentages(self, market_id):
            
                return Percentage.objects.filter(
                    supplier__market__id=market_id  # Traverse Percentage -> Supplier -> Market
                )

         def update_or_create_supplier_profit(self, supplier, month, profit):
                
                supplier_profit, created = SupplierProfit.objects.update_or_create(
                    supplier=supplier,
                    month=month,
                    defaults={'profit': profit}
                )

                if not created:
                    # If the record exists, update the profit
                    supplier_profit.profit += profit
                    supplier_profit.save()

                return supplier_profit
