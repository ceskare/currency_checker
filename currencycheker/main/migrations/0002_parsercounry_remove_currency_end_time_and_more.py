# Generated by Django 5.0.4 on 2024-05-07 10:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParserCounry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название страны')),
                ('currency', models.CharField(max_length=3, verbose_name='Валюта')),
            ],
        ),
        migrations.RemoveField(
            model_name='currency',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='start_time',
        ),
        migrations.AddField(
            model_name='currency',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
        migrations.CreateModel(
            name='ParserCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, verbose_name='Код валюты')),
                ('rate', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Курс валюты')),
                ('start_time', models.DateField(verbose_name='Начало периода')),
                ('end_time', models.DateField(verbose_name='Конец периода')),
                ('date', models.DateField(verbose_name='Дата')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.parsercounry')),
            ],
        ),
    ]
