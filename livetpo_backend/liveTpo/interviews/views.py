from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Interview
from .serializers import InterviewSerializer

@api_view(['GET'])
def get_all_interviews(request):
    interviews = Interview.objects.all()
    serializer = InterviewSerializer(interviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_interview(request):
    serializer = InterviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_interview(request, pk):
    try:
        interview = Interview.objects.get(pk=pk)
    except Interview.DoesNotExist:
        return Response({"error": "Interview not found"}, status=404)

    serializer = InterviewSerializer(interview, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_interview(request, pk):
    try:
        interview = Interview.objects.get(pk=pk)
        interview.delete()
        return Response({"message": "Interview deleted"}, status=204)
    except Interview.DoesNotExist:
        return Response({"error": "Interview not found"}, status=404)
