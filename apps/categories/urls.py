from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.test_category_view, name='test'),
    # Future category URLs will be added here
    # path('list/', views.CategoryListView.as_view(), name='list'),
    # path('create/', views.CategoryCreateView.as_view(), name='create'),
    # path('<int:pk>/', views.CategoryDetailView.as_view(), name='detail'),
    # path('<int:pk>/update/', views.CategoryUpdateView.as_view(), name='update'),
    # path('<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='delete'),
    # path('defaults/', views.DefaultCategoriesView.as_view(), name='defaults'),
]

# apps/categories/urls.py