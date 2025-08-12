# courses/admin.py
from django.contrib import admin
from .models import Course, SessionYear, Subject

# Register Course
@admin.register(Course) # This is a concise way to register
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'created_at', 'updated_at')
    search_fields = ('course_name',)
    list_filter = ('created_at',)

# Register SessionYear
@admin.register(SessionYear)
class SessionYearAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_start_year', 'session_end_year', 'created_at')
    list_filter = ('session_start_year',)

# Register Subject (you'll fill this out more when you work on subjects)
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_name', 'course_id', 'staff_id')
    search_fields = ('subject_name', 'course_id__course_name') # Search by subject name or course name
    list_filter = ('course_id', 'staff_id') # Filter by course or assigned staff