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
    path('delete_user/', 
        app_views.UserDeleteView.as_view(), name='delete_user'),
    path('edit_user/', 
        app_views.UserEditView.as_view(), name='edit_user'),
    path('staticfiles/<str:filename>/', 
        app_views.staticfiles), # can't use name 'static' (reserved for Django specifically)
    path('send/<int:chat_id>/', 
        app_views.SendMessageView.as_view(), name='send_message'),
    path('chats/', app_views.AllUserChatsView.as_view(), name='chats'),
    path('chat/<int:chat_id>', 
        app_views.chat_json),
]