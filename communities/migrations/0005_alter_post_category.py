# Generated by Django 3.2.18 on 2023-06-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('-', '-'), ('건물 소식', '건물 소식'), ('자취 꿀팁', '자취 꿀팁'), ('같이 사요', '같이 사요')], max_length=40),
        ),
    ]