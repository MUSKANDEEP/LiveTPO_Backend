from django.urls import path
from .views import student_register, verify_email

urlpatterns = [
    path('student-register/', student_register, name='student_register'),
    path('register/<uuid:token>/', student_register, name='student_register'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
]
