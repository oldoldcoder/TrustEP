from django.urls import path
from .views import evaluate_trust

urlpatterns = [
    path('evaluate/scores', evaluate_trust),
]
