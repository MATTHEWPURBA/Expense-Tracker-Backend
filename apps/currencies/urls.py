from django.urls import path
from . import views

app_name = 'currencies'

urlpatterns = [
    path('list/', views.currency_list, name='currency_list'),
] 