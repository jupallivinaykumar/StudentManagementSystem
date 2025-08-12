# attendance/forms.py
from django import forms
from .models import Attendance, AttendanceReport
from students.models import Student
from courses.models import Subject, SessionYear

class AttendanceSelectionForm(forms.Form):
    subject_id = forms.ModelChoiceField(
        queryset=Subject.objects.all().order_by('subject_name'),
        empty_label="Select Subject",
        widget=forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'})
    )
    session_year_id = forms.ModelChoiceField(
        queryset=SessionYear.objects.all().order_by('-session_start_year'),
        empty_label="Select Session Year",
        widget=forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'})
    )
    attendance_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'})
    )

class MarkAttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.students = kwargs.pop('students', [])
        super().__init__(*args, **kwargs)

        for student in self.students:
            field_name = f'student_{student.id}_status'
            self.fields[field_name] = forms.BooleanField(
                label=f"{student.admin.get_full_name()} ({student.admin.username})",
                required=False,
                widget=forms.CheckboxInput(attrs={'class': 'focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded'})
            )