from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    job_roles = models.JSONField(default=list)  # For storing multiple job roles
    ctc = models.CharField(max_length=255, blank=True, null=True)  # Expected format: "₹12 LPA"
    eligibility_cgpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    eligibility_skills = models.JSONField(default=list)  # For storing multiple skills
    mode_of_work = models.CharField(max_length=50, choices=[("remote", "Remote"), ("onsite", "Onsite"), ("hybrid", "Hybrid")], default="remote")
    bond = models.TextField(blank=True, null=True)
    selection_process = models.TextField(blank=True, null=True)
    openings = models.PositiveIntegerField(default=0)
    perks = models.TextField(blank=True, null=True)
    pdfs = models.FileField(upload_to="company_pdfs/", null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=[("full-time", "Full-time"), ("part-time", "Part-time"), ("internship", "Internship"), ("contract", "Contract")], default="full-time")
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    website_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "company_profiles"

    def __str__(self):
        return self.name
