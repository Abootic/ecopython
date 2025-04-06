from django.db import models
from api.models.customer import Customer
from api.models.product import Product

class Order(models.Model):
  customer = models.ForeignKey(
    Customer,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='orders',
    verbose_name="Customer",
    help_text="The customer who placed the order."
  )
  product = models.ForeignKey(
    Product,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='orders',
    verbose_name="Product",
    help_text="The product in the order."
  )
  total_price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    verbose_name="Total Price",
    help_text="The total price of the order."
  )
  price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00,  # Provide default value for existing rows
        verbose_name="Price",
        help_text="The price of the order."
    )
  create_at = models.DateField(
      auto_now=True,
        verbose_name="Creation Date",
        help_text="The date the order was created."
    )
  quantity = models.PositiveIntegerField(
    default=0,
    verbose_name="Quantity",
    help_text="The quantity of the product in the order."
  )

  class Meta:
    verbose_name = "Order"
    verbose_name_plural = "Orders"

  def __str__(self):
    return f"Order {self.id} - {self.total_price}"
