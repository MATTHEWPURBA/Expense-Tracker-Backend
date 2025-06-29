from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Notification, NotificationPreference

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Notification model
    """
    list_display = [
        'title', 'user', 'type', 'priority', 'is_read', 'is_archived', 
        'created_at', 'expires_at', 'get_status'
    ]
    list_filter = [
        'type', 'priority', 'is_read', 'is_archived', 'created_at'
    ]
    search_fields = ['title', 'message', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'read_at', 'time_since_created', 'is_expired']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'message', 'type', 'priority')
        }),
        ('Status', {
            'fields': ('is_read', 'is_archived', 'read_at')
        }),
        ('Additional Data', {
            'fields': ('action_url', 'metadata', 'expires_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'time_since_created', 'is_expired'),
            'classes': ('collapse',)
        }),
    )
    
    def get_status(self, obj):
        """Get colored status indicator"""
        if obj.is_expired:
            return format_html(
                '<span style="color: #999; font-style: italic;">Expired</span>'
            )
        elif obj.is_archived:
            return format_html(
                '<span style="color: #666;">Archived</span>'
            )
        elif obj.is_read:
            return format_html(
                '<span style="color: #28a745;">Read</span>'
            )
        else:
            priority_colors = {
                'urgent': '#dc3545',
                'high': '#fd7e14',
                'medium': '#ffc107',
                'low': '#6c757d'
            }
            color = priority_colors.get(obj.priority, '#6c757d')
            return format_html(
                '<span style="color: {}; font-weight: bold;">Unread</span>',
                color
            )
    
    get_status.short_description = 'Status'
    
    actions = ['mark_as_read', 'mark_as_unread', 'archive_notifications', 'unarchive_notifications']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read"""
        updated = 0
        for notification in queryset:
            if not notification.is_read:
                notification.mark_as_read()
                updated += 1
        
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread"""
        updated = 0
        for notification in queryset:
            if notification.is_read:
                notification.mark_as_unread()
                updated += 1
        
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = "Mark selected notifications as unread"
    
    def archive_notifications(self, request, queryset):
        """Archive selected notifications"""
        updated = 0
        for notification in queryset:
            if not notification.is_archived:
                notification.archive()
                updated += 1
        
        self.message_user(request, f'{updated} notifications archived.')
    archive_notifications.short_description = "Archive selected notifications"
    
    def unarchive_notifications(self, request, queryset):
        """Unarchive selected notifications"""
        updated = 0
        for notification in queryset:
            if notification.is_archived:
                notification.unarchive()
                updated += 1
        
        self.message_user(request, f'{updated} notifications unarchived.')
    unarchive_notifications.short_description = "Unarchive selected notifications"

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    """
    Admin interface for NotificationPreference model
    """
    list_display = [
        'user', 'email_enabled', 'push_enabled', 'in_app_enabled', 
        'quiet_hours_enabled', 'created_at'
    ]
    list_filter = [
        'email_enabled', 'push_enabled', 'in_app_enabled', 'quiet_hours_enabled'
    ]
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Email Notifications', {
            'fields': (
                'email_enabled', 'email_transaction', 'email_budget', 
                'email_reminder', 'email_system', 'email_achievement', 'email_security'
            )
        }),
        ('Push Notifications', {
            'fields': (
                'push_enabled', 'push_transaction', 'push_budget', 
                'push_reminder', 'push_system', 'push_achievement', 'push_security'
            )
        }),
        ('In-App Notifications', {
            'fields': (
                'in_app_enabled', 'in_app_transaction', 'in_app_budget', 
                'in_app_reminder', 'in_app_system', 'in_app_achievement', 'in_app_security'
            )
        }),
        ('Timing Settings', {
            'fields': ('quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Custom admin site configurations
admin.site.site_header = "Expense Tracker Notifications"
admin.site.site_title = "Notifications Admin"
admin.site.index_title = "Manage Notifications and Preferences"

# apps/notifications/admin.py
