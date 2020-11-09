from django.urls import path
from treasureinthecity.treasure_hunt import views

urlpatterns = [
    path("", views.error, name="error"),
    path("puzzle/<puzzle_id>", views.puzzle, name="puzzle"),
    path("answer/<puzzle_city_id>/<place_id>", views.answer, name="answer"),
    path("log", views.log_event, name="log_event"),
    path("<place_id>", views.home, name="home"),
]