from accounts.models import User
from chats.models import Message
from django.contrib.auth.decorators import login_required

# @login_required
def unchecked_alarms (request):
    if request.user.is_authenticated:  # 로그인 상태인 경우에만 실행
        unchecked_alarms = Message.objects.filter(is_checked=0, retriever=request.user).order_by('-created_at')[:5]
        has_unchecked_alarms = unchecked_alarms.exists()
    else:
        unchecked_alarms = []
        has_unchecked_alarms = False
    
    return {'unchecked_alarms': unchecked_alarms , 'has_unchecked_alarms': has_unchecked_alarms}