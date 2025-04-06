from django.db import models
from api.models.user import User

class Customer(models.Model):
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='customer_profile',
    verbose_name="User",
    help_text="The user associated with this customer."
  )
  phone_number = models.CharField(
    max_length=15,
    verbose_name="Phone Number",
    help_text="The phone number of the customer."
  )
  code = models.CharField(
    max_length=100,
    verbose_name="Customer Code",
    help_text="A unique code identifying the customer."
  )

  class Meta:
    verbose_name = "Customer"
    verbose_name_plural = "Customers"

  def __str__(self):
    return f"Customer {self.user.username} - {self.code}"
