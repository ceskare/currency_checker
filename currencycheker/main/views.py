from dateutil import parser as date_parser

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Currency, Country
from .parser import CurrencyRateParser, CountryParser


def index(request):
    return render(request, 'main/index.html', {"countries": Country.objects.all()})


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
    start_date = date_parser.parse(request.session.get('start_date'))
    end_date = date_parser.parse(request.session.get('end_date'))
    countries = Country.objects.filter(name__in=selected_countries)
    data = {}
    for country in countries:
        parser = CurrencyRateParser(country.currency_code)
        parser.fetch_currency_rates(start_date, end_date)
        currency = Currency.objects.filter(code=country.currency_code, date__range=(start_date, end_date)).order_by("date")
        data[country.name] = list(currency.values('date', 'rate'))

    return JsonResponse(data)

def fetch_currency_rates(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        try:
            start_date = date_parser.parse(start_date)
            end_date = date_parser.parse(end_date)
            if (end_date - start_date).days <= 0 or (end_date - start_date).days > 730:
                messages.error(request,
                               'Диапазон дат не должен превышать двух лет и дата начала периода должна быть раньше даты конца.')
                return redirect('index')
            request.session['start_date'] = str(start_date)
            request.session['end_date'] = str(end_date)
        except ValueError:
            messages.error(request, 'Неверно введена дата.')
            return redirect('index')

        CountryParser.parse_country()

        return render(request, 'main/country_list.html',
                      {"countries": Country.objects.all().order_by("name")})
    return redirect('index')
