from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, clean_data):
        if not clean_data.get('username', None):
            raise ValidationError(
                "Username field can't be blank."
            )
        user = User.objects.create_user(**clean_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=35)
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username and not email:
            raise serializers.ValidationError(
                "Must include username or email."
            )
        else:
            if not password:
                raise serializers.ValidationError(
                    'Must include "password"'
                )
            if email:
                user = authenticate(
                    request=self.context.get('request'),
                    email=email,
                    password=password
                )
            elif username:
                user = authenticate(
                    request=self.context.get('request'),
                    username=username,
                    password=password
                )
        data['user'] = user
        return data