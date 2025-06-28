from django.db import models
from django.contrib.auth.models import User
from apps.categories.models import Category

class Transaction(models.Model):
    """
    Transaction model for income and expenses
    """
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)  # For additional data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.amount} ({self.type})"
    
    @property
    def is_expense(self):
        return self.type == 'expense'
    
    @property
    def is_income(self):
        return self.type == 'income'

# apps/transactions/models.py