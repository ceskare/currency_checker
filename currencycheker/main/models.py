from django.utils import timezone
from django.db import models
class Country(models.Model):
    name = models.CharField("Страна", max_length=100, db_index=True)
    currency_code = models.CharField("Валюта", max_length=3, null=True)
    def __str__(self):
        return self.name

class Currency(models.Model):
    code = models.CharField("Код валюты", max_length=3, default="EUR")
    rate = models.DecimalField("Курс валюты", max_digits=10, decimal_places=4)
    change = models.CharField("Изменение курса", max_length=7, default="")
    date = models.DateField("Дата", default=timezone.now)
    countries = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.code

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
