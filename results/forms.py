# results/forms.py
from django import forms
from .models import Result
from students.models import Student
from courses.models import Subject, Course, SessionYear

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student_id', 'subject_id', 'session_year_id', 'subject_marks', 'exam_marks']
        widgets = {
            'student_id': forms.Select(attrs={'class': 'form-control'}),
            'subject_id': forms.Select(attrs={'class': 'form-control'}),
            'session_year_id': forms.Select(attrs={'class': 'form-control'}),
            'subject_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'exam_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_id'].queryset = Student.objects.all().order_by('admin__username')
        self.fields['subject_id'].queryset = Subject.objects.all().order_by('subject_name')
        self.fields['session_year_id'].queryset = SessionYear.objects.all().order_by('-session_start_year')

# --- NEW FORM FOR ADMIN TO CHECK RESULTS ---
class CheckStudentResultForm(forms.Form):
    course_id = forms.ModelChoiceField(
        queryset=Course.objects.all().order_by('course_name'),
        empty_label="Select Course",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    session_year_id = forms.ModelChoiceField(
        queryset=SessionYear.objects.all().order_by('-session_start_year'),
        empty_label="Select Session Year",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    student_id = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('admin__username'),
        empty_label="Select Student",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically filter students based on course, if a course is selected
        if 'initial' in kwargs and 'course_id' in kwargs['initial']:
            course_id = kwargs['initial']['course_id']
            self.fields['student_id'].queryset = Student.objects.filter(course_id=course_id).order_by('admin__username')