from django.urls import path
from . import views

urlpatterns = [
    path("stories", views.get_story, name="get_story"),
]