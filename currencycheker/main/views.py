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
        currency_rates = Currency.objects.filter(date__range=(start_date, end_date))
        try:  # Проверяем, что есть хотя бы один объект Currency
            # currency = Currency.objects.get(code='EUR')  # Получаем объект Currency по его коду (например, 'EUR')
            # country = currency.countries.all()  # Получаем все страны, связанные с этой валютой
            currency = Currency.objects.filter(code=name).first()
            country = Country.objects.filter(currency_code=currency)
            return render(request, 'main/index.html', {"currency_rates": currency_rates, "countries": country})
        except ValueError:
            # Обработка случая, если не найдено ни одной записи Currency
            return render(request, 'main/index.html', {"currency_rates": [], "countries": []})
        # code = Currency.objects.get(name)
        # country = Country.objects.filter(currency_code=code)
        # return render(request, 'main/index.html', {"currency_rates" : currency_rates, "countries" : country})
