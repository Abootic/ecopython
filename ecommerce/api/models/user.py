from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  # This code Create Class {يحتوى على قائمه من الخيارات الثابته}
  class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    CUSTOMER = "CUSTOMER", "Customer"
    SUPPLIER = "SUPPLIER", "Supplier"

  user_type = models.CharField( 
    max_length=10,
    choices=UserRole.choices, # استخدام القائمة بشكل نظيف
    default=UserRole.CUSTOMER
  )

  REQUIRED_FIELDS = ["user_type"]
  USERNAME_FIELD = "username"

    # تعديل الحقول المتعارضة مع related_name
  groups = models.ManyToManyField(
      'auth.Group', 
      related_name='api_user_set',  # إضافة related_name لتجنب التعارض
      blank=True
  )
  
  user_permissions = models.ManyToManyField(
      'auth.Permission',
      related_name='api_user_permissions_set',  # إضافة related_name لتجنب التعارض
      blank=True
  )

  def __str__(self):
    return self.username
