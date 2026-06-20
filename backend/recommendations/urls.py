from django.urls import path
from . import views

urlpatterns = [
    path('main-bank/', views.main_bank_recommendation),
    path('history/', views.my_recommendation_history),
]