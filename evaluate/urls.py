from django.urls import path
from .views import evaluate_trust, evaluate_device, evaluate_trust_software

urlpatterns = [
    path('evaluate/user_scores', evaluate_trust),
    path('evaluate/software_scores', evaluate_trust_software),
    path('evaluate/device_scores', evaluate_device),
]
