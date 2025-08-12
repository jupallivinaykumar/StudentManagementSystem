# feedback_app/forms.py
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'feedback_message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief subject...'}),
            'feedback_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your feedback...'}),
        }
        labels = {
            'subject': 'Subject (Optional)',
            'feedback_message': 'Your Feedback',
        }

class ReplyFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['reply_message', 'status']
        widgets = {
            'reply_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your reply...'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # Checkbox for status
        }
        labels = {
            'reply_message': 'Reply Message',
            'status': 'Mark as Replied/Resolved',
        }