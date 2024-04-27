from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings

database = settings.firebase.database()

def index():
