import json
from .models import InstantMessage, Chat, User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        chat = data['chat_id']

        await self.save_message(username, chat, message)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chat_id': chat,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chat = event['chat_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chat_id': chat
        }))

    @sync_to_async
    def save_message(self, username, chat_id, message):
        user = User.objects.get(username=username)
        chat = Chat.objects.get(id=chat_id)

        InstantMessage.objects.create(user=user, chat=chat, 
                                    text=message)