from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .models import Category
from .serializers import CategorySerializer, CategoryCreateSerializer

# Category views will be implemented here

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_category_view(request):
    return Response({'message': 'Categories app is working!'})

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new category
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter categories by user and type
        """
        queryset = Category.objects.filter(user=self.request.user, is_active=True)
        
        # Filter by type if provided
        type_filter = self.request.query_params.get('type', None)
        if type_filter in ['income', 'expense']:
            queryset = queryset.filter(type=type_filter)
        
        # Search by name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateSerializer
        return CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """
        Soft delete by setting is_active to False
        """
        category = self.get_object()
        
        # Check if category has associated transactions
        if category.transactions.exists():
            return Response({
                'error': 'Cannot delete category with associated transactions. Set it as inactive instead.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Hard delete if no transactions
        return super().delete(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """
        Partial update - can be used to deactivate category
        """
        return self.partial_update(request, *args, **kwargs)

class CategoryByTypeView(generics.ListAPIView):
    """
    Get categories filtered by type (income/expense)
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        type_filter = self.kwargs.get('type')
        return Category.objects.filter(
            user=self.request.user,
            type=type_filter,
            is_active=True
        )

# apps/categories/views.py