from django.urls import path,include
from .views import addLeave


urlpatterns = [
    path('leave/', addLeave),
    
]