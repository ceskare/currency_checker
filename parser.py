# from datetime import datetime
# import requests
# from bs4 import BeautifulSoup

class Params:
    def __init__(self, id_val, pv_val, cur_val, x_val, y_val):
        self.id = id_val
        self.pv = pv_val
        self.cur = cur_val
        self.x = x_val
        self.y = y_val


# def is_date_in_range(user_date, start_date, end_date):
#     try:
#         user_date = datetime.strptime(user_date[0].text.strip(), "%d.%m.%Y")
#         return start_date <= user_date <= end_date
#     except (ValueError, IndexError):
#         pass
#
#
# def parse_currency_rates(start_date, end_date, response):
#     html_code = BeautifulSoup(response.text, 'html.parser')
#     currency_rates = []
#
#     # Находим все строки таблицы с данными о курсах валют
#     rows = html_code.find_all('tr')
#     for row in rows:
#         # Извлекаем данные из каждой строки
#         cells = row.find_all('td')
#         if is_date_in_range(cells, start_date, end_date):
#             date = cells[0].text.strip()  # Дата
#             currency_unit = cells[1].text.strip()  # Единица валюты
#             rate = cells[2].text.strip()  # Курс
#             change = cells[3].text.strip()  # Изменение курса
#             # Добавляем данные в список курсов валют
#             currency_rates.append({
#                 "date": date,
#                 "currency_unit": currency_unit,
#                 "rate": rate,
#                 "change": change
#             })
#
#     return currency_rates
#
#
# def fetch_currency_rates(start_date, end_date):
#     url = "https://www.finmarket.ru/currency/rates/"
#     params = {
#         "id": 10148,
#         "pv": 1,
#         "cur": 52170,
#         "bd": start_date.day,
#         "bm": start_date.month,
#         "by": start_date.year,
#         "ed": end_date.day,
#         "em": end_date.month,
#         "ey": end_date.year,
#         "x": 48,
#         "y": 13
#     } #EURO
#
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return parse_currency_rates(start_date, end_date, response)
#     else:
#         print("Ошибка при получении страницы:", response.status_code)
#         return -1
#
#
# start_date = datetime.strptime("01.02.2022", "%d.%m.%Y")
# end_date = datetime.strptime("05.02.2022", "%d.%m.%Y")
#
# print(fetch_currency_rates(start_date, end_date))

from datetime import datetime

import requests
from bs4 import BeautifulSoup


# TRY =
# JXY =
# INR =
# CNY =

class CurrencyRateParser:
    def __init__(self, url):
        self.url = url

    def fetch_currency_rates(self, start_date, end_date):
        # if ''
        # params = Params(10148, 1, 52170, 48, 13)
        # params = {
        #     "id": 10148,
        #     "pv": 1,
        #     "cur": 52170,
        #     "bd": start_date.day,
        #     "bm": start_date.month,
        #     "by": start_date.year,
        #     "ed": end_date.day,
        #     "em": end_date.month,
        #     "ey": end_date.year,
        #     "x": 48,
        #     "y": 13
        # }  # EURO
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
        currency_name = "EURO"

        if currency_name == "EURO":
            currency_params["cur"] = 52170
        elif currency_name == "USD":
            currency_params["cur"] = 52148
        elif currency_name == "GBP":
            currency_params["cur"] = 52146
        elif currency_name == "TRY":
            currency_params["cur"] = 52158
        elif currency_name == "CNY":
            currency_params["cur"] = 52207
        elif currency_name == "INR":
            currency_params["cur"] = 52238
        elif currency_name == "JXY":
            currency_params["cur"] = 52246
        response = requests.get(self.url, params=currency_params)
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
        rows = html_code.find_all('tr')
        for row in rows:
            # Извлекаем данные из каждой строки
            cells = row.find_all('td')
            if self.is_date_in_range(cells, start_date, end_date):
                date = cells[0].text.strip()  # Дата
                currency_unit = cells[1].text.strip()  # Единица валюты
                rate = cells[2].text.strip()  # Курс
                change = cells[3].text.strip()  # Изменение курса
                # Добавляем данные в список курсов валют
                currency_rates.append({
                    "date": date,
                    "currency_unit": currency_unit,
                    "rate": rate,
                    "change": change
                })

        return currency_rates

# def main():
# Пример использования класса
url = "https://www.finmarket.ru/currency/rates/"
parser = CurrencyRateParser(url)
start_date = datetime.strptime("01.02.2022", "%d.%m.%Y")
end_date = datetime.strptime("05.02.2022", "%d.%m.%Y")

print(parser.fetch_currency_rates(start_date, end_date))
