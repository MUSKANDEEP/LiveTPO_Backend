import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from .models import Student
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from .serializers import StudentSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@csrf_exempt
def student_details(request, student_id):
    if request.method == "GET":
        try:
            student = Student.objects.get(id=student_id)
            serializer = StudentSerializer(student)
            student_data = serializer.data

            return JsonResponse({
                "message": "Student details fetched successfully",
                "user": student_data
            }, status=200)
        
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Error: {str(e)}"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def student_register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            required_fields = ['username', 'email', 'phone', 'course', 'cgpa', 'password', 'skills']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"error": f"Missing required field: {field}"}, status=400)

            # Validate email format
            try:
                validate_email(data['email'])
            except ValidationError:
                return JsonResponse({"error": "Invalid email format"}, status=400)

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

            password = data['password']
            if len(password) < 8:
                return JsonResponse({"error": "Password must be at least 8 characters long"}, status=400)

            if not isinstance(data['skills'], list):
                return JsonResponse({"error": "Skills must be a list of strings"}, status=400)

            resume_link = data.get('resume_link', None)
            if resume_link and not isinstance(resume_link, str):
                return JsonResponse({"error": "Resume link must be a valid URL"}, status=400)

            student = Student.objects.create(
                username=data['username'],
                email=data['email'],
                phone=data['phone'],
                course=data['course'],
                cgpa=cgpa,
                password=make_password(data['password']),
                skills=data['skills'],
                resume_link=resume_link,
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
            print(f"Error during registration: {str(e)}")
            return JsonResponse({"error": f"Error: {str(e)}"}, status=400)

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
            return JsonResponse({"error": f"Error: {str(e)}"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def update_student(request, student_id):
    if request.method == "PATCH":
        try:
            student = Student.objects.get(id=student_id)
            data = json.loads(request.body)

            # Update basic fields
            string_fields = ["username", "email", "contact", "phone", "course", "university"]
            for field in string_fields:
                if field in data:
                    setattr(student, field, data[field] or None)

            # Update Education History
            if "tenth_board" in data:
                student.tenth_board = data["tenth_board"]
            if "twelfth_board" in data:
                student.twelfth_board = data["twelfth_board"]
            if "year_of_graduation" in data:
                student.year_of_graduation = data["year_of_graduation"]
            if "university" in data:
                student.university = data["university"]
            if "tenth_percentage" in data:
                student.tenth_percentage = data["tenth_percentage"]
            if "twelfth_percentage" in data:
                student.twelfth_percentage = data["twelfth_percentage"]

            # Update Freshers-Focused Fields
            if "skills" in data:
                student.skills = data["skills"] if isinstance(data["skills"], list) else []
            if "resume_link" in data:
                student.resume_link = data["resume_link"]
            if "github_link" in data:
                student.github_link = data["github_link"]
            if "linkedin_link" in data:
                student.linkedin_link = data["linkedin_link"]
            if "portfolio_link" in data:
                student.portfolio_link = data["portfolio_link"]
            if "certifications" in data:
                student.certifications = data["certifications"] if isinstance(data["certifications"], list) else []
            if "projects" in data:
                student.projects = data["projects"] if isinstance(data["projects"], list) else []
            if "achievements" in data:
                student.achievements = data["achievements"]
            if "languages_known" in data:
                student.languages_known = data["languages_known"] if isinstance(data["languages_known"], list) else []

            # Update Placement Fields
            if "placement_status" in data:
                student.placement_status = data["placement_status"]
            if "offers" in data:
                student.offers = data["offers"] if isinstance(data["offers"], list) else []
            if "placement_history" in data:
                student.placement_history = data["placement_history"] if isinstance(data["placement_history"], list) else []
            if "applied_companies" in data:
                student.applied_companies = data["applied_companies"] if isinstance(data["applied_companies"], list) else []
            if "availability_date" in data:
                student.availability_date = data["availability_date"]

            # Save student image if available
            if 'image' in request.FILES:
                image = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                student.image = fs.url(filename)

            # Save updated student data
            student.save()

            return JsonResponse({
                "message": "Student profile updated successfully",
                "user": StudentSerializer(student).data
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
            # Fetch all students and serialize their full details
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
                
            return JsonResponse({
            "message": "List of all students",
            "students": serializer.data
            }, status=200)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)
