from django.utils import timezone
from django.db import models

class Currency(models.Model):
    code = models.CharField("Код валюты", max_length=3)
    country = models.CharField("Код страны", max_length=10)
    rate = models.DecimalField("Курс валюты", max_digits=10, decimal_places=4)
    # start_time = models.DateField("Начало периода")
    # end_time = models.DateField("Конец периода")
    date = models.DateField("Дата", default=timezone.now)

    def __str__(self):
        return self.code, self.country, self.rate, self.date

class Country(models.Model):
    name = models.CharField("Страна", max_length=100)
    currency_code = models.CharField("Код валюты", max_length=3)
    # @classmethod
    # def update_or_create(cls, code, country, rate, start_time, end_time):
    #     obj, created = cls.objects.update_or_create(
    #         code=code,
    #         country=country,
    #         rate=rate,
    #         start_time=start_time,
    #         end_time=end_time
    #     )
    #     # Если запись была создана, возвращаем True, иначе False
    #     return created