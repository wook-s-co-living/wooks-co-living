from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    age_Choices = (('10','20대 미만'),('20','20대'),('30','30대'),('40','40대'),('50','50대'),('60','60대 이상'))
    age = models.CharField(max_length=20, default='20', choices=age_Choices)

    address = models.CharField(max_length=200)
    town = models.CharField(max_length=100,blank=True,null=True)
    building = models.CharField(max_length=100,blank=True,null=True)

    introduce = RichTextUploadingField(blank=True,null=True)

    gender_Choices = (('male','남성'),('female','여성'))
    gender = models.CharField(max_length=20, choices=gender_Choices)

    maum = models.DecimalField(default=46.0, max_digits=4, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    likes = models.ManyToManyField('self', symmetrical=False, related_name='got_likes')
    dislikes = models.ManyToManyField('self', symmetrical=False, related_name='got_dislikes')
    

    # 이메일 인증
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=255, blank=True, null=True)

    def profile_image_path(instance, filename):
        return f'accounts/{instance.username}/{filename}'

    image_first = models.ImageField(upload_to=profile_image_path, null=True, blank=True)
    image = ImageSpecField(source='image_first',
                            processors=[ResizeToFill(300, 300)],
                            format='JPEG',
                            options={'quality': 100}
                            )

    def delete(self, *args, **kargs):
        if self.image_first:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image_first.path))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image_first.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(User, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(id=self.id)
            if self.image_first != old_user.image_first:
                if old_user.image_first:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_user.image_first.path))
        super(User, self).save(*args, **kwargs)

    def update_maum(self):
        like_count = self.likes.count()
        dislike_count = self.dislikes.count()
        self.maum = 46.0 - (0.1 * like_count) + (0.1 * dislike_count)
        self.save()
