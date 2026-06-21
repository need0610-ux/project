from django.urls import path
from . import views

urlpatterns = [
    path('explain/', views.chatbot_response),
]