from django.db import models
from accounts.models import User
from datetime import timedelta,datetime
from django.utils import timezone
# Create your models here.
class Chatroom(models.Model):
    user1 = models.ForeignKey(User, related_name='chatrooms_as_user1', null=True, on_delete=models.SET_NULL)
    user2 = models.ForeignKey(User, related_name='chatrooms_as_user2', null=True, on_delete=models.SET_NULL)  # 대화에 참여하는 참가자 둘
    created_at = models.DateTimeField(auto_now_add=True)

    def get_latest_message(self):
        return self.message_set.order_by('-created_at').first()

class Message(models.Model):
    content = models.TextField()  # 메시지 내용
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # 메시지 작성일시
    sender = models.ForeignKey(User, related_name='messages_as_sender', null=True, on_delete=models.SET_NULL)
    retriever = models.ForeignKey(User, related_name='messages_as_retriever', null=True, on_delete=models.SET_NULL)


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
        
class Alarm(models.Model):
    sender = models.ForeignKey(User, related_name='alarms_as_sender', on_delete=models.CASCADE)
    retriever = models.ForeignKey(User, related_name='alarms_as_retriever', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 메시지 작성일시