from django.contrib import admin
from .models import User, InstantMessage, Chat, UserToChat

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass


@admin.register(InstantMessage)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(UserToChat)
class UserToChatAdmin(admin.ModelAdmin):
    pass