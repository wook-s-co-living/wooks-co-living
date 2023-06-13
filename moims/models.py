from django.db import models
import os
from django.conf import settings
from django.core.validators import MinValueValidator
from datetime import timedelta,datetime,date
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail, ResizeToFill

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_moims_posts')
    title = models.CharField(max_length=100)
    content = models.TextField()

    category_Choices = (('many','정기모임'),('once','당일모임'))
    category = models.CharField(max_length=20, choices=category_Choices)

    many_datetime = models.CharField(max_length=50, null=True, blank=True)
    once_datetime = models.DateTimeField(null=True, blank=True)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_moims_posts')

    limit = models.IntegerField(default=1)
    join_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='join_moims_posts')

    address = models.CharField(max_length=200)
    town = models.CharField(max_length=100,blank=True,null=True)
    building = models.CharField(max_length=100,blank=True,null=True)
    detail_address = models.CharField(max_length=200)
    kakao_url = models.CharField(null=True, max_length=300)

    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def created_time(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')
    
    def post_image_path(instance, filename):
        return f'moims/{instance.user.username}/{filename}'

    image_first = models.ImageField(upload_to=post_image_path, null=True)
    image = ImageSpecField(source='image_first',
                            processors=[ResizeToFill(350, 250)],
                            format='JPEG',
                            options={'quality': 100}
                            )

    def delete(self, *args, **kargs):
        if self.image_first:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image_first.path))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image_first.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Post, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_user = Post.objects.get(id=self.id)
            if self.image_first != old_user.image_first:
                if old_user.image_first:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_user.image_first.path))
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_moims_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='child_comments')
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    depth = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    @property
    def created_time(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')