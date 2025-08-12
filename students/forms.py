# students/forms.py
from django import forms
from core.models import CustomUser
from .models import Student
from courses.models import Course, SessionYear # Required for choice fields

# Form for the CustomUser part when adding/editing a student
class StudentUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep current password. For new users, a password is required.")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Enter the same password as above.")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # For new user creation, password is required
        if not self.instance.pk and not password: # If creating new user and password is empty
            self.add_error('password', "Password is required for new users.")
        elif password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data

# Form for the Student-specific profile details
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['gender', 'address', 'course_id', 'session_year_id', 'date_of_birth']
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'course_id': forms.Select(attrs={'class': 'form-control'}),
            'session_year_id': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate ForeignKey choice fields
        self.fields['course_id'].queryset = Course.objects.all().order_by('course_name')
        self.fields['session_year_id'].queryset = SessionYear.objects.all().order_by('-session_start_year')