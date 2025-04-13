from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from .models import Student
from rest_framework_simplejwt.tokens import RefreshToken
import json

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@csrf_exempt
def student_register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Check required fields
            required_fields = ['username', 'email', 'phone', 'course', 'cgpa', 'password']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"error": f"Missing required field: {field}"}, status=400)
            
            # Validate email format
            try:
                validate_email(data['email'])
            except ValidationError:
                return JsonResponse({"error": "Invalid email format"}, status=400)
            
            # Check if email or phone already exists
            if Student.objects.filter(email=data['email']).exists():
                return JsonResponse({"error": "Email already registered"}, status=400)
            if Student.objects.filter(phone=data['phone']).exists():
                return JsonResponse({"error": "Phone number already registered"}, status=400)
            
            # Validate CGPA
            try:
                cgpa = Decimal(data['cgpa'])
                if not (0 <= cgpa <= 10):
                    return JsonResponse({"error": "CGPA must be between 0 and 10"}, status=400)
            except (ValueError, TypeError, InvalidOperation):
                return JsonResponse({"error": "Invalid CGPA format"}, status=400)
            
            # Create student
            student = Student.objects.create(
                username=data['username'],
                email=data['email'],
                phone=data['phone'],
                course=data['course'],
                cgpa=cgpa,
                password=make_password(data['password']),
                is_verified=False
            )
            
            tokens = get_tokens_for_user(student)

            return JsonResponse({
                "message": "Student registered successfully! Please verify your email.",
                "student_id": student.id,
                "token": tokens
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def student_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({"error": "Email and password are required"}, status=400)

            try:
                student = Student.objects.get(email=email)
            except Student.DoesNotExist:
                return JsonResponse({"error": "Invalid email or password"}, status=401)

            if not check_password(password, student.password):
                return JsonResponse({"error": "Invalid email or password"}, status=401)

            tokens = get_tokens_for_user(student)

            # Student data to return
            student_data = {
                "id": student.id,
                "username": student.username,
                "email": student.email,
                "phone": student.phone,
                "course": student.course,
                "cgpa": str(student.cgpa),
                "role": "student"
            }

            return JsonResponse({
                "message": "Login successful!",
                "token": tokens,
                "user": student_data
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
