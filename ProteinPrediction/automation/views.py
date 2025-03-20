from django.shortcuts import render
import os
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .automation_script import automate_prediction  # Our Selenium script

@api_view(['POST'])
def submit_dataset(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    file = request.FILES.get('file')

    if not all([email, password, file]):
        return JsonResponse({'error': 'All fields are required'}, status=400)

    # Save the uploaded file temporarily
    file_path = f'/tmp/{file.name}'
    with open(file_path, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    # Run the automation script with provided credentials
    automate_prediction(email, password, file_path)

    # Clean up uploaded file
    os.remove(file_path)
    return JsonResponse({'message': 'Automation process completed!'})

