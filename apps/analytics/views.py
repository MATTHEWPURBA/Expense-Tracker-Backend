from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Analytics views will be implemented here

@api_view(['GET'])
def test_analytics_view(request):
    return Response({'message': 'Analytics app is working!'})

# apps/analytics/views.py