from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from api.models import Story
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

def login(request):

    # Get request body
    request_dict = request.body.decode('utf-8')
    body = json.loads(request_dict)

    # Check if user exists
    user = settings.AUTH_USER_MODEL.objects.filter(username=body["username"], password=body["password"])

    if user is not None:
        request.session["login_status"] = "logged_in"
        session = request.session.items()
        return JsonResponse({"status": 200, "session": list(session)})

    return JsonResponse({"status": 200, "session": "did not work"})

def logout(request):
    return HttpResponse("Logout not implemented")

def post_story(request):
    return HttpResponse("Post story not implemented")

def get_story(request):

    # Get request body
    request_dict = request.body.decode('utf-8')
    body = json.loads(request_dict)

    # Get all stories
    # all_stories = Story.objects.all()

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

    if request.method == "DELETE":
        return HttpResponse("Delete story not implemented")

    return JsonResponse({"status": 400, "message": "Invalid request method"})
