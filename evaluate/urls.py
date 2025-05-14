from django.urls import path
from .views import evaluate_trust, evaluate_device

urlpatterns = [
    path('evaluate/scores', evaluate_trust),
    path('evaluate/device', evaluate_device),
]
