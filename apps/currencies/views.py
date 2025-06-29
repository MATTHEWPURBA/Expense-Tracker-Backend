from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Currency
from .serializers import CurrencySerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def currency_list(request):
    """
    List all active currencies
    """
    try:
        # Ensure default currencies exist
        Currency.get_default_currencies()
        
        # Get all active currencies
        currencies = Currency.objects.filter(is_active=True)
        serializer = CurrencySerializer(currencies, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Currencies retrieved successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve currencies'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 