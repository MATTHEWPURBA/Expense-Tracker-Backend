from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, help_text="Currency code (e.g., USD, EUR)")
    name = models.CharField(max_length=100, help_text="Currency name (e.g., US Dollar)")
    symbol = models.CharField(max_length=10, help_text="Currency symbol (e.g., $, €)")
    is_active = models.BooleanField(default=True, help_text="Whether this currency is available for selection")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

    @classmethod
    def get_default_currencies(cls):
        """Create default currencies if they don't exist"""
        default_currencies = [
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$'},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
            {'code': 'GBP', 'name': 'British Pound', 'symbol': '£'},
            {'code': 'JPY', 'name': 'Japanese Yen', 'symbol': '¥'},
            {'code': 'CAD', 'name': 'Canadian Dollar', 'symbol': 'C$'},
            {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': 'A$'},
            {'code': 'CHF', 'name': 'Swiss Franc', 'symbol': 'CHF'},
            {'code': 'CNY', 'name': 'Chinese Yuan', 'symbol': '¥'},
            {'code': 'INR', 'name': 'Indian Rupee', 'symbol': '₹'},
            {'code': 'SGD', 'name': 'Singapore Dollar', 'symbol': 'S$'},
        ]
        
        for currency_data in default_currencies:
            cls.objects.get_or_create(
                code=currency_data['code'],
                defaults={
                    'name': currency_data['name'],
                    'symbol': currency_data['symbol'],
                }
            ) 