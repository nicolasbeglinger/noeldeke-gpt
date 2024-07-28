from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.maps, name='chat'),
    path('maps', views.maps, name='maps'),
]