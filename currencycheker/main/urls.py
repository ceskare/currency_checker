from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('read_data', views.read_data),
    path('fetch_currency_rates/', views.fetch_currency_rates, name='fetch_currency_rates'),
]
