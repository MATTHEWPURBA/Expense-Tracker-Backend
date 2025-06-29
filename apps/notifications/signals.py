from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from .models import Notification, NotificationPreference
from apps.transactions.models import Transaction
from apps.authentication.models import UserProfile

@receiver(post_save, sender=Transaction)
def create_transaction_notification(sender, instance, created, **kwargs):
    """
    Create a notification when a new transaction is created
    """
    if created:
        user = instance.user
        
        # Check if user has transaction notifications enabled
        try:
            prefs = user.notification_preferences
            if not prefs.in_app_transaction:
                return
        except NotificationPreference.DoesNotExist:
            # If no preferences exist, create default and proceed
            NotificationPreference.objects.create(user=user)
        
        # Create notification for new transaction
        notification_title = f"New {instance.type.capitalize()} Added"
        notification_message = f"You've added a {instance.type} of {instance.amount} for {instance.category.name}: {instance.title}"
        
        Notification.objects.create(
            user=user,
            title=notification_title,
            message=notification_message,
            type='transaction',
            priority='low',
            metadata={
                'transaction_id': instance.id,
                'transaction_type': instance.type,
                'amount': str(instance.amount),
                'category': instance.category.name
            }
        )

@receiver(post_save, sender=UserProfile)
def check_budget_notification(sender, instance, **kwargs):
    """
    Check if user is approaching or exceeding their monthly budget
    """
    if not instance.monthly_budget:
        return
    
    user = instance.user
    
    # Check if user has budget notifications enabled
    try:
        prefs = user.notification_preferences
        if not prefs.in_app_budget:
            return
    except NotificationPreference.DoesNotExist:
        return
    
    # Calculate current month's expenses
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    monthly_expenses = Transaction.objects.filter(
        user=user,
        type='expense',
        date__gte=start_of_month.date()
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    budget = instance.monthly_budget
    percentage_used = (monthly_expenses / budget) * 100
    
    # Check if we need to send a budget notification
    # Avoid sending duplicate notifications by checking recent ones
    recent_budget_notifications = Notification.objects.filter(
        user=user,
        type='budget',
        created_at__gte=now - timedelta(days=1)
    ).exists()
    
    if not recent_budget_notifications:
        if percentage_used >= 100:
            # Budget exceeded
            Notification.objects.create(
                user=user,
                title="Budget Exceeded!",
                message=f"You've exceeded your monthly budget of {budget}. Current expenses: {monthly_expenses} ({percentage_used:.1f}%)",
                type='budget',
                priority='high',
                metadata={
                    'budget': str(budget),
                    'expenses': str(monthly_expenses),
                    'percentage': percentage_used,
                    'status': 'exceeded'
                }
            )
        elif percentage_used >= 90:
            # 90% budget warning
            Notification.objects.create(
                user=user,
                title="Budget Warning: 90% Used",
                message=f"You've used 90% of your monthly budget. Budget: {budget}, Spent: {monthly_expenses}",
                type='budget',
                priority='medium',
                metadata={
                    'budget': str(budget),
                    'expenses': str(monthly_expenses),
                    'percentage': percentage_used,
                    'status': 'warning_90'
                }
            )
        elif percentage_used >= 75:
            # 75% budget warning
            Notification.objects.create(
                user=user,
                title="Budget Alert: 75% Used",
                message=f"You've used 75% of your monthly budget. Budget: {budget}, Spent: {monthly_expenses}",
                type='budget',
                priority='low',
                metadata={
                    'budget': str(budget),
                    'expenses': str(monthly_expenses),
                    'percentage': percentage_used,
                    'status': 'alert_75'
                }
            )

@receiver(post_save, sender=User)
def create_welcome_notification(sender, instance, created, **kwargs):
    """
    Create a welcome notification for new users
    """
    if created:
        Notification.objects.create(
            user=instance,
            title="Welcome to Expense Tracker!",
            message="Welcome! Start tracking your expenses and income to better manage your finances. Add your first transaction to get started.",
            type='system',
            priority='medium',
            metadata={
                'welcome': True,
                'onboarding': True
            }
        )

@receiver(post_delete, sender=Transaction)
def create_transaction_deletion_notification(sender, instance, **kwargs):
    """
    Create a notification when a transaction is deleted
    """
    user = instance.user
    
    # Check if user has transaction notifications enabled
    try:
        prefs = user.notification_preferences
        if not prefs.in_app_transaction:
            return
    except NotificationPreference.DoesNotExist:
        return
    
    Notification.objects.create(
        user=user,
        title="Transaction Deleted",
        message=f"Transaction '{instance.title}' ({instance.type} of {instance.amount}) has been deleted.",
        type='transaction',
        priority='low',
        metadata={
            'deleted_transaction': {
                'title': instance.title,
                'type': instance.type,
                'amount': str(instance.amount),
                'category': instance.category.name if instance.category else 'Unknown'
            }
        }
    )

# Import models for signals
from django.db import models

# apps/notifications/signals.py 