from django.shortcuts import HttpResponse
from django.http import JsonResponse
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

def get_story(request):
    return JsonResponse({"status": 200})