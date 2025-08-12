# attendance/models.py
from django.db import models
from core.models import CustomUser
from courses.models import Subject, SessionYear

class Attendance(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    session_year_id = models.ForeignKey(SessionYear, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_id.subject_name} on {self.attendance_date}"

class AttendanceReport(models.Model):
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report for {self.student_id.username} on {self.attendance_id.attendance_date}"