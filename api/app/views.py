from django.shortcuts import render
from django.contrib.auth import logout, login
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .permissions import IsNotAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication, 
                                        authenticate)

def index(request):
    return render(request, 'index.html')


class UserRegisterView(APIView):
    permission_classes = (IsNotAuthenticated,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)
            if user:
                return Response(
                    serializer.validated_data,
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
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
