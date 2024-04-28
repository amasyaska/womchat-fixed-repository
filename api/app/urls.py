from  . import views as app_views
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', app_views.index, name='index'),
    path('registration/', app_views.UserRegisterView.as_view(), name='registration'),
    path('login/', app_views.UserAuthenticateView.as_view(), name='login'),
    path('logout/', app_views.UserLogoutView.as_view(), name='logout'),
    path('delete_user/', app_views.UserDeleteView.as_view(), name='delete_user'),
    path('staticfiles/<str:filename>/', app_views.staticfiles), # can't use name 'static' (reserved for Django specifically)
    path('chat/', app_views.chat),
    path('chat/<int:chat_id>', app_views.chat_json),
]