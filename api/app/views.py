import os
from django.db.models.query import QuerySet
from .models import InstantMessage, Chat, User, UserToChat
from django.http import HttpResponse
from django.contrib.auth import logout, login, update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.generics import (RetrieveUpdateAPIView, 
    CreateAPIView, ListAPIView)
from .serializers import (UserSerializer, UserLoginSerializer,
    MessageSerializer, ChatSerializer)
from .permissions import IsNotAuthenticated, CustomIsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication, 
    authenticate)

def staticfiles(request, filename):
    static_path = os.path.join(os.path.abspath(__file__), "..", "..", "..", "static")
    with open(os.path.join(static_path, filename), 'r') as f:
        file_data = f.read()
        response = HttpResponse(file_data)
        if (filename.split('.')[-1] == 'js'):
            response['Content-Type'] = 'application/javascript; charset=utf-8'
        if (filename.split('.')[-1] == 'css'):
            response['Content-Type'] = 'text/css; charset=utf-8'
    return response


class UserRegisterView(CreateAPIView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)
            if user:
                return Response(
                    status=status.HTTP_200_OK
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class UserAuthenticateView(APIView):
    permission_classes = (IsNotAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(request, **serializer.validated_data)
            if user is None:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class UserLogoutView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    

class UserInfoView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(instance=request.user)
        data = serializer.data
        data.pop('password')
        data['special_mode'] = request.user.special_mode
        return Response(data=data, status=status.HTTP_200_OK)


class UserDeleteView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        logout(request)

        return Response(status=status.HTTP_200_OK)


class UserEditView(RetrieveUpdateAPIView):
    permission_classes = (CustomIsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.get_serializer(
            instance=request.user)
        data = serializer.data
        data.pop('password')
        return Response(data=data, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        return self.request.user

    def update(self, request):
        serializer = self.get_serializer(instance=request.user, 
                                        data=request.data, 
                                        partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.update(request.user, 
                                    serializer.validated_data)
            update_session_auth_hash(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SendMessageView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def post(self, request, chat_id: int):
        chat = Chat.objects.get(id=chat_id)
        message_text = request.data.get('message')
        if not message_text:
            return Response(
                data={'error': "You can't send empty message."},
                status=status.HTTP_400_BAD_REQUEST
            )
        message = InstantMessage(text=message_text,
                            chat=chat, user=request.user)
        message.save()

        return Response(status=status.HTTP_200_OK)


class ChatView(ListAPIView):
    permission_classes = (CustomIsAuthenticated,)
    serializer_class = MessageSerializer

    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        try:
            UserToChat.objects.get(user=request.user, chat=chat)
        except UserToChat.DoesNotExist:
            return Response(
                data={'error': "You are not a member of this chat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        messages = self.get_serializer(
            instance=chat.messages.all(), many=True
        )
        return Response(
            data={'messages': messages.data},
            status=status.HTTP_200_OK
        )


class AllUserChatsView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def get(self, request):
        chats = list(map(lambda instance: instance.chat, 
                    request.user.user_to_chat.all()))
        serializer = ChatSerializer(instance=chats, many=True)
        data = serializer.data
        return Response(data={"chats": data}, status=status.HTTP_200_OK)
    

class CreateChatView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def post(self, request):
        users_list = request.data.get('users')
        chat_type = request.data.get('chat_type', 0)
        if chat_type == 0:
            if len(users_list) > 1:
                return Response(
                    data={
                        'error': 'Private chat is only for two users.'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            try:
                private_chats_1 = set(
                    request.user.user_to_chat.values_list('chat_id')
                )
                private_chats_2 = set(
                    User.objects.get(
                        username=users_list[0]).user_to_chat.values_list('chat_id')
                )
            except User.DoesNotExist:
                return Response(
                    data={'error': 
                        f"User with name {users_list[0]} doesn't exist."
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            if private_chats_1 & private_chats_2:
                return Response(
                    data={
                        'error': 'You already have private chat with this user.'
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        chat_title = request.data.get('title', 'new chat')
        users = []
        for username in users_list:
            try:
                user = User.objects.get(username=username)
                users.append(user)
            except User.DoesNotExist:
                return Response(
                    data={
                        'error': f"User with name {username} doesn't exist."
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        chat = Chat.objects.create(title=chat_title, 
                                chat_type=chat_type)
        UserToChat(chat=chat, user=request.user).save()
        for user in users:
            UserToChat(chat=chat, user=user).save()

        return Response(status=status.HTTP_200_OK)