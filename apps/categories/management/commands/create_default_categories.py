from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.categories.models import Category

class Command(BaseCommand):
    help = 'Create default categories for all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='Create categories for specific user ID',
        )

    def handle(self, *args, **options):
        # Default categories data
        default_categories = [
            # Expense categories
            {'name': 'Food & Dining', 'type': 'expense', 'icon': '🍔', 'color': '#FF6B6B'},
            {'name': 'Transportation', 'type': 'expense', 'icon': '🚗', 'color': '#4ECDC4'},
            {'name': 'Shopping', 'type': 'expense', 'icon': '🛍️', 'color': '#45B7D1'},
            {'name': 'Entertainment', 'type': 'expense', 'icon': '🎬', 'color': '#FFA07A'},
            {'name': 'Bills & Utilities', 'type': 'expense', 'icon': '📄', 'color': '#98D8C8'},
            {'name': 'Healthcare', 'type': 'expense', 'icon': '🏥', 'color': '#F7DC6F'},
            {'name': 'Education', 'type': 'expense', 'icon': '📚', 'color': '#BB8FCE'},
            {'name': 'Travel', 'type': 'expense', 'icon': '✈️', 'color': '#85C1E9'},
            
            # Income categories
            {'name': 'Salary', 'type': 'income', 'icon': '💰', 'color': '#58D68D'},
            {'name': 'Freelance', 'type': 'income', 'icon': '💻', 'color': '#5DADE2'},
            {'name': 'Investment', 'type': 'income', 'icon': '📈', 'color': '#F8C471'},
            {'name': 'Business', 'type': 'income', 'icon': '🏢', 'color': '#AF7AC5'},
            {'name': 'Gift', 'type': 'income', 'icon': '🎁', 'color': '#F1948A'},
            {'name': 'Other Income', 'type': 'income', 'icon': '💡', 'color': '#82E0AA'},
        ]

        # Determine which users to process
        if options['user_id']:
            try:
                users = [User.objects.get(id=options['user_id'])]
                self.stdout.write(f"Processing user ID: {options['user_id']}")
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"User with ID {options['user_id']} does not exist")
                )
                return
        else:
            users = User.objects.all()
            self.stdout.write(f"Processing all {users.count()} users")

        # Create categories for each user
        created_count = 0
        for user in users:
            self.stdout.write(f"Creating categories for user: {user.username}")
            
            for category_data in default_categories:
                category, created = Category.objects.get_or_create(
                    user=user,
                    name=category_data['name'],
                    type=category_data['type'],
                    defaults={
                        'icon': category_data['icon'],
                        'color': category_data['color'],
                        'description': f"Default {category_data['type']} category",
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        f"  ✓ Created: {category.name} ({category.type})"
                    )
                else:
                    self.stdout.write(
                        f"  - Exists: {category.name} ({category.type})"
                    )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} categories")
        ) 