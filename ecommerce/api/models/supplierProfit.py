from django.db import models
from api.models.supplier import Supplier

class SupplierProfit(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    month = models.DateField(verbose_name="Month", help_text="The month for the profit")
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ('supplier', 'month')  # Ensure unique profit entry per supplier per month

    def __str__(self):
        # Using user.username instead of supplier.name
        return f"{self.supplier.user.username} Profit for {self.month}"
