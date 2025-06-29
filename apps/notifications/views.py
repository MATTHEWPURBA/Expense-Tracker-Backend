from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from datetime import datetime, timedelta
from django.utils import timezone

from .models import Notification, NotificationPreference
from .serializers import (
    NotificationSerializer, NotificationCreateSerializer, NotificationUpdateSerializer,
    NotificationPreferenceSerializer, NotificationStatsSerializer, BulkNotificationActionSerializer
)

# Custom pagination class for notifications
class NotificationPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_notification_view(request):
    """Test endpoint for notifications app"""
    return Response({'message': 'Notifications app is working!'})

class NotificationListCreateView(generics.ListCreateAPIView):
    """
    List all notifications or create a new notification
    """
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination
    
    def get_queryset(self):
        """
        Filter notifications by user and various parameters
        """
        queryset = Notification.objects.filter(user=self.request.user)
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read', None)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Filter by archived status
        is_archived = self.request.query_params.get('is_archived', None)
        if is_archived is not None:
            queryset = queryset.filter(is_archived=is_archived.lower() == 'true')
        
        # Filter by type
        notification_type = self.request.query_params.get('type', None)
        if notification_type:
            queryset = queryset.filter(type=notification_type)
        
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Search by title or message
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(message__icontains=search)
            )
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        # Exclude expired notifications by default unless requested
        include_expired = self.request.query_params.get('include_expired', 'false')
        if include_expired.lower() != 'true':
            queryset = queryset.filter(
                Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
            )
        
        # Ordering
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering in ['created_at', '-created_at', 'title', '-title', 'priority', '-priority']:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def list(self, request, *args, **kwargs):
        """Override list to return success response format"""
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
            'message': 'Notifications retrieved successfully'
        })

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a notification
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return NotificationUpdateSerializer
        return NotificationSerializer
    
    def update(self, request, *args, **kwargs):
        """Override update to handle read status changes"""
        instance = self.get_object()
        
        # If marking as read, update read_at timestamp
        if request.data.get('is_read') and not instance.is_read:
            instance.mark_as_read()
        elif request.data.get('is_read') is False and instance.is_read:
            instance.mark_as_unread()
        
        response = super().update(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
            'message': 'Notification updated successfully'
        })

class NotificationStatsView(generics.GenericAPIView):
    """
    Get notification statistics for the user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationStatsSerializer
    
    def get(self, request):
        """
        Get comprehensive notification statistics
        """
        user_notifications = Notification.objects.filter(user=request.user)
        
        # Basic counts
        total_count = user_notifications.count()
        unread_count = user_notifications.filter(is_read=False).count()
        read_count = user_notifications.filter(is_read=True).count()
        archived_count = user_notifications.filter(is_archived=True).count()
        
        # Group by type
        by_type = {}
        type_counts = user_notifications.values('type').annotate(count=Count('id'))
        for item in type_counts:
            by_type[item['type']] = item['count']
        
        # Group by priority
        by_priority = {}
        priority_counts = user_notifications.values('priority').annotate(count=Count('id'))
        for item in priority_counts:
            by_priority[item['priority']] = item['count']
        
        # Recent notifications (last 5)
        recent_notifications = user_notifications.order_by('-created_at')[:5]
        recent_serializer = NotificationSerializer(recent_notifications, many=True, context={'request': request})
        
        stats_data = {
            'total_count': total_count,
            'unread_count': unread_count,
            'read_count': read_count,
            'archived_count': archived_count,
            'by_type': by_type,
            'by_priority': by_priority,
            'recent_notifications': recent_serializer.data,
        }
        
        return Response({
            'success': True,
            'data': stats_data,
            'message': 'Notification statistics retrieved successfully'
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, pk):
    """Mark a specific notification as read"""
    try:
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.mark_as_read()
        
        serializer = NotificationSerializer(notification, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Notification marked as read'
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Failed to mark notification as read: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    """Mark all notifications as read for the user"""
    try:
        updated_count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        
        return Response({
            'success': True,
            'data': {'updated_count': updated_count},
            'message': f'Marked {updated_count} notifications as read'
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Failed to mark all notifications as read: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_notification_action(request):
    """Perform bulk actions on notifications"""
    serializer = BulkNotificationActionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    notification_ids = serializer.validated_data['notification_ids']
    action = serializer.validated_data['action']
    
    try:
        # Get notifications belonging to the user
        notifications = Notification.objects.filter(
            id__in=notification_ids,
            user=request.user
        )
        
        if not notifications.exists():
            return Response({
                'success': False,
                'message': 'No valid notifications found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        updated_count = 0
        
        if action == 'mark_read':
            updated_count = notifications.filter(is_read=False).update(
                is_read=True, 
                read_at=timezone.now()
            )
        elif action == 'mark_unread':
            updated_count = notifications.filter(is_read=True).update(
                is_read=False, 
                read_at=None
            )
        elif action == 'archive':
            updated_count = notifications.filter(is_archived=False).update(is_archived=True)
        elif action == 'unarchive':
            updated_count = notifications.filter(is_archived=True).update(is_archived=False)
        elif action == 'delete':
            updated_count, _ = notifications.delete()
            updated_count = updated_count if isinstance(updated_count, int) else 0
        
        return Response({
            'success': True,
            'data': {'updated_count': updated_count},
            'message': f'Successfully performed {action} on {updated_count} notifications'
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Failed to perform bulk action: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

# Notification Preferences Views
class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update notification preferences
    """
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        preference, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preference
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return success response format"""
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
            'message': 'Notification preferences retrieved successfully'
        })
    
    def update(self, request, *args, **kwargs):
        """Override update to return success response format"""
        response = super().update(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
            'message': 'Notification preferences updated successfully'
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_types(request):
    """Get available notification types and priorities"""
    return Response({
        'success': True,
        'data': {
            'types': [{'value': choice[0], 'label': choice[1]} for choice in Notification.TYPE_CHOICES],
            'priorities': [{'value': choice[0], 'label': choice[1]} for choice in Notification.PRIORITY_CHOICES],
        },
        'message': 'Notification types and priorities retrieved successfully'
    })
