# Generated by Django 4.2.4 on 2023-08-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='color',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='size',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
