# core/forms.py
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
        })

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        # --- IMPORTANT CHANGE HERE ---
        # Include 'user_type' in the fields list
        # Ensure that get_user_model() has 'student' and 'staff' as valid choices
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type') 
        # -----------------------------
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to all fields in this form
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm'
            })
        
        # Optionally, restrict choices for user_type for public signup
        # For example, to only allow 'student' or 'staff', not 'admin':
        # if 'user_type' in self.fields:
        #    allowed_choices = [choice for choice in self.fields['user_type'].choices if choice[0] in ['student', 'staff']]
        #    self.fields['user_type'].choices = allowed_choices

        # Remove the default help text for password fields from AbstractUser
        if 'password' in self.fields:
            self.fields['password'].help_text = None
        if 'password2' in self.fields:
            self.fields['password2'].help_text = None