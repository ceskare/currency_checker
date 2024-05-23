from datetime import datetime

import requests
from bs4 import BeautifulSoup

from .models import Currency, Country


class CurrencyRateParser:
    def __init__(self, code):
        self.code = code
        self.currency_params = {
            "EUR": 52170,
            "USD": 52148,
            "GBP": 52146,
            "TRY": 52158,
            "CNY": 52207,
            "INR": 52238,
            "JPY": 52246
        }

    def fetch_currency_rates(self, start_date, end_date):
        params = {
            "id": 10148,
            "pv": 1,
            "bd": start_date.day,
            "bm": start_date.month,
            "by": start_date.year,
            "ed": end_date.day,
            "em": end_date.month,
            "ey": end_date.year,
            "x": 48,
            "y": 13,
            "cur": self.currency_params.get(self.code)
        }

        response = requests.get("https://www.finmarket.ru/currency/rates/", params=params)
        if response.status_code == 200:
            return self.parse_currency_rates(start_date, end_date, response)
        else:
            print("Ошибка при получении страницы:", response.status_code)
            return []

    def is_date_in_range(self, user_date, start_date, end_date):
        try:
            user_date = datetime.strptime(user_date[0].text.strip(), "%d.%m.%Y")
            return start_date <= user_date <= end_date
        except (ValueError, IndexError):
            return False

    def parse_currency_rates(self, start_date, end_date, response):
        html_code = BeautifulSoup(response.text, 'html.parser')
        rows = html_code.find_all('tr')[1:]
        for row in rows:
            cells = row.find_all('td')
            if self.is_date_in_range(cells, start_date, end_date):
                date = datetime.strptime(cells[0].text.strip(), "%d.%m.%Y").date()
                rate = float(cells[2].text.strip().replace(',', '.'))
                change = cells[3].text.strip()
                Currency.objects.get_or_create(code=self.code, rate=rate, date=date, change=change)

class CountryParser:
    @staticmethod
    def parse_country():
        response = requests.get("https://www.iban.ru/currency-codes")
        html_code = BeautifulSoup(response.text, 'html.parser')
        rows = html_code.find('tbody').find_all('tr')[1:]
        currency_codes = ["EUR", "USD", "GBP", "TRY", "CNY", "INR", "JPY"]
        for row in rows:
            columns = row.find_all('td')
            country_name = columns[0].text.strip()
            currency_code = columns[2].text
            if currency_code in currency_codes:
                existing_country = Country.objects.filter(name=country_name).first()
                if existing_country is None:
                    Country.objects.get_or_create(name=country_name, currency_code=currency_code)