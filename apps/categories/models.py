from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Category model for transactions
    """
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=10, blank=True, default='📋')  # Emoji icon
    color = models.CharField(max_length=7, default='#6B7280')  # Hex color
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ['name', 'user', 'type']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.type})"

# apps/categories/models.py