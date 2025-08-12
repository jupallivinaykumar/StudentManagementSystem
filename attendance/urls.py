# attendance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_attendance, name='manage_attendance'),
    path('add/', views.add_attendance, name='add_attendance'), # This is the staff's "Take Attendance" view
    path('reports/', views.view_attendance_reports, name='view_attendance_reports'),
    # You might need specific URLs for editing attendance later (e.g., /edit/<int:attendance_id>/)
]