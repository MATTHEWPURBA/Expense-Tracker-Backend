from django.core.management.base import BaseCommand
from apps.currencies.models import Currency

class Command(BaseCommand):
    help = 'Create default currencies in the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating default currencies...'))
        
        try:
            Currency.get_default_currencies()
            currency_count = Currency.objects.filter(is_active=True).count()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created/verified {currency_count} currencies!'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating currencies: {str(e)}')
            ) 