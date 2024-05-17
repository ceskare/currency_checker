from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('chart/', views.chart, name='chart'),
    path('fetch_currency_rates/', views.fetch_currency_rates, name='fetch_currency_rates'),
]
