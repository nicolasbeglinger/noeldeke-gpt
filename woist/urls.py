from django.urls import path
from .views import get_json_data, update_json_data

urlpatterns = [
    path('get-woist-data/', get_json_data, name='get_woist_data'),
    path('update-woist-data/', update_json_data, name='update_woist_data'),
]
