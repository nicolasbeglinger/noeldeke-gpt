from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('chat', views.chat, name='chat'),
    path('tipps_tricks', views.tipps_tricks, name='tipps_tricks'),
    path("milchkalender", views.milchkalender, name="milchkalender"),
]
