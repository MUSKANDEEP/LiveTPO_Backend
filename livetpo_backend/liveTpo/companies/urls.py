from django.urls import path
from . import views

urlpatterns = [
    path('companiesData/', views.list_companies, name='list_companies'),  # List all companies
    path('<int:company_id>/', views.get_company, name='get_company'),  # Get company details
    path('manage/', views.create_company, name='create_company'),  # Add a new company or update
    path('manage/<int:company_id>/', views.update_company, name='update_company_with_id'),  # Update company
    path('manage/<int:company_id>/', views.partial_update_company, name='update_company_with_id'),  # Update company
    path('delete/<int:company_id>/', views.delete_company, name='delete_company'),  # Delete company
]
