from rest_framework import serializers
from .models import Notification, NotificationPreference

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model
    """
    time_since_created = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'type', 'priority', 'is_read', 'is_archived',
            'action_url', 'metadata', 'expires_at', 'created_at', 'updated_at',
            'read_at', 'time_since_created', 'is_expired'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'read_at']

class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating notifications
    """
    class Meta:
        model = Notification
        fields = [
            'title', 'message', 'type', 'priority', 'action_url', 
            'metadata', 'expires_at'
        ]
    
    def create(self, validated_data):
        # Set the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class NotificationUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating notification read status and other fields
    """
    class Meta:
        model = Notification
        fields = ['is_read', 'is_archived']

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for NotificationPreference model
    """
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'email_enabled', 'email_transaction', 'email_budget', 
            'email_reminder', 'email_system', 'email_achievement', 'email_security',
            'push_enabled', 'push_transaction', 'push_budget', 'push_reminder', 
            'push_system', 'push_achievement', 'push_security',
            'in_app_enabled', 'in_app_transaction', 'in_app_budget', 
            'in_app_reminder', 'in_app_system', 'in_app_achievement', 'in_app_security',
            'quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class NotificationStatsSerializer(serializers.Serializer):
    """
    Serializer for notification statistics
    """
    total_count = serializers.IntegerField()
    unread_count = serializers.IntegerField()
    read_count = serializers.IntegerField()
    archived_count = serializers.IntegerField()
    by_type = serializers.DictField()
    by_priority = serializers.DictField()
    recent_notifications = NotificationSerializer(many=True)

class BulkNotificationActionSerializer(serializers.Serializer):
    """
    Serializer for bulk notification actions
    """
    ACTION_CHOICES = [
        ('mark_read', 'Mark as Read'),
        ('mark_unread', 'Mark as Unread'),
        ('archive', 'Archive'),
        ('unarchive', 'Unarchive'),
        ('delete', 'Delete'),
    ]
    
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    action = serializers.ChoiceField(choices=ACTION_CHOICES) 