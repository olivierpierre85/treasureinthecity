from django.urls import path
from treasureinthecity.showcase import views
import django.views

urlpatterns = [
    path("favicon.ico", django.views.defaults.page_not_found),
    path("", views.index, name="index"),
    path("email", views.email, name="email"),
    path("<city>", views.city, name="city"),
]