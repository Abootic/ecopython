from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # This code creates a class containing a list of fixed choices
    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        SUPPLIER = "SUPPLIER", "Supplier"

    user_type = models.CharField(
        max_length=10,
        choices=UserRole.choices,  # Using the list of choices in a clean way
        default=UserRole.CUSTOMER
    )

    REQUIRED_FIELDS = ["user_type"]
    USERNAME_FIELD = "username"

    # Modifying fields that conflict with related_name
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='api_user_set',  # Adding related_name to avoid conflicts
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_permissions_set',  # Adding related_name to avoid conflicts
        blank=True
    )

    def __str__(self):
        return self.username
