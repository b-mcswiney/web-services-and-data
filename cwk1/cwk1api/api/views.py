from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from api.models import Story
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

@csrf_exempt
def login(request):

    # Get request body
    request_dict = request.body.decode('utf-8')
    body = json.loads(request_dict)

    # Authenticate user
    user = authenticate(request, username=body["username"], password=body["password"])

    if user is not None:
        request.session["login_status"] = "logged_in"

        return JsonResponse({"status": 200, "message": "Welcome!"})

    return JsonResponse({"status": 200, "session": "Incorrect username or password"})

@csrf_exempt
def logout(request):

    try:
        session = request.session["login_status"]

        if session == "logged_in":
            request.session["login_status"] = "logged_out"
            return JsonResponse({"status": 200, "message": "User logged out"})
    except KeyError:
        return JsonResponse({"status": 401, "message": "User not logged in"})
    
    return JsonResponse({"status": 401, "message": "User not logged in"})

@csrf_exempt
def stories(request):
    if request.method == "GET":
        return get_story(request)
    
    if request.method == "POST":
        return post_story(request)

def post_story(request):

    try:
        session = request.session["login_status"]

        if session == "logged_in":
            return HttpResponse("logged in")
    except KeyError:
        return JsonResponse({"status": 401, "message": "User not logged in"})
    
    return HttpResponse("Post story not implemented")

def get_story(request):

    # Get request body
    request_dict = request.body.decode('utf-8')
    body = json.loads(request_dict)

    # Filter stories by request specified params
    response = Story.objects

    if body["story_cat"] == "*":
        response = response.all()
    else:
        response = response.filter(category=body["story_cat"])
    
    if body["story_region"] == "*":
        response = response.all()
    else:  
        response = response.filter(region=body["story_region"])
    
    if body["story_date"] == "*":
        response = response.all()
    else:
        response = response.filter(date=body["story_date"])

    return JsonResponse({"status": 200, "stories": list(response.values())})

def delete_story(request, id):

    if request.method != "DELETE":
        return JsonResponse({"status": 400, "message": "Invalid request method"})

    return HttpResponse("Delete story not implemented")

