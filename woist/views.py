import json
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# File path to your JSON file
json_file_path = os.path.join(settings.BASE_DIR, 'woist', 'data',  'woist.json')

def get_json_data(request):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return JsonResponse(data, safe=False)

@csrf_exempt
def update_json_data(request):
    if request.method == 'PUT':
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)

            with open(json_file_path, 'w') as file:
                json.dump(data, file, indent=2)

            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponse(status=500, content=f"Error: {str(e)}")
    return HttpResponse(status=405)  # Method not allowed
