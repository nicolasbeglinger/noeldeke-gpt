from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('chat', views.chat, name='chat'),
    path("daily_fundorte", views.daily_fundorte, name="daily_fundorte"),
    path("milchkalender", views.milchkalender, name="milchkalender")
]
