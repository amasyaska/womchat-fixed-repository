from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import BaseUserManager
from django.urls import reverse
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, email=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is False:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is False:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, email, **extra_fields)
    

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                        editable=False)
    email = models.EmailField(blank=True, null=True, default="")
    username = models.CharField(max_length=35, unique=True, 
                                blank=True, null=True)
    special_mode = models.BooleanField(default=False)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def clean(self) -> None:
        if not self.username:
            raise ValidationError(
                "Username field can't be blank."
            )
        if self.email and User.objects.filter(
            email=self.email).exclude(id=self.id).exists():
            raise ValidationError(
                "User with this email already exists."
            )
        return super().clean()

    def __str__(self):
        if self.email:
            return self.email
        return self.username if self.username else ''


class Chat(models.Model):
    '''
    one-to-many relationship between Chat and Message
    '''
    class ChatType(models.IntegerChoices):
        PRIVATE = 0, 'Private'
        GROUP = 1, 'Group'

    chat_type = models.IntegerField(
        choices=ChatType.choices,
        default=ChatType.PRIVATE,
        verbose_name='type'
    )
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('app:send_message', args=[self.id])


class InstantMessage(models.Model):
    text = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE,
                                related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='messages')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

    def __str__(self) -> str:
        text = self.text[:20]
        if len(self.text) > 20:
            text += '...'
        return f' from {self.user} in {self.chat}: {text}'


class UserToChat(models.Model):
    '''
    join table to implement many-to-many relationship between User and Chat
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                                related_name='user_to_chat')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE,
                                related_name='user_to_chat')
    
    def __str__(self) -> str:
        return f'user: {self.user}, chat: {self.chat}'
