# from django.shortcuts import render, redirect
# from .models import Currency, Country
# from .parser import CurrencyRateParser
# from datetime import datetime
# from django.contrib import messages
#
#
# def index(request):
#     currency_rates = Currency.objects.all()
#     countries = Country.objects.all()
#     return render(request, 'main/index.html', {"currency_rates": currency_rates, "countries": countries})
#
# def read_data(request):
#     return render(request, 'main/chart.html')
#
#
# def fetch_currency_rates(request):
#     if request.method == 'POST':
#         try:
#             start_date = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d")
#             end_date = datetime.strptime(request.POST.get('end_date'), "%Y-%m-%d")
#         except ValueError:
#             messages.error(request, 'Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД.')
#             return redirect('index')
#         # Currency.objects.all().delete()
#         # Country.objects.all().delete()
#         for code in ["EUR", "USD", "GBP","TRY", "CNY", "INR", "JXY"]:
#             parser = CurrencyRateParser(code)
#             parser.fetch_currency_rates(start_date, end_date)
#         parser.parse_country()
#         currency_rates = Currency.objects.filter(date__range=(start_date, end_date)).order_by("date")
#         country = Country.objects.all()
#         # return render(request, 'main/index.html')
#         return render(request, 'main/index.html', {"currency_rates" : currency_rates, "countries" : country})
#     else:
#         return redirect('index')
#
# def currency_chart(request):
#     currencies = Currency.objects.all()
#     country = Country.object.all()
#
#     labels = [currency.date.strftime("%Y-%m-%d") for currency in currencies]
#     rates = [float(currency.rate) for currency in currencies]
#     codes = [currency.code for currency in currencies]
#
#     context = {
#         'labels': labels,
#         'rates': rates,
#         'codes': codes,
#     }
#     return render(request, 'main/currency_chart.html', context)

from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from .models import Currency, Country
from .parser import CurrencyRateParser
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'main/index.html', {"countries": Country.objects.all()})

# def chart(request):
#     if request.method == 'POST':
#         selected_countries = request.POST.getlist('selected_countries')
#         countries = Country.objects.filter(currency_code__in=selected_countries)
#
#         data = {}
#         for country in countries:
#             currency_data = country.get_currency_data()
#             data[country.name] = list(currency_data.values('date', 'rate'))
#
#         return JsonResponse(data)
#
#     countries = Country.objects.all()
#     return render(request, 'chart.html', {'countries': countries})

def chart(request):
    if request.method == 'POST':
        selected_countries = request.POST.getlist('selected_countries')
        request.session['selected_countries'] = selected_countries
        return redirect('chart_view')

    countries = Country.objects.all()
    return render(request, 'chart.html', {'countries': countries})

def chart_view(request):
    return render(request, 'main/chart.html')

def chart_data(request):
    selected_countries = request.session.get('selected_countries', [])
    countries = Country.objects.filter(currency_code__in=selected_countries)

    data = {}
    for country in countries:
        currency_data = country.get_currency_data()
        data[country.name] = list(currency_data.values('date', 'rate'))

    print(data)  # Временный вывод данных для проверки

    return JsonResponse(data)


def fetch_currency_rates(request):
    # Currency.objects.all().delete()
    # Country.objects.all().delete()
    if request.method == 'POST':
        try:
            start_date = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d")
            end_date = datetime.strptime(request.POST.get('end_date'), "%Y-%m-%d")
            if (end_date - start_date).days <= 0 or (end_date - start_date).days > 730:
                messages.error(request, 'Диапазон дат не должен превышать двух лет и дата начала периода должна быть раньше даты конца.')
                return redirect('index')
        except ValueError:
            messages.error(request, 'Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД.')
            return redirect('index')

        for code in ["EUR", "USD", "GBP", "TRY", "CNY", "INR", "JXY"]:
            parser = CurrencyRateParser(code)
            parser.fetch_currency_rates(start_date, end_date)
        parser.parse_country()

        currency_rates = Currency.objects.filter(date__range=(start_date, end_date)).order_by("date")
        data = {
            'currency_rates': list(currency_rates.values('code', 'rate', 'date')),
            'countries': list(Country.objects.values('name', 'currency_code'))
        }
        # selected_countries = request.POST.getlist('data')
        # request.session['data'] = json.dumps(data, cls=DjangoJSONEncoder)
        return render(request, 'main/country_list.html', {"countries": Country.objects.all(), "data": json.dumps(data, cls=DjangoJSONEncoder)})
    return redirect('index')