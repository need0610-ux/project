from django.urls import path
from . import views

urlpatterns = [
    path('deposits/save/', views.save_deposit_products),
    path('deposits/', views.deposit_product_list),
    path('deposits/<int:product_id>/', views.deposit_product_detail),
]