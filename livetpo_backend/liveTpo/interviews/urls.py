from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.get_all_interviews, name="get_all_interviews"),
    path('create/', views.create_interview, name="create_interview"),
    path('update/<int:pk>/', views.update_interview, name="update_interview"),
    path('delete/<int:pk>/', views.delete_interview, name="delete_interview"),
]

