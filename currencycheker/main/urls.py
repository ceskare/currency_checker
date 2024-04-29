from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('read_data', views.read_data)
]
