# Generated by Django 4.2.4 on 2023-11-15 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_rename_amount_paid_payment_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='invoice',
        ),
        migrations.AddField(
            model_name='payment',
            name='invoice_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
