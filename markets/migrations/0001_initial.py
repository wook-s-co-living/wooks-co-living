# Generated by Django 3.2.18 on 2023-06-13 05:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import markets.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('price', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('sale_status', models.CharField(choices=[('판매중', '판매중'), ('예약중', '예약중'), ('판매완료', '판매완료')], default='판매중', max_length=20, null=True)),
                ('views', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('like_users', models.ManyToManyField(related_name='like_markets_posts', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_markets_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Postimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_first', models.ImageField(blank=True, null=True, upload_to=markets.models.Postimage.post_image_path)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postimages', to='markets.post')),
            ],
        ),
    ]
