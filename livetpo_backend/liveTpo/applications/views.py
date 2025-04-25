from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from .models import JobApplication, Student
import json

# Helper function to handle error responses
def handle_error(message, status):
    return JsonResponse({"error": message}, status=status)

@csrf_exempt
def create_job_application(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Check required fields
            required_fields = ['student_id', 'company_name', 'job_role', 'ctc', 'status']
            for field in required_fields:
                if field not in data:
                    return handle_error(f"Missing required field: {field}", 400)

            # Validate student existence
            try:
                student = Student.objects.get(id=data['student_id'])
            except Student.DoesNotExist:
                return handle_error("Student not found", 404)

            # Validate CTC (should be a number)
            try:
                ctc = Decimal(data['ctc'])
                if ctc <= 0:
                    return handle_error("CTC must be a positive number", 400)
            except (ValueError, TypeError, InvalidOperation):
                return handle_error("Invalid CTC format", 400)

            # Create job application
            job_application = JobApplication.objects.create(
                student=student,
                company_name=data['company_name'],
                job_role=data['job_role'],
                ctc=ctc,
                status=data['status'],
                resume_link=data.get('resume_link', None),
                cover_letter=data.get('cover_letter', None)
            )

            # Return success response
            return JsonResponse({
                "message": "Job application created successfully",
                "application_id": job_application.id
            }, status=201)

        except json.JSONDecodeError:
            return handle_error("Invalid JSON data", 400)
        except Exception as e:
            return handle_error(str(e), 400)

    return handle_error("Invalid request method", 405)


@csrf_exempt
def get_job_application(request, application_id):
    if request.method == "GET":
        try:
            application = JobApplication.objects.get(id=application_id)
            application_data = {
                "id": application.id,
                "student_id": application.student.id,
                "company_name": application.company_name,
                "job_role": application.job_role,
                "ctc": str(application.ctc),
                "status": application.status,
                "resume_link": application.resume_link,
                "cover_letter": application.cover_letter,
                "applied_on": application.applied_on,
            }

            return JsonResponse({
                "message": "Job application details fetched successfully",
                "application": application_data
            }, status=200)

        except JobApplication.DoesNotExist:
            return handle_error("Job application not found", 404)
        except Exception as e:
            return handle_error(str(e), 400)

    return handle_error("Invalid request method", 405)


@csrf_exempt
def update_job_application(request, application_id):
    if request.method == "PATCH":
        try:
            application = JobApplication.objects.get(id=application_id)
            data = json.loads(request.body)

            # Update fields
            if 'company_name' in data:
                application.company_name = data['company_name']
            if 'job_role' in data:
                application.job_role = data['job_role']
            if 'ctc' in data:
                try:
                    ctc = Decimal(data['ctc'])
                    if ctc <= 0:
                        return handle_error("CTC must be a positive number", 400)
                    application.ctc = ctc
                except (ValueError, TypeError, InvalidOperation):
                    return handle_error("Invalid CTC format", 400)
            if 'status' in data:
                application.status = data['status']
            if 'resume_link' in data:
                application.resume_link = data['resume_link']
            if 'cover_letter' in data:
                application.cover_letter = data['cover_letter']

            application.save()

            # Return success response
            return JsonResponse({
                "message": "Job application updated successfully",
                "application": {
                    "id": application.id,
                    "student_id": application.student.id,
                    "company_name": application.company_name,
                    "job_role": application.job_role,
                    "ctc": str(application.ctc),
                    "status": application.status,
                    "resume_link": application.resume_link,
                    "cover_letter": application.cover_letter,
                    "applied_on": application.applied_on,
                }
            }, status=200)

        except JobApplication.DoesNotExist:
            return handle_error("Job application not found", 404)
        except json.JSONDecodeError:
            return handle_error("Invalid JSON data", 400)
        except Exception as e:
            return handle_error(str(e), 400)

    return handle_error("Invalid request method", 405)


@csrf_exempt
def delete_job_application(request, application_id):
    if request.method == "DELETE":
        try:
            application = JobApplication.objects.get(id=application_id)
            application.delete()

            return JsonResponse({"message": "Job application deleted successfully"}, status=200)

        except JobApplication.DoesNotExist:
            return handle_error("Job application not found", 404)
        except Exception as e:
            return handle_error(str(e), 400)

    return handle_error("Invalid request method", 405)


@csrf_exempt
def list_job_applications(request):
    if request.method == "GET":
        try:
            applications = JobApplication.objects.all()
            applications_data = [
                {
                    "id": application.id,
                    "student_id": application.student.id,
                    "company_name": application.company_name,
                    "job_role": application.job_role,
                    "ctc": str(application.ctc),
                    "status": application.status,
                    "resume_link": application.resume_link,
                    "cover_letter": application.cover_letter,
                    "applied_on": application.applied_on,
                }
                for application in applications
            ]

            return JsonResponse({
                "message": "List of all job applications",
                "applications": applications_data
            }, status=200)

        except Exception as e:
            return handle_error(str(e), 400)

    return handle_error("Invalid request method", 405)
