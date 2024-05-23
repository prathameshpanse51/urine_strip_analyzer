import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.shortcuts import render

def index(request):
    return render(request, 'analyzer/index.html')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image_file = request.FILES['image']
        file_path = default_storage.save('temp.jpg', image_file)
        image_path = default_storage.path(file_path)

        # Process the image with OpenCV
        result = analyze_image(image_path)

        return JsonResponse(result)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def analyze_image(image_path):
    image = cv2.imread(image_path)

    # Placeholder for actual image processing logic
    colors = []
    for i in range(10):
        x, y, w, h = 10, 10 + i*20, 20, 20  # Example coordinates
        region = image[y:y+h, x:x+w]
        average_color = cv2.mean(region)[:3]
        colors.append(tuple(map(int, average_color)))

    # Define the keys for the tests
    keys = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']

    # Map the colors to the corresponding keys
    result = {key: color for key, color in zip(keys, colors)}

    return result
