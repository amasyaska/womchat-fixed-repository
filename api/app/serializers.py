from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import User, InstantMessage, Chat

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=35, required=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9_]+$',
                message='You can use only letters, digits and underscore'
        )])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'special_mode')

    def create(self, clean_data):
        user = User.objects.create_user(**clean_data)
        return user
    
    def update(self, instance, clean_data):
        password = clean_data.pop('password', instance.password)

        for key, value in clean_data.items():
            setattr(instance, key, value)

        instance.set_password(password)

        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=35, required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
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
        return data   


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('title', 'chat_type')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            last_message = instance.messages.latest('date_added').text
        except InstantMessage.DoesNotExist:
            last_message = ""
        data['last_message'] = last_message
        return data

class MessageSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(source='date_added')

    class Meta:
        model = InstantMessage
        fields = ('id', 'user', 'text', 'timestamp')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_id = data.pop('user')
        data['username'] = User.objects.get(id=user_id).username
        if self.context['request'].user.username == data['username']:
            data['is_own'] = True
        else:
            data['is_own'] = False
        return data