from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_events),  # GET all events
    path('create/', views.create_event),  # POST to create event
    path('update/<int:pk>/', views.update_event),  # PUT to update event by ID
    path('delete/<int:pk>/', views.delete_event),  # DELETE event by ID
]
