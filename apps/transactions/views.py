from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Sum, Count
from datetime import datetime

from .models import Transaction
from .serializers import TransactionSerializer, TransactionCreateSerializer, TransactionUpdateSerializer

# Custom pagination class for transactions
class TransactionPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

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
    pagination_class = TransactionPagination
    
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
        
        # Ordering
        ordering = self.request.query_params.get('ordering', '-date')
        if ordering in ['date', '-date', 'amount', '-amount', 'title', '-title', 'created_at', '-created_at']:
            queryset = queryset.order_by(ordering, '-created_at')
        else:
            queryset = queryset.order_by('-date', '-created_at')
        
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
        recent_serializer = TransactionSerializer(recent_transactions, many=True, context={'request': request})
        
        # Category breakdown
        category_breakdown = []
        categories = user_transactions.values('category__name', 'category__type').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        for cat in categories:
            category_breakdown.append({
                'category': cat['category__name'],
                'type': cat['category__type'],
                'total': float(cat['total'])
            })
        
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
            'category_breakdown': category_breakdown,
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
    pagination_class = TransactionPagination
    
    def get_queryset(self):
        type_filter = self.kwargs.get('type')
        queryset = Transaction.objects.filter(
            user=self.request.user,
            type=type_filter
        ).select_related('category')
        
        # Apply ordering
        ordering = self.request.query_params.get('ordering', '-date')
        if ordering in ['date', '-date', 'amount', '-amount', 'title', '-title']:
            queryset = queryset.order_by(ordering, '-created_at')
        else:
            queryset = queryset.order_by('-date', '-created_at')
            
        return queryset

class TransactionByCategoryView(generics.ListAPIView):
    """
    Get transactions filtered by category
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TransactionPagination
    
    def get_queryset(self):
        category_name = self.kwargs.get('category')
        queryset = Transaction.objects.filter(
            user=self.request.user,
            category__name=category_name
        ).select_related('category')
        
        # Apply ordering
        ordering = self.request.query_params.get('ordering', '-date')
        if ordering in ['date', '-date', 'amount', '-amount', 'title', '-title']:
            queryset = queryset.order_by(ordering, '-created_at')
        else:
            queryset = queryset.order_by('-date', '-created_at')
            
        return queryset

# Additional views for better API functionality

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_stats_view(request):
    """
    Get transaction statistics for charts and analytics
    """
    user_transactions = Transaction.objects.filter(user=request.user)
    
    # Monthly breakdown for the last 12 months
    from django.db.models import TruncMonth
    from datetime import datetime, timedelta
    
    twelve_months_ago = datetime.now().date().replace(day=1) - timedelta(days=365)
    
    monthly_data = user_transactions.filter(
        date__gte=twelve_months_ago
    ).annotate(
        month=TruncMonth('date')
    ).values('month', 'type').annotate(
        total=Sum('amount')
    ).order_by('month', 'type')
    
    # Category breakdown
    category_data = user_transactions.values(
        'category__name', 'type'
    ).annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    return Response({
        'monthly_breakdown': list(monthly_data),
        'category_breakdown': list(category_data),
        'total_income': float(user_transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0),
        'total_expenses': float(user_transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0),
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_delete_transactions(request):
    """
    Delete multiple transactions at once
    """
    transaction_ids = request.data.get('transaction_ids', [])
    
    if not transaction_ids:
        return Response({'error': 'No transaction IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    deleted_count = Transaction.objects.filter(
        id__in=transaction_ids,
        user=request.user
    ).delete()[0]
    
    return Response({
        'message': f'{deleted_count} transactions deleted successfully',
        'deleted_count': deleted_count
    })

# apps/transactions/views.py