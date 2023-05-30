# chat/consumers.py
import json
from .models import Message, Chatroom
from accounts.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        roomName = text_data_json["roomName"]
        sender = text_data_json["sender"]
        retriever = text_data_json["retriever"]
        senderUser = await sync_to_async(User.objects.get)(username=sender)
        retrieverUser = await sync_to_async(User.objects.get)(username=retriever)
        await sync_to_async(Message.objects.create)(content=message, sender=senderUser, retriever=retrieverUser, chatroom=await sync_to_async(Chatroom.objects.get)(pk=roomName))
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "sender": sender,}
        )

        

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        # WebSocket으로 메시지를 전송합니다.
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
        }))


class LoginConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("login을 하고 socket에 연결")
        # Add the user to a group or do any other initialization
        
    async def disconnect(self, close_code):
        print("logout을 하고 socket과 연결 종료")
        pass
        # Remove the user from the group or perform any cleanup
        
    async def receive(self, text_data):
        pass
        # Handle incoming messages from the client
        
    async def login_status_update(self, event):
        pass
        # Handle login status updates from the server
    # 알림에 대한 메세지
            # 메세지를 받으면
            # 알림 db에 쌓는다
                # sender와 message를 쌓는다.
            
# 이미 다른 곳에서 로그인