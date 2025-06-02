from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.test_transaction_view, name='test'),
    # Future transaction URLs will be added here
    # path('list/', views.TransactionListView.as_view(), name='list'),
    # path('create/', views.TransactionCreateView.as_view(), name='create'),
    # path('<int:pk>/', views.TransactionDetailView.as_view(), name='detail'),
    # path('<int:pk>/update/', views.TransactionUpdateView.as_view(), name='update'),
    # path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='delete'),
]

# apps/transactions/urls.py