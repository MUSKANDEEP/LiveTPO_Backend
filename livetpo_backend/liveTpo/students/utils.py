from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(student):
    subject = "Verify Your Email"
    message = f"""
    Hi {student.username},

    Please click the link below to verify your email and activate your account:
    http://yourdomain.com/verify-email/{student.id}/{student.registration_token}/

    If you did not sign up, please ignore this email.

    Thanks,
    The Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student.email])
