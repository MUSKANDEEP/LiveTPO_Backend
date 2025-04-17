from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Grade, Attendance, Timetable
from .serializers import CourseSerializer, GradeSerializer, AttendanceSerializer, TimetableSerializer

# --- Course Views ---

@api_view(['GET'])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(course)
    return Response(serializer.data)

@api_view(['PUT'])
def update_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CourseSerializer(course, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    
    course.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# --- Grade Views ---

@api_view(['GET'])
def get_all_grades(request):
    grades = Grade.objects.all()
    serializer = GradeSerializer(grades, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_grade(request):
    serializer = GradeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_grade(request, pk):
    try:
        grade = Grade.objects.get(pk=pk)
    except Grade.DoesNotExist:
        return Response({"error": "Grade not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = GradeSerializer(grade)
    return Response(serializer.data)

@api_view(['PUT'])
def update_grade(request, pk):
    try:
        grade = Grade.objects.get(pk=pk)
    except Grade.DoesNotExist:
        return Response({"error": "Grade not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = GradeSerializer(grade, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_grade(request, pk):
    try:
        grade = Grade.objects.get(pk=pk)
    except Grade.DoesNotExist:
        return Response({"error": "Grade not found"}, status=status.HTTP_404_NOT_FOUND)
    
    grade.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# --- Attendance Views ---

@api_view(['GET'])
def get_all_attendances(request):
    attendances = Attendance.objects.all()
    serializer = AttendanceSerializer(attendances, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_attendance(request):
    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_attendance(request, pk):
    try:
        attendance = Attendance.objects.get(pk=pk)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = AttendanceSerializer(attendance)
    return Response(serializer.data)

@api_view(['PUT'])
def update_attendance(request, pk):
    try:
        attendance = Attendance.objects.get(pk=pk)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AttendanceSerializer(attendance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_attendance(request, pk):
    try:
        attendance = Attendance.objects.get(pk=pk)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)
    
    attendance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# --- Timetable Views ---

@api_view(['GET'])
def get_all_timetables(request):
    timetables = Timetable.objects.all()
    serializer = TimetableSerializer(timetables, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_timetable(request):
    serializer = TimetableSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_timetable(request, pk):
    try:
        timetable = Timetable.objects.get(pk=pk)
    except Timetable.DoesNotExist:
        return Response({"error": "Timetable not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = TimetableSerializer(timetable)
    return Response(serializer.data)

@api_view(['PUT'])
def update_timetable(request, pk):
    try:
        timetable = Timetable.objects.get(pk=pk)
    except Timetable.DoesNotExist:
        return Response({"error": "Timetable not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TimetableSerializer(timetable, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_timetable(request, pk):
    try:
        timetable = Timetable.objects.get(pk=pk)
    except Timetable.DoesNotExist:
        return Response({"error": "Timetable not found"}, status=status.HTTP_404_NOT_FOUND)
    
    timetable.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
