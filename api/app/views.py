from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from .permissions import IsNotAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
