from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Test endpoint
    path('', views.test_auth_view, name='test'),
    
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh'),
    
    # Profile management
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    
    # User management (admin)
    path('users/', views.UserListView.as_view(), name='user_list'),
]

# apps/authentication/urls.py