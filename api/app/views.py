from django.shortcuts import render
from ..api.settings import firebase

database = firebase.database()

def index(request):
    return render(request, 'index.html')
