# Generated by Django 4.2.4 on 2023-09-15 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_accounts_address_line_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pictuer',
            field=models.ImageField(blank=True, default='userprofile/blog-05_2SI8kgU.jpg', null=True, upload_to='userprofile'),
        ),
    ]
