from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notification(models.Model):
    """
    Notification model for user notifications
    """
    TYPE_CHOICES = [
        ('transaction', 'Transaction'),
        ('budget', 'Budget'),
        ('reminder', 'Reminder'),
        ('system', 'System'),
        ('achievement', 'Achievement'),
        ('security', 'Security'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    action_url = models.URLField(blank=True, null=True)  # URL to navigate when notification is clicked
    metadata = models.JSONField(blank=True, null=True)  # Additional data
    expires_at = models.DateTimeField(blank=True, null=True)  # Optional expiration date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def mark_as_unread(self):
        """Mark notification as unread"""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save(update_fields=['is_read', 'read_at'])
    
    def archive(self):
        """Archive notification"""
        if not self.is_archived:
            self.is_archived = True
            self.save(update_fields=['is_archived'])
    
    def unarchive(self):
        """Unarchive notification"""
        if self.is_archived:
            self.is_archived = False
            self.save(update_fields=['is_archived'])
    
    @property
    def is_expired(self):
        """Check if notification is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def time_since_created(self):
        """Get human readable time since creation"""
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"

class NotificationPreference(models.Model):
    """
    User notification preferences
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email notifications
    email_enabled = models.BooleanField(default=True)
    email_transaction = models.BooleanField(default=True)
    email_budget = models.BooleanField(default=True)
    email_reminder = models.BooleanField(default=True)
    email_system = models.BooleanField(default=True)
    email_achievement = models.BooleanField(default=True)
    email_security = models.BooleanField(default=True)
    
    # Push notifications (for mobile)
    push_enabled = models.BooleanField(default=True)
    push_transaction = models.BooleanField(default=True)
    push_budget = models.BooleanField(default=True)
    push_reminder = models.BooleanField(default=True)
    push_system = models.BooleanField(default=False)
    push_achievement = models.BooleanField(default=True)
    push_security = models.BooleanField(default=True)
    
    # In-app notifications
    in_app_enabled = models.BooleanField(default=True)
    in_app_transaction = models.BooleanField(default=True)
    in_app_budget = models.BooleanField(default=True)
    in_app_reminder = models.BooleanField(default=True)
    in_app_system = models.BooleanField(default=True)
    in_app_achievement = models.BooleanField(default=True)
    in_app_security = models.BooleanField(default=True)
    
    # Timing preferences
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(default='22:00')
    quiet_hours_end = models.TimeField(default='08:00')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"{self.user.username}'s Notification Preferences"

# Signal to create default notification preferences
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_notification_preferences(sender, instance, created, **kwargs):
    """
    Automatically create NotificationPreference when a User is created
    """
    if created:
        NotificationPreference.objects.get_or_create(user=instance)

# apps/notifications/models.py
