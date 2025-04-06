from django.db import models

class Market(models.Model):
  """Model representing a marketplace entity."""
  
  name = models.CharField(
    max_length=100, 
    unique=True, 
    verbose_name="Market Name",
    help_text="Enter a unique name for the market."
  )
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
  updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

  class Meta:
    ordering = ["name"]  # ترتيب تلقائي حسب الاسم
    verbose_name = "Market"
    verbose_name_plural = "Markets"

  def __str__(self):
    return self.name

