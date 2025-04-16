from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PlacementDrive
from .serializers import PlacementDriveSerializer

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
