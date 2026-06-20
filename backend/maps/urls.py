from django.urls import path
from . import views

urlpatterns = [
    path('banks/', views.search_bank_branches),
]