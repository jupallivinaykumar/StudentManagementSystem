# core/views.py (simplified example)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomAuthenticationForm # Create this form

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == "admin":
                    return redirect('admin_dashboard')
                elif user.user_type == "staff":
                    return redirect('staff_dashboard')
                elif user.user_type == "student":
                    return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def admin_dashboard(request):
    # Logic for admin dashboard
    return render(request, 'core/admin_dashboard.html')

# Similar views for staff_dashboard and student_dashboard

def custom_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# core/forms.py (CustomAuthenticationForm)
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# student_management_system/urls.py (main project urls)
from django.contrib import admin
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.custom_login_view, name='login'), # Your custom login page
    path('logout/', core_views.custom_logout_view, name='logout'),

    path('admin_dashboard/', core_views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', core_views.staff_dashboard, name='staff_dashboard'),
    path('student_dashboard/', core_views.student_dashboard, name='student_dashboard'),

    # Include URLs for other apps
    path('students/', include('students.urls')),
    path('staff/', include('staff.urls')),
    path('courses/', include('courses.urls')),
    
    path('admin/pending_users/', core_views.manage_pending_users, name='manage_pending_users'),
    path('admin/approve_user/<int:user_id>/', core_views.approve_user, name='approve_user'),
    # ---------------------------------------------------------------

]