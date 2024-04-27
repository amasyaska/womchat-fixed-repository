from .views import UserRegisterView, UserAuthenticateView, index
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('login/', UserAuthenticateView.as_view(), name='login')
]