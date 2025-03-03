from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, unique=True)
    course = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    password = models.CharField(max_length=255)  # Hashed password
    is_verified = models.BooleanField(default=False)  # Email verification status
    verification_token = models.CharField(max_length=255, blank=True, null=True)  # Token for email verification

    def __str__(self):
        return self.email
