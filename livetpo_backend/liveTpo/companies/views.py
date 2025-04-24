from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Company
from .serializers import CompanySerializer

# CREATE
@csrf_exempt
@api_view(["POST"])
def create_company(request):
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        company = serializer.save()
        return JsonResponse({"message": "Company created successfully", "company": serializer.data}, status=201)
    return JsonResponse({"error": "Invalid data", "details": serializer.errors}, status=400)

# FULL UPDATE (PUT)
@csrf_exempt
@api_view(["PUT"])
def update_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found"}, status=404)

    serializer = CompanySerializer(company, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Company updated successfully", "company": serializer.data})
    return JsonResponse({"error": "Invalid data", "details": serializer.errors}, status=400)

# PARTIAL UPDATE (PATCH)
@csrf_exempt
@api_view(["PATCH"])
def partial_update_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found"}, status=404)

    serializer = CompanySerializer(company, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Company partially updated", "company": serializer.data})
    return JsonResponse({"error": "Invalid data", "details": serializer.errors}, status=400)

# GET SINGLE COMPANY
@api_view(["GET"])
def get_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
        serializer = CompanySerializer(company)
        return JsonResponse({"company": serializer.data}, status=200)
    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found"}, status=404)

# DELETE COMPANY
@csrf_exempt
@api_view(["DELETE"])
def delete_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
        company.delete()
        return JsonResponse({"message": "Company deleted"}, status=200)
    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found"}, status=404)

# LIST COMPANIES
@api_view(["GET"])
def list_companies(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return JsonResponse({"companies": serializer.data}, status=200)
