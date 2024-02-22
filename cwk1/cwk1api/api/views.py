from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from api.models import Story
from datetime import date
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

@csrf_exempt
def login(request):

    # Get request body
    username = request.POST["username"]
    password = request.POST["password"]


    # Authenticate user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        request.session["login_status"] = "logged_in"
        request.session["username"] = password

        return JsonResponse({"status": 200, "message": "Welcome!"})

    return JsonResponse({"status": 200, "session": "Incorrect username or password"})

@csrf_exempt
def logout(request):

    try:
        session = request.session["login_status"]

        if session == "logged_in":
            request.session["login_status"] = "logged_out"
            request.session["username"] = ""

            return JsonResponse({"status": 200, "message": "User logged out"})
    except KeyError:
        return JsonResponse({"status": 401, "message": "User not logged in"})
    
    return JsonResponse({"status": 401, "message": "User not logged in"})

@csrf_exempt
def stories(request):
    # if request.method == "GET":
    #     return get_story(request)
    
    return get_story(request)

    # if request.method == "POST":
    #     return post_story(request)

def post_story(request):

    try:
        session = request.session["login_status"]

        if session != "logged_in":
            return JsonResponse({"status": 503, "message": "Service unavailable, user not logged in"})
    except KeyError:
        return JsonResponse({"status": 503, "message": "Service unavailable, user not logged in"})
    
    request_dict = request.body.decode('utf-8')
    body = json.loads(request_dict)

    headline = body["headline"]
    category = body["category"]
    region = body["region"]
    details = body["details"]
    date_today = date.today()
    author = User.objects.get(username=request.session["username"])

    if headline == "" or category == "" or region == "" or details == "":
        return JsonResponse({"status": 503, "message": "Service unavailable, empty fields detected"})

    if category != "pol" and category != "art" and category != "tech" and category != "trivia":
        return JsonResponse({"status": 503, "message": "Service unavailable, invalid category"})
    
    if region != "uk" and region != "eu" and region != "w":
        return JsonResponse({"status": 503, "message": "Service unavailable, invalid region"})
    


    story = Story(headline=headline, category=category, region=region, details=details, date=date_today, author=author)

    story.save()

    return JsonResponse({"status": 201, "message": "CREATED"})

def get_story(request):

    # Get request data
    category = request.POST["story_cat"]
    region = request.POST["story_region"]
    date = request.POST["story_date"]

    # Filter stories by request specified params
    response = Story.objects

    if category == "*":
        response = response.all()
    else:
        response = response.filter(category=category)
    
    if region == "*":
        response = response.all()
    else:  
        response = response.filter(region=region)
    
    if date == "*":
        response = response.all()
    else:
        response = response.filter(date=date)

    return JsonResponse({"status": 200, "stories": list(response.values()), "story_cat": category, "story_region": region, "story_date": date})
    # return HttpResponse(request.encoding)

def delete_story(request, id):

    if request.method != "DELETE":
        return JsonResponse({"status": 503, "message": "Service unavailable, Invalid method"})

    item = Story.objects.get(id=id)

    if item is not None:
        item.delete()
        return JsonResponse({"status": 200, "message": "OK"})

    return JsonResponse({"status": 503, "message": "Service unavailable, Invalid method"})

