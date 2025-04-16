from django.db import models
from students.models import Student  # Correct import path based on your shared model

class PlacementDrive(models.Model):
    company = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    eligibility_criteria = models.TextField(blank=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "placement_drives"

    def __str__(self):
        return f"{self.company} - {self.job_role}"

