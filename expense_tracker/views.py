from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API Root endpoint that provides information about available endpoints
    """
    return Response({
        'message': 'Expense Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'authentication': '/api/auth/',
            'transactions': '/api/transactions/',
            'categories': '/api/categories/',
            'analytics': '/api/analytics/',
            'admin': '/admin/',
        },
        'documentation': 'API documentation coming soon',
        'status': 'active'
    })

def health_check(request):
    """
    Simple health check endpoint
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'Expense Tracker Backend is running'
    })

# expense_tracker/views.py