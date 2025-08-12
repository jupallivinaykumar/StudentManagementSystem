# attendance/admin.py
from django.contrib import admin
from .models import Attendance, AttendanceReport # Ensure both are imported

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_id', 'session_year_id', 'attendance_date', 'created_at')
    list_filter = ('subject_id', 'session_year_id', 'attendance_date')
    search_fields = ('subject_id__subject_name', 'session_year_id__session_start_year')

@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'attendance_id', 'status', 'created_at')
    list_filter = ('status', 'attendance_id__subject_id__subject_name', 'attendance_id__session_year_id__session_start_year')
    search_fields = ('student_id__username', 'student_id__first_name', 'student_id__last_name')