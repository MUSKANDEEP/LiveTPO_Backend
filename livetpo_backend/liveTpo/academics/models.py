from django.db import models
from students.models import Student  # Adjust if needed

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    credits = models.IntegerField(default=0)

    class Meta:
        db_table = "courses"

    def __str__(self):
        return self.name

# Grade Model
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades")
    grade = models.CharField(max_length=5)
    semester = models.CharField(max_length=10, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "student_grades"

    def __str__(self):
        return f"{self.student.username} - {self.course.name} ({self.grade})"

# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    class Meta:
        db_table = "attendance"

    def __str__(self):
        return f"{self.student.username} - {self.course.name} - {self.status}"

# Timetable Model (Optional)
class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="timetables")
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200)

    class Meta:
        db_table = "timetable"

    def __str__(self):
        return f"{self.course.name} - {self.day_of_week}"

