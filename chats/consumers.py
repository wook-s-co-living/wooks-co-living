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

        loginUser = str(self.scope["user"])
        print(loginUser)
        loginStatus = True

        user = await sync_to_async(User.objects.get)(username=loginUser)
        user.is_login = True
        await sync_to_async(user.save)()

        await self.channel_layer.group_add("login_group", self.channel_name)

        await self.channel_layer.group_send(
            "login_group", {"type": "chat_message", "loginUser": loginUser, "loginStatus": loginStatus,}
        )

    async def disconnect(self, close_code):
        print("logout을 하고 socket과 연결 종료")

        loginUser = str(self.scope["user"])
        print(loginUser)
        loginStatus = False

        user = await sync_to_async(User.objects.get)(username=loginUser)
        user.is_login = False
        await sync_to_async(user.save)()

        await self.channel_layer.group_send(
            "login_group", {"type": "chat_message", "loginUser": loginUser, "loginStatus": loginStatus,}
        )

        await self.channel_layer.group_discard("login_group", self.channel_name)

    async def chat_message(self, event):
        loginUser = event["loginUser"]
        loginStatus = event["loginStatus"]

        # WebSocket으로 메시지를 전송합니다.
        await self.send(text_data=json.dumps({
            "loginUser": loginUser,
            "loginStatus": loginStatus,
        }))


class AlarmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("login을 하고 socket에 연결")
        await self.channel_layer.group_add("alarm_group", self.channel_name)
        # Add the user to a group or do any other initialization
        
    async def disconnect(self, close_code):
        print("logout을 하고 socket과 연결 종료")
        print(close_code)
        await self.channel_layer.group_discard("alarm_group", self.channel_name)
        # Remove the user from the group or perform any cleanup
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        roomName = text_data_json["roomName"]
        sender = text_data_json["sender"]
        retriever = text_data_json["retriever"]
        senderUser = await sync_to_async(User.objects.get)(username=sender)
        if senderUser.image :
            senderImage = senderUser.image.url
        else : 
            senderImage = "/static/image/noimage.png"
        
        # await sync_to_async(Message.objects.create)(content=content, sender=sender, retriever=retriever)
        # Send message to room group
        await self.channel_layer.group_send(
            "alarm_group", {"type": "alarm_message", "sender": sender, "retriever": retriever, "roomName": roomName,}
        )

    async def alarm_message(self, event):
        sender = event["sender"]
        retriever = event["retriever"]
        senderUser = await sync_to_async(User.objects.get)(username=sender)
        sendername = senderUser.first_name
        roomName = event["roomName"]
        
        # WebSocket으로 메시지를 전송합니다.
        await self.send(text_data=json.dumps({
            "sender": sender,
            "retriever": retriever,
            
            "roomName": roomName,
            "sendername": sendername,
        }))
        

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]
#         sender = event["sender"]

#         # WebSocket으로 메시지를 전송합니다.
#         await self.send(text_data=json.dumps({
#             "message": message,
#             "sender": sender,
#         }))
#         # Handle login status updates from the server
#     # 알림에 대한 메세지
#             # 메세지를 받으면
#             # 알림 db에 쌓는다
#                 # sender와 message를 쌓는다.
#             # 커넥트가 된 상태라면 message가 전송될 때마다 알림을 보낸다. 어디에 base.html에다가 하면 된다.
            
# # 이미 다른 곳에서 로그인

class IndexConsumer(AsyncWebsocketConsumer):
    async def connect(self):
            await self.accept()
            await self.channel_layer.group_add("index_group", self.channel_name)
            # Add the user to a group or do any other initialization

    async def disconnect(self, close_code):
        print(close_code)
        await self.channel_layer.group_discard("index_group", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        roomName = text_data_json["roomName"]
        sender = text_data_json["sender"]
        retriever = text_data_json["retriever"]
        senderUser = await sync_to_async(User.objects.get)(username=sender)
        if senderUser.image :
            senderImage = senderUser.image.url
        else : 
            senderImage = "/static/image/noimage.png"
        retrieverUser = await sync_to_async(User.objects.get)(username=retriever)
        # await sync_to_async(Message.objects.create)(content=message, sender=senderUser, retriever=retrieverUser, chatroom=await sync_to_async(Chatroom.objects.get)(pk=roomName))
        # Send message to room group
        await self.channel_layer.group_send(
            "index_group", {"type": "index_message", "sender": sender, "retriever": retriever, "message": message, "roomName": roomName, "sender": sender, "senderImage": senderImage}
        )

    async def index_message(self, event):
        sender = event["sender"]
        retriever = event["retriever"]
        message = event["message"]
        roomName = event["roomName"]
        sendername = event["sender"]
        senderImage = event["senderImage"]
        # WebSocket으로 메시지를 전송합니다.
        await self.send(text_data=json.dumps({
            "sender": sender,
            "retriever": retriever,
            "message": message,
            "roomName": roomName,
            "sendername": sendername,
            "senderImage": senderImage,
        }))