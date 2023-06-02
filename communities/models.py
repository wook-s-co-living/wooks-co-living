from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from datetime import timedelta,datetime,date
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_communities_posts')
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True,null=True)
    category = models.CharField(max_length=40, blank=True)
    views = models.PositiveIntegerField(default=0, verbose_name='조회수')

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_communities_posts')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_communities_posts')

    tags = TaggableManager(blank=True)
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
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_communities_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='child_comments')
    content = RichTextUploadingField(blank=True,null=True)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_communities_comments')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_communities_comments')

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