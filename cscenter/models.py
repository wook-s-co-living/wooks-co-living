from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from datetime import timedelta,datetime
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_cscenter_posts')
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True,null=True)
    category_Choices = (('계정 문의', '계정 문의'), ('채팅, 알림', '채팅, 알림'), ('커뮤니티', '커뮤니티'), ('플리마켓', '플리마켓'), ('모임', '모임'), ('기타', '기타'))
    category = models.CharField(max_length=40, choices=category_Choices)
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