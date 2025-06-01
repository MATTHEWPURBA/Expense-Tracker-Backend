from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Transaction views will be implemented here

@api_view(['GET'])
def test_transaction_view(request):
    return Response({'message': 'Transactions app is working!'})

# apps/transactions/views.py