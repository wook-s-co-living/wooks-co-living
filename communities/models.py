from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from taggit.managers import TaggableManager
from datetime import timedelta,datetime,date
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_communities_posts')
    title = models.CharField(max_length=100)
    content = content = RichTextUploadingField(blank=True,null=True)
    category_Choices = (('', '카테고리'),('일상 이야기', '일상 이야기'), ('건물 소식', '건물 소식'), ('자취 꿀팁', '자취 꿀팁'), ('같이 사요', '같이 사요'))
    category = models.CharField(max_length=40, choices=category_Choices)
    views = models.IntegerField(default=0) #models.PositiveIntegerField(default=0, verbose_name='조회수')

    scrape_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='scrape_communities_posts')
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
        
    @property
    def likes_count(self):
        return self.like_users.count()-self.dislike_users.count()
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_communities_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='child_comments')
    content = models.TextField(null=True)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_communities_comments')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_communities_comments')

    created_at = models.DateTimeField(auto_now_add=True)

    depth = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    @property
    def likes_count(self):
        return self.like_users.count()-self.dislike_users.count()

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