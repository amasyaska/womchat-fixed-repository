from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings

database = firebase.database()

def index(request):
    return render(request, 'index.html')