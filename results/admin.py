# results/admin.py
from django.contrib import admin
from .models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'subject_id', 'session_year_id', 'subject_marks', 'exam_marks', 'final_grade', 'created_at')
    list_filter = ('session_year_id', 'subject_id', 'final_grade')
    search_fields = ('student_id__admin__username', 'student_id__admin__first_name', 'subject_id__subject_name')
    raw_id_fields = ('student_id', 'subject_id', 'session_year_id') # Useful for ForeignKey selection in admin