# Generated by Django 3.2.18 on 2023-06-01 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20230530_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_login',
            field=models.BooleanField(default=False),
        ),
    ]