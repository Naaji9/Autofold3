from django.urls import path
from .views import submit_dataset

urlpatterns = [
    path('submit-dataset/', submit_dataset),
]

