from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Student
from .forms import StudentRegistrationForm
from .utils import send_verification_email  # Ensure this function exists

def student_register(request, token):
    try:
        student = Student.objects.get(registration_token=token, is_verified=False)
    except Student.DoesNotExist:
        messages.error(request, "Invalid or expired registration link.")
        return redirect('login')

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student.username = form.cleaned_data['username']
            student.email = form.cleaned_data['email']
            student.phone = form.cleaned_data['phone']
            student.course = form.cleaned_data['course']
            student.cgpa = form.cleaned_data['cgpa']
            student.set_password(form.cleaned_data['password1'])  # Ensure 'password1' exists
            student.is_verified = True  # Mark student as verified upon registration
            student.save()

            # Send email verification (Ensure function exists in utils.py)
            send_verification_email(student)

            messages.success(request, "Check your email to verify your account.")
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form})

# 🔹 Email Verification Function
def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"http://127.0.0.1:8000/students/verify-email/{uid}/{token}/"

    email_body = render_to_string('email_verification.html', {'link': verification_link})
    send_mail('Verify Your Email', email_body, 'noreply@yourapp.com', [user.email])

# 🔹 Email Verification View
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        student = Student.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Student.DoesNotExist):
        student = None

    if student and default_token_generator.check_token(student, token):
        student.is_verified = True
        student.save()
        messages.success(request, "Your email has been verified. You can now log in.")
        return redirect('login')
    else:
        return render(request, 'email_verification_failed.html')

def student_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        student = authenticate(request, username=email, password=password)

        if student:
            if student.is_verified:
                login(request, student)
                return redirect('dashboard')
            else:
                messages.error(request, "Please verify your email first.")
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'login.html')
