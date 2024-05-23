from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chart/', views.chart, name='chart'),
    path('chart/view/', views.chart_view, name='chart_view'),
    path('chart/data/', views.chart_data, name='chart_data'),
    path('fetch_currency_rates/', views.fetch_currency_rates, name='fetch_currency_rates'),
]
