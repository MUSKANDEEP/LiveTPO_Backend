from django.contrib import admin
from .models import Student
from django.core.mail import send_mail

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verified')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If new student
            obj.set_password('defaultpassword123')  # Set temporary password
            obj.save()
            registration_link = f"http://127.0.0.1:8000/students/register/{obj.registration_token}/"
            send_mail('Complete Your Registration', f'Click here: {registration_link}', 'noreply@yourapp.com', [obj.email])
        else:
            super().save_model(request, obj, form, change)
