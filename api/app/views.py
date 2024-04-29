import os
from .models import InstantMessage, Chat, User, UserToChat
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout, login, update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.generics import (RetrieveUpdateAPIView, 
    CreateAPIView)
from .serializers import (UserSerializer, UserLoginSerializer)
from .permissions import IsNotAuthenticated, CustomIsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication, 
    authenticate)

def index(request):
    return render(request, 'index.html')


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


def chat_json(request, chat_id):
    '''
    !!! implement check if user is allowed to read this chat here !!!
    pseudo-code
    dct = dict()
    for message in chat_id:
        dct[message_id] = message_text
    return JsonResponse(dct)
    '''
    message_to_user_and_text = dict()
    message_to_user_and_text["messages"] = []
    for message in InstantMessage.objects.filter(chat=chat_id):
        message_to_user_and_text["messages"].append([message.id, message.user.id, message.text, message.date_added])
    return JsonResponse(message_to_user_and_text)


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


class UserDeleteView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def post(self, request):
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
        return Response(data=data,
                        status=status.HTTP_200_OK)
    
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

    def post(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        message_text = request.data.get('message', None)
        if not message_text:
            raise ValueError('empty message.')
        message = InstantMessage(text=message_text,
                            chat=chat, user=request.user)
        message.save()

        return Response(status=status.HTTP_200_OK)
    

class AllUserChatsView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def get(self, request):
        user_to_chats = request.user.chats.all()
        data = {}
        for user_to_chat in user_to_chats:
            chat = user_to_chat.chat
            data[chat.id] = [chat.title, 
                            chat.messages.latest('date_added').text]
        return Response(data=data, status=status.HTTP_200_OK)
    

class CreateChatWithUserView(APIView):
    permission_classes = (CustomIsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            if request.user.username == username:
                raise ValueError("You can't create a chat with yourself.")
            user = User.objects.get(
                username=request.data.get('username'))
        except (User.DoesNotExist, ValueError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        chat_title = request.data.get('chat_title', 'new chat')
        chat = Chat.objects.create(title=chat_title)
        UserToChat(chat=chat, user=request.user).save()
        UserToChat(chat=chat, user=user).save()

        return Response(data={
            'chat_title': chat_title,
            'user_1': request.user.__str__(),
            'user_2': user.__str__(),
            }, status=status.HTTP_200_OK)