from django.urls import path
from .views import (
    student_register,
    student_login,
    student_details,
    update_student,
    delete_student,
    list_students,
    student_placement_status,
)

urlpatterns = [
    path('student-register/', student_register, name='student_register'),
    path('student-login/', student_login, name='student_login'),
    path('student-details/<int:student_id>/', student_details, name='student_details'),  # Read (Fetch Student)
    path('update-student/<int:student_id>/', update_student, name='update_student'),  # Update (Edit Student)
    path('delete-student/<int:student_id>/', delete_student, name='delete_student'),  # Delete Student
    path('list-students/', list_students, name='list_students'),  # List all students (Admin access)
    path('student-placement-status/<int:student_id>/', student_placement_status, name='student_placement_status'),
]
