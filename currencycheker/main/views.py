from django.shortcuts import render
from .models import Currency, Country
from .parser import CurrencyRateParser
from datetime import datetime
from django.contrib import messages


def index(request):
    currency_rates = Currency.objects.all()
    return render(request, 'main/index.html', {"currency_rates" : currency_rates})

def read_data(request):
    return render(request, 'main/read_data.html')


def fetch_currency_rates(request):
    if request.method == 'POST':
        name = "EUR"
        parser = CurrencyRateParser(name)
        try:
            start_date = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d")
            end_date = datetime.strptime(request.POST.get('end_date'), "%Y-%m-%d")
        except ValueError:
            messages.error(request, 'Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД.')
            return render(request, 'main/index.html')
        parser.fetch_currency_rates(start_date, end_date)
        parser.parse_country()
        currency_rates = Currency.objects.all()
        country = Country.objects.all()
        return render(request, 'main/index.html', {"currency_rates" : currency_rates, "countries" : country})
