from django.db import models
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

from .models import Currency, Country
#
#
# # class ParserCountry(models.Model):
# #     name = models.CharField("Название страны", max_length=100)
# #     currency = models.CharField("Валюта", max_length=3)
# #
# #     def __str__(self):
# #         return self.name
#
# # class ParserCurrency(models.Model):
# #     code = models.CharField("Код валюты", max_length=3)
# #     country = models.ForeignKey(ParserCounry, on_delete=models.CASCADE)
# #     rate = models.DecimalField("Курс валюты", max_digits=10, decimal_places=4)
# #     start_time = models.DateField("Начало периода")
# #     end_time = models.DateField("Конец периода")
# #     date = models.DateField("Дата")
#
# class CurrencyRateParser:
#     def __init__(self):
#         self.currency_codes = ["EUR", "USD", "GBP","TRY", "CNY", "INR", "JXY"]
#         # self.code =
#
#     def fetch_currency_rates(self, start_date, end_date):
#         currency_params = {
#             "id": 10148,
#             "pv": 1,
#             "bd": start_date.day,
#             "bm": start_date.month,
#             "by": start_date.year,
#             "ed": end_date.day,
#             "em": end_date.month,
#             "ey": end_date.year,
#             "x": 48,
#             "y": 13
#         }
#
#         for currency_name in self.currency_codes:
#             if currency_name == "EUR":
#                 currency_params["cur"] = 52170
#             elif currency_name == "USD":
#                 currency_params["cur"] = 52148
#             elif currency_name == "GBP":
#                 currency_params["cur"] = 52146
#             elif currency_name == "TRY":
#                 currency_params["cur"] = 52158
#             elif currency_name == "CNY":
#                 currency_params["cur"] = 52207
#             elif currency_name == "INR":
#                 currency_params["cur"] = 52238
#             elif currency_name == "JXY":
#                 currency_params["cur"] = 52246
#             response = requests.get("https://www.finmarket.ru/currency/rates/", params=currency_params)
#
#             if response.status_code == 200:
#                 return self.parse_currency_rates(start_date, end_date, response, currency_name)
#             else:
#                 print("Ошибка при получении страницы:", response.status_code)
#                 return []
#
#     def is_date_in_range(self, user_date, start_date, end_date):
#         if (end_date - start_date) <= timedelta(days=365 * 2):
#             try:
#                 user_date = datetime.strptime(user_date[0].text.strip(), "%d.%m.%Y")
#                 return start_date <= user_date <= end_date
#             except (ValueError, IndexError):
#                 return False
#         else:
#             return False
#     def parse_currency_rates(self, start_date, end_date, response, code):
#         html_code = BeautifulSoup(response.text, 'html.parser')
#         currency_rates = []
#
#         # Находим все строки таблицы с данными о курсах валют
#         rows = html_code.find_all('tr')[1:]
#         for row in rows:
#             # Извлекаем данные из каждой строки
#             cells = row.find_all('td')
#             if self.is_date_in_range(cells, start_date, end_date):
#                 date = datetime.strptime(cells[0].text.strip(), "%d.%m.%Y").date()
#                 currency_unit = cells[1].text.strip()
#                 change = cells[3].text.strip()
#                 rate = float(cells[2].text.strip().replace(',', '.'))
#                 Currency.objects.create(code=code, country=currency_unit, rate=rate, date=date, change=change)
#                 # self.parse_country(code)
#
#         return currency_rates
#
#     def parse_country(self, code):
#         response = requests.get("https://www.iban.ru/currency-codes")
#         html_code = BeautifulSoup(response.text, 'html.parser')
#
#         table = html_code.find('tbody')
#         for row in table.find_all('tr')[1:]:
#             columns = row.find_all('td')
#             if columns[2].text == code:
#                 country_name = columns[0].text.strip()
#                 currency_code = columns[3].text.strip()
#                 Country.objects.update(name=country_name, currency_code=currency_code)

class CurrencyRateParser:
    def __init__(self, code):
        self.code = code

    def fetch_currency_rates(self, start_date, end_date):
        currency_params = {
            "id": 10148,
            "pv": 1,
            "bd": start_date.day,
            "bm": start_date.month,
            "by": start_date.year,
            "ed": end_date.day,
            "em": end_date.month,
            "ey": end_date.year,
            "x": 48,
            "y": 13
        }

        if self.code == "EUR":
            currency_params["cur"] = 52170
        elif self.code == "USD":
            currency_params["cur"] = 52148
        elif self.code == "GBP":
            currency_params["cur"] = 52146
        elif self.code == "TRY":
            currency_params["cur"] = 52158
        elif self.code == "CNY":
            currency_params["cur"] = 52207
        elif self.code == "INR":
            currency_params["cur"] = 52238
        elif self.code == "JXY":
            currency_params["cur"] = 52246
        response = requests.get("https://www.finmarket.ru/currency/rates/", params=currency_params)
        if response.status_code == 200:
            return self.parse_currency_rates(start_date, end_date, response, currency_params["cur"])
        else:
            print("Ошибка при получении страницы:", response.status_code)
            return []

    def is_date_in_range(self, user_date, start_date, end_date):
        try:
            user_date = datetime.strptime(user_date[0].text.strip(), "%d.%m.%Y")
            return start_date <= user_date <= end_date
        except (ValueError, IndexError):
            return False

    def parse_currency_rates(self, start_date, end_date, response, country):
        html_code = BeautifulSoup(response.text, 'html.parser')
        # currency_rates = []

        # Находим все строки таблицы с данными о курсах валют
        rows = html_code.find_all('tr')[1:]
        for row in rows:
            # Извлекаем данные из каждой строки
            cells = row.find_all('td')
            if self.is_date_in_range(cells, start_date, end_date):
                date = datetime.strptime(cells[0].text.strip(), "%d.%m.%Y").date()
                # currency_unit = cells[1].text.strip()
                rate = float(cells[2].text.strip().replace(',', '.'))
                change = cells[3].text.strip()
                Currency.objects.get_or_create(code=self.code, country=country, rate=rate, date=date, change=change)
        # return currency_rates

    def parse_country(self):
        response = requests.get("https://www.iban.ru/currency-codes")
        html_code = BeautifulSoup(response.text, 'html.parser')

        table = html_code.find('tbody')
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if columns[2].text in  ["EUR", "USD", "GBP", "TRY", "CNY", "INR", "JXY"]:
                country_name = columns[0].text.strip()
                currency_code = columns[1].text.strip()

                Country.objects.get_or_create(name=country_name, currency_code=currency_code)