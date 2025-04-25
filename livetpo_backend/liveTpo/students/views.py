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
            required_fields = ['username', 'email', 'phone', 'course', 'cgpa', 'password', 'skills']
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

            # Validate password strength (e.g., at least 8 characters, includes numbers/special chars)
            password = data['password']
            if len(password) < 8:
                return JsonResponse({"error": "Password must be at least 8 characters long"}, status=400)

            # Validate skills (optional, but should be a list)
            if not isinstance(data['skills'], list):
                return JsonResponse({"error": "Skills must be a list of strings"}, status=400)

            # Validate resume_link (optional, but should be a valid URL)
            resume_link = data.get('resume_link', None)
            if resume_link and not isinstance(resume_link, str):
                return JsonResponse({"error": "Resume link must be a valid URL"}, status=400)

            # Create student
            student = Student.objects.create(
                username=data['username'],
                email=data['email'],
                phone=data['phone'],
                course=data['course'],
                cgpa=cgpa,
                password=make_password(data['password']),
                skills=data['skills'],
                resume_link=resume_link,  # Optional field
                is_verified=False
            )

            # Generate token
            tokens = get_tokens_for_user(student)

            return JsonResponse({
                "message": "Student registered successfully! Please verify your email.",
                "student_id": student.id,
                "token": tokens
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            # You can log the exception for better error tracking
            print(f"Error during registration: {str(e)}")
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

@csrf_exempt
def student_details(request, student_id):
    if request.method == "GET":
        try:
            student = Student.objects.get(id=student_id)
            
            # Make sure the student is authenticated, for example, by token or session
            student_data = {
                "id": student.id,
                "username": student.username,
                "email": student.email,
                "phone": student.phone,
                "course": student.course,
                "skills": student.skills,
                "resume_link": student.resume_link,
                "cgpa": str(student.cgpa),
                "role": "student"
            }
            
            return JsonResponse({
                "message": "Student details fetched successfully",
                "user": student_data
            }, status=200)
        
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def update_student(request, student_id):
    if request.method == "PATCH":
        try:
            student = Student.objects.get(id=student_id)
            
            # Check for the fields that can be updated
            data = json.loads(request.body)
            
            # Update fields
            if 'username' in data:
                student.username = data['username']
            if 'email' in data:
                student.email = data['email']
            if 'phone' in data:
                student.phone = data['phone']
            if 'course' in data:
                student.course = data['course']
            if 'cgpa' in data:
                try:
                    cgpa = Decimal(data['cgpa'])
                    if 0 <= cgpa <= 10:
                        student.cgpa = cgpa
                    else:
                        return JsonResponse({"error": "CGPA must be between 0 and 10"}, status=400)
                except (ValueError, TypeError, InvalidOperation):
                    return JsonResponse({"error": "Invalid CGPA format"}, status=400)
            
            if 'password' in data:
                student.password = make_password(data['password'])
            
            student.save()
            
            return JsonResponse({
                "message": "Student profile updated successfully",
                "user": {
                    "id": student.id,
                    "username": student.username,
                    "email": student.email,
                    "phone": student.phone,
                    "course": student.course,
                    "cgpa": str(student.cgpa),
                    "role": "student"
                }
            }, status=200)
        
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_student(request, student_id):
    if request.method == "DELETE":
        try:
            student = Student.objects.get(id=student_id)
            student.delete()

            return JsonResponse({"message": "Student deleted successfully"}, status=200)
        
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def list_students(request):
    if request.method == "GET":
        try:
            # You can add filters or pagination here if needed
            students = Student.objects.all()
            students_data = [
                {
                    "id": student.id,
                    "username": student.username,
                    "email": student.email,
                    "phone": student.phone,
                    "course": student.course,
                    "cgpa": str(student.cgpa),
                    "role": "student"
                }
                for student in students
            ]
            
            return JsonResponse({
                "message": "List of all students",
                "students": students_data
            }, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)
