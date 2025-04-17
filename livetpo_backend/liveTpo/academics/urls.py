from django.urls import path
from . import views

urlpatterns = [
    # Course URLs
    path('courses/', views.get_all_courses),
    path('courses/create/', views.create_course),
    path('courses/update/<int:pk>/', views.update_course),
    path('courses/delete/<int:pk>/', views.delete_course),

    # Grade URLs
    path('grades/', views.get_all_grades),
    path('grades/create/', views.create_grade),
    path('grades/update/<int:pk>/', views.update_grade),
    path('grades/delete/<int:pk>/', views.delete_grade),

    # Attendance URLs
    path('attendances/', views.get_all_attendances),
    path('attendances/create/', views.create_attendance),
    path('attendances/update/<int:pk>/', views.update_attendance),
    path('attendances/delete/<int:pk>/', views.delete_attendance),

    # Timetable URLs
    path('timetables/', views.get_all_timetables),
    path('timetables/create/', views.create_timetable),
    path('timetables/update/<int:pk>/', views.update_timetable),
    path('timetables/delete/<int:pk>/', views.delete_timetable),
]
