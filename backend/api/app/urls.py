from  . import views as app_views
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('registration/', 
        app_views.UserRegisterView.as_view(), name='registration'),
    path('login/', 
        app_views.UserAuthenticateView.as_view(), name='login'),
    path('logout/', 
        app_views.UserLogoutView.as_view(), name='logout'),

    path('user/info/', 
        app_views.UserInfoView.as_view(), name='user_info'),
    path('user/delete/', 
        app_views.UserDeleteView.as_view(), name='delete_user'),
    path('user/edit/', 
        app_views.UserEditView.as_view(), name='edit_user'),
    
    path('staticfiles/<str:filename>/', 
        app_views.staticfiles), # can't use name 'static' (reserved for Django specifically)
    
    path('chats/',
        app_views.AllUserChatsView.as_view(), name='chats'),
    path('chats/<int:chat_id>/', app_views.ChatView.as_view(),
        name='chat'),
    path('chats/<int:chat_id>/send/', 
        app_views.SendMessageView.as_view(), name='send_message'),
    path('chats/create/', 
        app_views.CreateChatView.as_view(), name='create_chat'),
]