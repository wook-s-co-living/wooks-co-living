# Generated by Django 3.2.18 on 2023-06-08 06:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0008_post_scrape_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='depth',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]