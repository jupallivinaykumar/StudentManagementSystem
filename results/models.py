# results/models.py
from django.db import models
from students.models import Student # Assuming you link to Student profile
from courses.models import Subject, SessionYear

class Result(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session_year_id = models.ForeignKey(SessionYear, on_delete=models.CASCADE)
    subject_marks = models.FloatField(default=0.0)
    exam_marks = models.FloatField(default=0.0) # You might have separate exam marks
    final_grade = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student_id', 'subject_id', 'session_year_id') # A student typically has one result per subject per session

    def __str__(self):
        return f"{self.student_id.admin.get_full_name()} - {self.subject_id.subject_name} ({self.session_year_id})"

