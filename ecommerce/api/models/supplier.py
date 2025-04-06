from django.db import models
from api.models.market import Market
from api.models.user import User

class Supplier(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="The user associated with this supplier."
    )
    market = models.ForeignKey(
        Market,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        related_name='suppliers',
        to_field='id',
        verbose_name="Market",
        help_text="The market this supplier is associated with."
    )
    join_date = models.DateTimeField(auto_now_add=True, null=True)  # Only auto_now_add=True

    code = models.CharField(
        max_length=100,
        verbose_name="Supplier Code",
        help_text="Enter a unique code for the supplier."
    )

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ['user__username']

    def __str__(self):
        return f"Supplier {self.user.username}"
