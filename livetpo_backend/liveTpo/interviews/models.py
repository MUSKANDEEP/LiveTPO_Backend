from django.db import models
from students.models import Student

class Interview(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="interviews")
    company = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected')
    ], default="Scheduled")
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "interview_schedules"

    def __str__(self):
        return f"{self.student.username} - {self.company}"
