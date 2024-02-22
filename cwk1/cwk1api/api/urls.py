from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("stories", views.stories, name="stories"),
    path("stories/<int:id>", views.delete_story, name="delete_story"),
]