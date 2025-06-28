from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    # Test endpoint
    path('', views.test_transaction_view, name='test'),
    
    # Transaction CRUD endpoints
    path('list/', views.TransactionListCreateView.as_view(), name='list_create'),
    path('create/', views.TransactionListCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TransactionDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.TransactionDetailView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TransactionDetailView.as_view(), name='delete'),
    
    # Transaction analytics and filtering
    path('summary/', views.TransactionSummaryView.as_view(), name='summary'),
    path('type/<str:type>/', views.TransactionByTypeView.as_view(), name='by_type'),
    path('category/<str:category>/', views.TransactionByCategoryView.as_view(), name='by_category'),
]

# apps/transactions/urls.py