# courses/forms.py
from django import forms
from .models import Course, SessionYear, Subject
from staff.models import Staff

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course Name'})
        }

class SessionYearForm(forms.ModelForm):
    class Meta:
        model = SessionYear
        fields = ['session_start_year', 'session_end_year']
        widgets = {
            'session_start_year': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'session_end_year': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name', 'course_id', 'staff_id']
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject Name'}),
            'course_id': forms.Select(attrs={'class': 'form-control'}),
            'staff_id': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_id'].queryset = Course.objects.all().order_by('course_name')
        self.fields['staff_id'].queryset = Staff.objects.all().order_by('admin__username')