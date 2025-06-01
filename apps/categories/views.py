from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Category views will be implemented here

@api_view(['GET'])
def test_category_view(request):
    return Response({'message': 'Categories app is working!'})

# apps/categories/views.py