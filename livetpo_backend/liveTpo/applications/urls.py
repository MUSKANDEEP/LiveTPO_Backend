from django.urls import path
from . import views

urlpatterns = [
    path('job-applications/', views.list_job_applications, name='job_application_list'),  # List All Applications
    path('job-applications/create/', views.create_job_application, name='create_job_application'),  # Create a Job Application
    path('job-applications/<int:application_id>/', views.get_job_application, name='get_job_application'),  # Get Single Application
    path('job-applications/<int:application_id>/update/', views.update_job_application, name='update_job_application'),  # Update Job Application
    path('job-applications/<int:application_id>/delete/', views.delete_job_application, name='delete_job_application'),  # Delete Job Application
]
