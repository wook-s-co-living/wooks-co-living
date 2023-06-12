from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from datetime import timedelta,datetime,date
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import Thumbnail
import os
from django.conf import settings

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_markets_posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    sale_status_Choices = (('판매중','판매중'), ('예약중','예약중'), ('판매완료','판매완료'))
    sale_status = models.CharField(max_length=20, default='판매중', choices=sale_status_Choices, null=True)

    views = models.IntegerField(default=0)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_markets_posts')

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

    def delete(self, *args, **kwargs):
        images = self.postimages.all()
        for image in images:
            image.delete()
        super(Post, self).delete(*args, **kwargs)

class Postimage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postimages')

    def post_image_path(instance, filename):
        return f'markets/{instance.post.user.username}/{filename}'

    image_first = models.ImageField(upload_to=post_image_path, null=True, blank=True)
    image = ImageSpecField(source='image_first',
                            processors=[ResizeToFill(800, 800)],
                            format='JPEG',
                            options={'quality': 100}
                            )

    def delete(self, *args, **kargs):
        if self.image_first:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image_first.path))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image_first.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(Postimage, self).delete(*args, **kargs)
