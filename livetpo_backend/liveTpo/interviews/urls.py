from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_interviews),
    path('create/', views.create_interview),
    path('update/<int:pk>/', views.update_interview),
    path('delete/<int:pk>/', views.delete_interview),
]
