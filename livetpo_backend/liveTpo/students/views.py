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
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

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
def update_student(request, student_id):
    if request.method == "PATCH":
        try:
            student = Student.objects.get(id=student_id)
            data = json.loads(request.body)

            # Simple string fields
            string_fields = [
                "username", "email", "phone", "contact", "course",
                "university", "tenth_board", "twelfth_board",
                "preferred_job_location", "preferred_company_type",
                "github_link", "linkedin_link", "portfolio_link",
                "achievements", "verification_token"
            ]
            for field in string_fields:
                if field in data:
                    setattr(student, field, data[field] or None)

            # JSON fields
            json_fields = [
                "skills", "certifications", "projects",
                "languages_known", "applied_companies"
            ]
            for field in json_fields:
                if field in data:
                    setattr(student, field, data[field] if isinstance(data[field], list) else [])

            # Boolean
            if "relocation_ready" in data:
                student.relocation_ready = data["relocation_ready"]

            # Date
            if "availability_date" in data:
                date_value = data["availability_date"]
            if date_value in [None, "", "Not provided"]:
                student.availability_date = None
            else:
                student.availability_date = date_value  # assuming it's already a valid date string

            # Year (integer)
            if "year_of_graduation" in data:
                try:
                    student.year_of_graduation = int(data["year_of_graduation"]) if data["year_of_graduation"] else None
                except ValueError:
                    student.year_of_graduation = None

            # Percentages and CGPA
            if "cgpa" in data:
                try:
                    student.cgpa = Decimal(data["cgpa"])
                except (InvalidOperation, ValueError, TypeError):
                    student.cgpa = None

            if "tenth_percentage" in data:
                try:
                    student.tenth_percentage = Decimal(data["tenth_percentage"])
                except (InvalidOperation, ValueError, TypeError):
                    student.tenth_percentage = None

            if "twelfth_percentage" in data:
                try:
                    student.twelfth_percentage = Decimal(data["twelfth_percentage"])
                except (InvalidOperation, ValueError, TypeError):
                    student.twelfth_percentage = None

            if 'image' in request.FILES:
                image = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                student.image = fs.url(filename)
                student.save()

            # Password
            if "password" in data:
                student.password = make_password(data["password"])

            student.save()

            # Prepare response
            response_data = {
                "id": student.id,
                "username": student.username,
                "email": student.email,
                "phone": student.phone,
                "contact": student.contact,
                "course": student.course,
                "image": student.image.url if student.image else None,
                "role": "student",
                "tenth_board": student.tenth_board,
                "cgpa": str(student.cgpa) if student.cgpa else None,
                "tenth_percentage": str(student.tenth_percentage) if student.tenth_percentage else None,
                "twelfth_percentage": str(student.twelfth_percentage) if student.twelfth_percentage else None,
                "university": student.university,
                "year_of_graduation": student.year_of_graduation,
                "skills": student.skills,
                "certifications": student.certifications,
                "projects": student.projects,
                "achievements": student.achievements,
                "languages_known": student.languages_known,
                "preferred_job_location": student.preferred_job_location,
                "relocation_ready": student.relocation_ready,
                "preferred_company_type": student.preferred_company_type,
                "applied_companies": student.applied_companies,
                "availability_date": student.availability_date,
                "github_link": student.github_link,
                "linkedin_link": student.linkedin_link,
                "portfolio_link": student.portfolio_link,
                "resume_link": student.resume_link,
                "verification_token": student.verification_token,
                "is_verified": student.is_verified
            }

            return JsonResponse({
                "message": "Student profile updated successfully",
                "user": response_data
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
