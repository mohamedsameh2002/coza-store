# Generated by Django 4.2.4 on 2023-09-21 01:55

import discounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount_codes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=discounts.models.random_code, max_length=10)),
                ('discount', models.IntegerField(max_length=100)),
                ('validate_from', models.DateTimeField()),
                ('validate_to', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
