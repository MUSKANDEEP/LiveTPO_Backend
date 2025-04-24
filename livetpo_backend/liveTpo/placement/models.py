from django.db import models
from students.models import Student  # Correct import path based on your shared model

class PlacementDrive(models.Model):
    company = models.CharField(max_length=100)  # Company name
    job_role = models.CharField(max_length=100)  # Job role (e.g., Software Engineer)
    location = models.CharField(max_length=100, blank=True)  # Location, optional field
    ctc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salary, optional
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salary, optional
    eligibility_criteria = models.TextField(blank=True)  # Eligibility criteria, optional
    description = models.TextField(blank=True)  # Description, optional
    date = models.DateField()  # Date for the placement drive (required)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation (auto-generated)
    status = models.CharField(
        max_length=20,
        choices=[("Upcoming", "Upcoming"), ("Ongoing", "Ongoing"), ("Past", "Past")],
        default="Upcoming"
    )  

    class Meta:
        db_table = "placement_drives"

    def __str__(self):
        return f"{self.company} - {self.job_role} ({self.status})"

