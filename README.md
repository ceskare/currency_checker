# Django Currency Data Project

## Описание проекта

Этот проект предназначен для отображения данных о валютах различных стран с использованием Django. Вы можете выбирать страны, чтобы увидеть данные о валютных курсах, которые будут представлены в таблице и на графике с помощью Highcharts.

## Структура проекта

- **models.py**: Определяет модели `Country` и `Currency`.
- **views.py**: Содержит представления для отображения данных о валютах.
- **urls.py**: Определяет маршруты URL для доступа к представлениям.
- **templates/**: Содержит HTML шаблоны для отображения данных.
- **static/**: Включает статические файлы, такие как CSS.

## Установка и настройка

### Установка зависимостей

Создайте виртуальное окружение и установите необходимые зависимости:

```bash
python -m venv venv
source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
pip install -r requirements.txt
```

### Запуск сервера разработки
#### Запустите сервер разработки Django:

```bash
python manage.py runserver
```

Перейдите по адресу http://127.0.0.1:8000/ в вашем веб-браузере для доступа к приложению.

### Использование
#### Основная страница
На основной странице вы можете выбрать страны, для которых хотите отобразить данные о валютах. Выбранные страны будут сохранены в сессии.

#### Страница графика
На странице графика отображаются данные о валютах выбранных стран в виде таблицы и графика. Данные загружаются асинхронно с помощью Fetch API и отображаются с помощью Highcharts.

### Модели:
#### Country
Модель Country представляет страны и содержит следующие поля:

    name: Имя страны.  
    currency_code: Код валюты страны.

#### Currency
Модель Currency представляет данные о валюте и содержит следующие поля:

    code: Код валюты.  
    rate: Курс валюты.  
    change: Изменение курса валюты.  
    date: Дата курса валюты.  
    countries: Внешний ключ, связывающий валюту с моделью Country.  
