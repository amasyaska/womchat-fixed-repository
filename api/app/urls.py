from .views import UserRegisterView, index
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
]