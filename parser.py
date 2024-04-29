from datetime import datetime

import requests
from bs4 import BeautifulSoup


class Params:
    def __init__(self, id_val, pv_val, cur_val, x_val, y_val):
        self.id = id_val
        self.pv = pv_val
        self.cur = cur_val
        self.x = x_val
        self.y = y_val


class CurrencyRateParser:
    def __init__(self, url, code):
        self.url = url
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

    def parse_country(self):
        response = requests.get("https://www.iban.ru/currency-codes")
        html_code = BeautifulSoup(response.text, 'html.parser')
        country = []
        table = html_code.find('tbody')
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns[2].text == self.code:
                country.append({
                    "country": columns[0].text.strip(),
                    "currency": columns[1].text.strip(),
                })

        return country

# def main():
# Пример использования класса
url = "https://www.finmarket.ru/currency/rates/"
name = "EUR"
parser = CurrencyRateParser(url, name)
start_date = datetime.strptime("01.02.2022", "%d.%m.%Y")
end_date = datetime.strptime("05.02.2022", "%d.%m.%Y")

print(parser.fetch_currency_rates(start_date, end_date))
print(parser.parse_country())
