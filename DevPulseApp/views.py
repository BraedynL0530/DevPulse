from django.shortcuts import render
from rest_framework_api_key.models import APIKey

def getApiKey(request):
    api_key, key = APIKey.objects.create_key(name="api_keys")

def addHistory(request):
    return None

def fetchHistory(request):
    return None