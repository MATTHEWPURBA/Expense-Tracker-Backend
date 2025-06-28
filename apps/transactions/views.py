from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Sum
from datetime import datetime

from .models import Transaction
from .serializers import TransactionSerializer, TransactionCreateSerializer, TransactionUpdateSerializer

# Transaction views will be implemented here

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_transaction_view(request):
    return Response({'message': 'Transactions app is working!'})

class TransactionListCreateView(generics.ListCreateAPIView):
    """
    List all transactions or create a new transaction
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter transactions by user and various parameters
        """
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by type
        type_filter = self.request.query_params.get('type', None)
        if type_filter in ['income', 'expense']:
            queryset = queryset.filter(type=type_filter)
        
        # Filter by category
        category_filter = self.request.query_params.get('category', None)
        if category_filter:
            queryset = queryset.filter(category__name=category_filter)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Search by title or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.select_related('category')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionCreateSerializer
        return TransactionSerializer

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a transaction
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related('category')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TransactionUpdateSerializer
        return TransactionSerializer

class TransactionSummaryView(generics.GenericAPIView):
    """
    Get transaction summary (totals, balance, etc.)
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get financial summary for the user
        """
        user_transactions = Transaction.objects.filter(user=request.user)
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date:
            user_transactions = user_transactions.filter(date__gte=start_date)
        if end_date:
            user_transactions = user_transactions.filter(date__lte=end_date)
        
        # Calculate totals
        income_total = user_transactions.filter(type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense_total = user_transactions.filter(type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        balance = income_total - expense_total
        
        # Get transaction counts
        total_transactions = user_transactions.count()
        income_count = user_transactions.filter(type='income').count()
        expense_count = user_transactions.filter(type='expense').count()
        
        # Recent transactions
        recent_transactions = user_transactions.order_by('-date', '-created_at')[:5]
        recent_serializer = TransactionSerializer(recent_transactions, many=True)
        
        return Response({
            'summary': {
                'total_income': float(income_total),
                'total_expenses': float(expense_total),
                'balance': float(balance),
                'total_transactions': total_transactions,
                'income_transactions': income_count,
                'expense_transactions': expense_count,
            },
            'recent_transactions': recent_serializer.data,
            'date_range': {
                'start_date': start_date,
                'end_date': end_date,
            }
        })

class TransactionByTypeView(generics.ListAPIView):
    """
    Get transactions filtered by type (income/expense)
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        type_filter = self.kwargs.get('type')
        return Transaction.objects.filter(
            user=self.request.user,
            type=type_filter
        ).select_related('category')

class TransactionByCategoryView(generics.ListAPIView):
    """
    Get transactions filtered by category
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        category_name = self.kwargs.get('category')
        return Transaction.objects.filter(
            user=self.request.user,
            category__name=category_name
        ).select_related('category')

# apps/transactions/views.py