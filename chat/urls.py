from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tipps_tricks', views.tipps_tricks, name='tipps_tricks'),
]
