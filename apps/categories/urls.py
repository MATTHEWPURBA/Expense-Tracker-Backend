from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    # Test endpoint
    path('', views.test_category_view, name='test'),
    
    # Category CRUD endpoints
    path('list/', views.CategoryListCreateView.as_view(), name='list_create'),
    path('create/', views.CategoryListCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CategoryDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.CategoryDetailView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CategoryDetailView.as_view(), name='delete'),
    
    # Category filtering
    path('type/<str:type>/', views.CategoryByTypeView.as_view(), name='by_type'),
]

# apps/categories/urls.py