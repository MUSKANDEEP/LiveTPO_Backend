from django.urls import path
from .views import student_register, student_login

urlpatterns = [
    path('student-register/', student_register, name='student_register'),
    path('student-login/', student_login, name='student_login'),
    # path('register/<uuid:token>/', student_register, name='student_register'),
    # path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),
]
