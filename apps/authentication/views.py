from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Authentication views will be implemented here

@api_view(['GET'])
def test_auth_view(request):
    return Response({'message': 'Authentication app is working!'})

# apps/authentication/views.py