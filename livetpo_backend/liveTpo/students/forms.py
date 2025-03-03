from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['username', 'email', 'phone', 'course', 'cgpa', 'password1', 'password2']
