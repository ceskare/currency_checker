# Generated by Django 5.0.4 on 2024-05-16 14:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0006_remove_currency_country_currency_countries_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='currency_code',
            field=models.CharField(max_length=3, null=True, verbose_name='Валюта'),
        ),
    ]
