# students/admin.py
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'get_full_name', 'course_id', 'session_year_id', 'gender', 'date_of_birth')
    search_fields = ('admin__username', 'admin__first_name', 'admin__last_name', 'course_id__course_name')
    list_filter = ('course_id', 'session_year_id', 'gender')

    def get_username(self, obj):
        return obj.admin.username
    get_username.short_description = 'Username'

    def get_full_name(self, obj):
        return obj.admin.get_full_name()
    get_full_name.short_description = 'Full Name'