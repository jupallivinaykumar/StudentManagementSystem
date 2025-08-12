# leave_app/forms.py
from django import forms
from .models import Leave

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_date', 'leave_message']
        widgets = {
            'leave_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'leave_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Reason for leave...'}),
        }
        labels = {
            'leave_date': 'Date of Leave',
            'leave_message': 'Reason for Leave',
        }

class LeaveApprovalForm(forms.ModelForm): # Form to update status of leave by admin
    class Meta:
        model = Leave
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }