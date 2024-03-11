import json
from datetime import date

from api.models import Story
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


@csrf_exempt
def login(request):
    # Get request body
    try:
        username = request.POST["username"]
        password = request.POST["password"]
    except KeyError:
        return JsonResponse({"message": "Service unavailable, invalid request"}, status=503)

    # Authenticate user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        request.session["login_status"] = "logged_in"
        request.session["username"] = username

        request.session.save()

        return JsonResponse({"message": "Welcome!"}, status=200)

    return JsonResponse({"message": "Incorrect username or password"}, status=503)


@csrf_exempt
def logout(request):
    try:
        session = request.session["login_status"]

        if session == "logged_in":
            request.session["login_status"] = "logged_out"
            request.session["username"] = ""

            return JsonResponse({"message": "User logged out"}, status=200)
    except KeyError:
        return JsonResponse({"message": "User not logged in, key error detected"}, status=503)

    return JsonResponse({"message": "User not logged in"}, status=503)


@csrf_exempt
def stories(request):
    if request.method == "GET":
        return get_story(request)

    if request.method == "POST":
        return post_story(request)


def post_story(request):
    try:
        session = request.session["login_status"]

        if session != "logged_in":
            return JsonResponse({"message": "Service unavailable, user not logged in"}, status=503)
    except KeyError:
        return JsonResponse({"message": "Service unavailable, user not logged in"}, status=503)

    request_dict = request.body.decode('utf-8')
    body = json.loads(request_dict)

    headline = body["headline"]
    category = body["category"]
    region = body["region"]
    details = body["details"]
    date_today = date.today()
    author = User.objects.get(username=request.session["username"])

    if headline == "" or category == "" or region == "" or details == "":
        return JsonResponse({"message": "Service unavailable, empty fields detected"}, status=503)

    if category != "pol" and category != "art" and category != "tech" and category != "trivia":
        return JsonResponse({"message": "Service unavailable, invalid category"}, status=503)

    if region != "uk" and region != "eu" and region != "w":
        return JsonResponse({"message": "Service unavailable, invalid region"}, status=503)

    story = Story(headline=headline, category=category, region=region, details=details, date=date_today, author=author)

    story.save()

    return JsonResponse({"message": "CREATED"}, status=200)


def get_story(request):
    # Get request data

    try:
        category = request.GET["story_cat"]
        region = request.GET["story_region"]
        date = request.GET["story_date"]
    except KeyError:
        return JsonResponse({"message": "Service unavailable, invalid request"}, status=503)

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

    response = response.values()

    output = []

    for story in response:
        story_dict = {}

        # get the author of current story
        author = User.objects.get(id=story["author_id"])

        # Build output dictionary for the story
        story_dict["key"] = story["id"]
        story_dict["headline"] = story["headline"]
        story_dict["story_cat"] = story["category"]
        story_dict["story_region"] = story["region"]
        story_dict["author"] = author.username
        story_dict["story_date"] = story["date"]
        story_dict["story_details"] = story["details"]

        output.append(story_dict)

    return JsonResponse({"stories": output}, status=200)


@csrf_exempt
def delete_story(request, id):
    if request.method != "DELETE":
        return JsonResponse({"message": "Service unavailable, Invalid method"}, status=503)

    try:
        session = request.session["login_status"]

        if session != "logged_in":
            return JsonResponse({"message": "Service unavailable, user not logged in"}, status=503)
    except KeyError:
        return JsonResponse({"message": "Service unavailable, user not logged in"}, status=503)

    try:
        item = Story.objects.get(id=id)
    except Story.DoesNotExist:
        return JsonResponse({"message": "Service unavailable, story not found"}, status=503)

    item.delete()
    return JsonResponse({"message": "OK"}, status=200)
