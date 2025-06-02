from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.test_auth_view, name='test'),
    # Future authentication URLs will be added here
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('refresh/', views.RefreshTokenView.as_view(), name='refresh'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
]

# apps/authentication/urls.py