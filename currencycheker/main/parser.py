# from datetime import datetime
# from models import Currency
# # from django.db import models
# import requests
# from bs4 import BeautifulSoup
#
#
# class CurrencyRateParser:
#     def __init__(self, code):
#         self.code = code
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
#         if self.code == "EUR":
#             currency_params["cur"] = 52170
#         elif self.code == "USD":
#             currency_params["cur"] = 52148
#         elif self.code == "GBP":
#             currency_params["cur"] = 52146
#         elif self.code == "TRY":
#             currency_params["cur"] = 52158
#         elif self.code == "CNY":
#             currency_params["cur"] = 52207
#         elif self.code == "INR":
#             currency_params["cur"] = 52238
#         elif self.code == "JXY":
#             currency_params["cur"] = 52246
#         response = requests.get("https://www.finmarket.ru/currency/rates/", params=currency_params)
#         if response.status_code == 200:
#             self.parse_currency_rates(start_date, end_date, response)
#         else:
#             print("Ошибка при получении страницы:", response.status_code)
#             return []
#
#     def is_date_in_range(self, user_date, start_date, end_date):
#         try:
#             user_date = datetime.strptime(user_date[0].text.strip(), "%d.%m.%Y")
#             return start_date <= user_date <= end_date
#         except (ValueError, IndexError):
#             return False
#
#     def parse_currency_rates(self, start_date, end_date, response):
#         html_code = BeautifulSoup(response.text, 'html.parser')
#
#         # Находим все строки таблицы с данными о курсах валют
#         rows = html_code.find_all('tr')[1:]
#         for row in rows:
#             # Извлекаем данные из каждой строки
#             cells = row.find_all('td')
#             if self.is_date_in_range(cells, start_date, end_date):
#                 date = datetime.strptime(cells[0].text.strip(), "%d.%m.%Y").date()
#                 currency_unit = cells[1].text.strip()
#                 rate = float(cells[2].text.strip().replace(',', '.'))  # Преобразуем в формат float
#                 # Сохраняем данные в базу данных
#                 Currency.objects.create(code=self.code, country=currency_unit, rate=rate, date=date)
#
#
#     def parse_country(self):
#         response = requests.get("https://www.iban.ru/currency-codes")
#         html_code = BeautifulSoup(response.text, 'html.parser')
#         country = []
#         table = html_code.find('tbody')
#         for row in table.find_all('tr')[1:]:
#             columns = row.find_all('td')
#             if columns[2].text == self.code:
#                 country.append({
#                     "country": columns[0].text.strip(),
#                     "currency": columns[1].text.strip(),
#                 })
#
#         return country
#
# # def main():
# # Пример использования класса
# name = "EUR"
# parser = CurrencyRateParser(name)
# start_date = datetime.strptime("01.02.2022", "%d.%m.%Y")
# end_date = datetime.strptime("05.02.2022", "%d.%m.%Y")

# print(parser.fetch_currency_rates(start_date, end_date))
# print(parser.parse_country())

from django.db import models
from datetime import datetime
from bs4 import BeautifulSoup
import requests

from .models import Currency, Country


# class ParserCountry(models.Model):
#     name = models.CharField("Название страны", max_length=100)
#     currency = models.CharField("Валюта", max_length=3)
#
#     def __str__(self):
#         return self.name

# class ParserCurrency(models.Model):
#     code = models.CharField("Код валюты", max_length=3)
#     country = models.ForeignKey(ParserCounry, on_delete=models.CASCADE)
#     rate = models.DecimalField("Курс валюты", max_digits=10, decimal_places=4)
#     start_time = models.DateField("Начало периода")
#     end_time = models.DateField("Конец периода")
#     date = models.DateField("Дата")

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
        currency_rates = []

        # Находим все строки таблицы с данными о курсах валют
        rows = html_code.find_all('tr')[1:]
        for row in rows:
            # Извлекаем данные из каждой строки
            cells = row.find_all('td')
            if self.is_date_in_range(cells, start_date, end_date):
                date = datetime.strptime(cells[0].text.strip(), "%d.%m.%Y").date()
                currency_unit = cells[1].text.strip()
                rate = float(cells[2].text.strip().replace(',', '.'))
                Currency.objects.get_or_create(code=self.code, country=currency_unit, rate=rate, date=date)

        return currency_rates

    def parse_country(self):
        response = requests.get("https://www.iban.ru/currency-codes")
        html_code = BeautifulSoup(response.text, 'html.parser')

        table = html_code.find('tbody')
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if columns[2].text == self.code:
                country_name = columns[0].text.strip()
                currency_code = columns[1].text.strip()

                Country.objects.get_or_create(name=country_name, currency_code=currency_code)

#
# # # Пример использования класса
# name = "EUR"
# parser = CurrencyRateParser(name)
# start_date = datetime.strptime("01.02.2022", "%d.%m.%Y")
# end_date = datetime.strptime("05.02.2022", "%d.%m.%Y")
#
# # Получаем данные и сохраняем их в базу данных
# parser.fetch_currency_rates(start_date, end_date)
# # Получаем все записи о курсах валют из базы данных
# currencies = ParserCurrency.objects.all()
#
# # Печатаем или выводим полученные записи
# for currency in currencies:
#     print("DATA ABOUT CUR")
#     print(currency.code, currency.country, currency.rate, currency.start_time, currency.end_time)