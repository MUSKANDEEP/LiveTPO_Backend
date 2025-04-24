from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PlacementDrive
from .serializers import PlacementDriveSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from students.models import Student
from companies.models import Company
from placement.models import PlacementDrive  # Adjust if app/model name is different
from datetime import date

@api_view(["GET"])
def get_all_placement_drives(request):
    drives = PlacementDrive.objects.all().order_by("-date")
    serializer = PlacementDriveSerializer(drives, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_placement_drive(request):
    serializer = PlacementDriveSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def delete_placement_drive(request, pk):
    try:
        drive = PlacementDrive.objects.get(pk=pk)
        drive.delete()
        return Response({"message": "Drive deleted successfully"}, status=status.HTTP_200_OK)
    except PlacementDrive.DoesNotExist:
        return Response({"error": "Drive not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
def update_placement_drive(request, pk):
    try:
        drive = PlacementDrive.objects.get(pk=pk)
    except PlacementDrive.DoesNotExist:
        return Response({"error": "Drive not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PlacementDriveSerializer(drive, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_stats(request):
    total_students = Student.objects.count()
    total_companies = Company.objects.count()
    upcoming_drives = PlacementDrive.objects.filter(status="Upcoming", date__gte=date.today()).count()
    # total_applications = Application.objects.count()

    return Response({
        "total_students": total_students,
        "total_companies": total_companies,
        "upcoming_drives": upcoming_drives,
        # "total_applications": total_applications,
    })