from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Test endpoint
    path('', views.test_notification_view, name='test'),
    
    # Notification CRUD endpoints
    path('list/', views.NotificationListCreateView.as_view(), name='list_create'),
    path('create/', views.NotificationListCreateView.as_view(), name='create'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.NotificationDetailView.as_view(), name='update'),
    path('<int:pk>/delete/', views.NotificationDetailView.as_view(), name='delete'),
    
    # Notification actions
    path('<int:pk>/mark-read/', views.mark_notification_read, name='mark_read'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('bulk-action/', views.bulk_notification_action, name='bulk_action'),
    
    # Notification statistics and metadata
    path('stats/', views.NotificationStatsView.as_view(), name='stats'),
    path('types/', views.notification_types, name='types'),
    
    # Notification preferences
    path('preferences/', views.NotificationPreferenceView.as_view(), name='preferences'),
] 