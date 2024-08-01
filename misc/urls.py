from django.urls import path
from . import views

urlpatterns = [
    path("", views.starting_page, name="starting_page"),
    path("daily_fundorte", views.daily_fundorte, name="daily_fundorte"),
    path("milchkalender", views.milchkalender, name="milchkalender")
]