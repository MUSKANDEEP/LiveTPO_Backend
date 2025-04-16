from django.urls import path
from . import views

urlpatterns = [
    # Course URLs
    path('courses/', views.get_all_courses),
    path('courses/create/', views.create_course),

    # Grade URLs
    path('grades/', views.get_all_grades),
    path('grades/create/', views.create_grade),

    # Attendance URLs
    path('attendances/', views.get_all_attendances),
    path('attendances/create/', views.create_attendance),

    # Timetable URLs
    path('timetables/', views.get_all_timetables),
    path('timetables/create/', views.create_timetable),
]
