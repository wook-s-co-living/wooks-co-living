from accounts.models import User
from chats.models import Alarm

def all_users(request):
    all_users = User.objects.exclude(username=request.user.username)
    return {'all_users': all_users}

def all_alarms(request):
    all_alarms = Alarm.objects.filter(retriever=request.user)
    return {'all_alarms': all_alarms}