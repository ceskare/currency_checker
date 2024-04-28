import requests
from bs4 import BeautifulSoup


def parse_currency_rates(start_date, end_date, response):
    html_code = BeautifulSoup(response.text, 'html.parser')
    currency_rates = []

    # Находим все строки таблицы с данными о курсах валют
    rows = html_code.find_all('tr')
    for row in rows:
        # Извлекаем данные из каждой строки
        cells = row.find_all('td')
        if start_date in row.text or end_date in row.text:

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


def fetch_currency_rates(start_date, end_date):
    url = "https://www.finmarket.ru/currency/rates/"
    params = {
        "id": 10148,
        "pv": 1,
        "cur": 52170,
        "bd": start_date[0:2],
        "bm": start_date[3:5],
        "by": start_date[6:10],
        "ed": end_date[0:2],
        "em": end_date[3:5],
        "ey": end_date[6:10],
        "x": 48,
        "y": 13
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return parse_currency_rates(start_date, end_date, response)
    else:
        print("Ошибка при получении страницы:", response.status_code)
        return -1


# Пример использования функции
start_date = "01.02.2022"
end_date = "05.02.2022"
print(fetch_currency_rates(start_date, end_date))
