from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'main/index.html')

def read_data(request):
    return render(request, 'main/read_data.html')