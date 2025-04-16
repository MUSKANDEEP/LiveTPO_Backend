from django.contrib import admin
from .models import PlacementDrive

@admin.register(PlacementDrive)
class PlacementDriveAdmin(admin.ModelAdmin):
    list_display = ('company', 'job_role', 'date', 'location', 'salary')
    search_fields = ('company', 'job_role')
    list_filter = ('company', 'date')
