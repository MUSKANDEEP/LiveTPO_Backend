from django.urls import path
from . import views

urlpatterns = [
    path('drives/', views.get_all_placement_drives, name="get_all_drives"),
    path('drives/create/', views.create_placement_drive, name="create_drive"),
    path('drives/delete/<int:pk>/', views.delete_placement_drive, name="delete_drive"),
    path('drives/update/<int:pk>/', views.update_placement_drive, name="update_drive"),
    path('admin/dashboard-stats/', views.admin_dashboard_stats, name='admin-dashboard-stats'),
]
