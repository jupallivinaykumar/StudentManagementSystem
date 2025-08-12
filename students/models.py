# students/models.py
from django.db import models
from core.models import CustomUser
# Use string references for cross-app ForeignKeys to avoid circular imports
# NO: from courses.models import Course, SessionYear

class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100)
    address = models.TextField()
    course_id = models.ForeignKey('courses.Course', on_delete=models.DO_NOTHING, null=True, blank=True)
    session_year_id = models.ForeignKey('courses.SessionYear', on_delete=models.DO_NOTHING, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Fallback to username if first/last name are not set
        return f"{self.admin.first_name} {self.admin.last_name}" if self.admin.first_name and self.admin.last_name else self.admin.username