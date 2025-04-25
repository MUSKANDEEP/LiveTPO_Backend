from django.db import models
from django.utils import timezone
from students.models import Student  # Correctly import the Student model

class JobApplication(models.Model):
    # Correctly reference the Student model
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    
    # Company and job details
    company_name = models.CharField(max_length=255)
    job_role = models.CharField(max_length=255)
    ctc = models.DecimalField(max_digits=10, decimal_places=2)  # CTC in LPA or other currency units
    
    # Timestamp of when application was created
    applied_on = models.DateTimeField(auto_now_add=True)  # Removed default=timezone.now
    
    # Status of the application (e.g., applied, interview, hired, rejected)
    status = models.CharField(
        max_length=50,
        choices=[
            ('applied', 'Applied'),
            ('interview', 'Interview Scheduled'),
            ('hired', 'Hired'),
            ('rejected', 'Rejected')
        ],
        default='applied'
    )
    
    # Additional fields for student's resume and cover letter
    resume_link = models.URLField(blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "job_applications"  # Table name in the database

    def __str__(self):
        # String representation of the Job Application
        return f"{self.student.username} - {self.company_name} - {self.job_role}"
