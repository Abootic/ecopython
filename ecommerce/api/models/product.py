from django.db import models
from api.models.supplier import Supplier

class Product(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Supplier',
        help_text="Select the supplier for this product."
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Product Name",
        help_text="Enter the name of the product."
    )
    image = models.CharField(
        max_length=255,  # Adjusted length to allow a longer URL/file path
        verbose_name="Product Image",
        help_text="Enter the image URL or file path for the product."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price",
        help_text="Enter the price of the product."
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"  
        ordering = ['name'] 

    def __str__(self):
        return f"Product {self.name}"
