# Generated by Django 4.2.4 on 2023-09-17 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_blog_tag1_remove_blog_tag2_remove_blog_tag3_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='criated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
