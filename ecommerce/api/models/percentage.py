from django.db import models
from api.models.supplier import Supplier
from api.models.market import Market

class Percentage(models.Model):
  supplier = models.ForeignKey(
    Supplier,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='percentage_suppliers',
    verbose_name="Supplier",
    help_text="The supplier associated with this percentage."
  )
  market = models.ForeignKey(
    Market,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='percentage_markets',
    verbose_name="Market",
    help_text="The market associated with this percentage."
  )
  priority = models.PositiveIntegerField(
    verbose_name="Priority",
    help_text="Priority for the percentage (lower values have higher priority)."
  )
  percentage_value = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    verbose_name="Percentage Value",
    help_text="The percentage value associated with the supplier and market."
  )

  class Meta:
    unique_together = ['market', 'supplier']
    verbose_name = "Percentage"
    verbose_name_plural = "Percentages"
    ordering = ['priority']

  def __str__(self):
    return f"{self.supplier.code} - {self.percentage_value}%"
