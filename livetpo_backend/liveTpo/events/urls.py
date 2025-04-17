from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_events, name="get_all_events"),  # GET all events
    path('create/', views.create_event, name="create_event"),  # POST to create event
    path('update/<int:pk>/', views.update_event, name="update_event"),  # PUT to update
    path('delete/<int:pk>/', views.delete_event, name="delete_event"),  # DELETE event
]
