from django.db import models
from django.utils import timezone

class Student(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, unique=True)
    course = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    skills = models.JSONField(default=list)
    resume_link = models.URLField(blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)  # Add default=timezone.now

    class Meta:
        db_table = "student_profiles"

    def __str__(self):
        return self.email
