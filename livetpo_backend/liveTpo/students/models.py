from django.db import models

class Student(models.Model):
    # Basic Info
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # contact = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, unique=True)
    course = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)

    # Education History
    tenth_board = models.CharField(max_length=100, blank=True, null=True)
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    twelfth_board = models.CharField(max_length=100, blank=True, null=True)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    year_of_graduation = models.IntegerField(blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)

    # Freshers-Focused Fields
    skills = models.JSONField(default=list)
    resume_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)

    certifications = models.JSONField(default=list)
    projects = models.JSONField(default=list)
    achievements = models.TextField(blank=True, null=True)
    languages_known = models.JSONField(default=list)
    preferred_job_location = models.CharField(max_length=100, blank=True, null=True)
    relocation_ready = models.BooleanField(default=True)
    preferred_company_type = models.CharField(
        max_length=100,
        choices=[('Startup', 'Startup'), ('MNC', 'MNC'), ('Any', 'Any')],
        default='MNC'
    )

    applied_companies = models.JSONField(default=list)
    availability_date = models.DateField(blank=True, null=True)

    # New Fields for Placement
    placement_status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Placed', 'Placed')],
        default='Pending'
    )

    offers = models.JSONField(default=list)  # Array of offers with company, role, CTC, etc.
    placement_history = models.JSONField(default=list)  # Array of placement history (company, status, year)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_profiles"

    def __str__(self):
        return self.email
