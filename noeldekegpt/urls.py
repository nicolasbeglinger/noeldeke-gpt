from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('misc.urls')),
    path('', include('chat.urls')),
    path('', include('maps.urls'))
]
