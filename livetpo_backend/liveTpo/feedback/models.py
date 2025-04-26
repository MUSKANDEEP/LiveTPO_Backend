from django.db import models
from students.models import Student

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    message = models.TextField()
    rating = models.PositiveIntegerField(null=True, blank=True)  # Rating 1 to 5, optional
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "student_feedback"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Feedback from {self.student.username}"
