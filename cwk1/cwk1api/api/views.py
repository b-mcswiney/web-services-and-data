from django.shortcuts import HttpResponse
from django.http import JsonResponse
from api.models import Story
import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

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
