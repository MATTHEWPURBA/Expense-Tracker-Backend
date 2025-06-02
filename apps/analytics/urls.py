from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.test_analytics_view, name='test'),
    # Future analytics URLs will be added here
    # path('summary/', views.SummaryView.as_view(), name='summary'),
    # path('monthly/', views.MonthlySummaryView.as_view(), name='monthly'),
    # path('charts/', views.ChartsView.as_view(), name='charts'),
    # path('trends/', views.TrendsView.as_view(), name='trends'),
    # path('categories/', views.CategoryAnalyticsView.as_view(), name='categories'),
]

# apps/analytics/urls.py