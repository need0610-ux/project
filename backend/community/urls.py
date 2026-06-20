from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list_create),
    path('<int:post_id>/', views.post_detail_update_delete),
    path('<int:post_id>/comments/', views.comment_create),
    path('comments/<int:comment_id>/', views.comment_delete),
]