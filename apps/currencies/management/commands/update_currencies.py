from django.core.management.base import BaseCommand
from apps.currencies.models import Currency


class Command(BaseCommand):
    help = 'Update existing currencies in the database'

    def handle(self, *args, **options):
        self.stdout.write('Updating currency data...')
        
        # Update existing currencies with correct data
        updated_currencies = [
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
        
        updated_count = 0
        created_count = 0
        
        for currency_data in updated_currencies:
            currency, created = Currency.objects.update_or_create(
                code=currency_data['code'],
                defaults={
                    'name': currency_data['name'],
                    'symbol': currency_data['symbol'],
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created currency: {currency.code} - {currency.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Updated currency: {currency.code} - {currency.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Currency update completed! Created: {created_count}, Updated: {updated_count}'
            )
        ) 