import json
from .models import InstantMessage, Chat, User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['chat_id']

        await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chat_id': room,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['chat_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chat_id': room
        }))

    @sync_to_async
    def save_message(self, username, chat_id, message):
        user = User.objects.get(username=username)
        room = Chat.objects.get(id=chat_id)

        InstantMessage.objects.create(user=user, chat=room, 
                                    text=message)