from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q # Added for dashboard charts
from django.core.paginator import Paginator, EmptyPage, InvalidPage # For pagination

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import CustomUser
from students.models import Student
from staff.models import Staff
from courses.models import Course, Subject, SessionYear
from attendance.models import Attendance, AttendanceReport
from results.models import Result
from feedback_app.models import Feedback
from leave_app.models import Leave

# For email (placeholder)
from django.core.mail import send_mail
from django.conf import settings # To access settings like EMAIL_HOST_USER

# Decorator to ensure only specific user types can access a view
def user_type_required(allowed_user_types):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, "Please log in to access this page.")
                return redirect('login')
            # Check if user is active
            if not request.user.is_active:
                messages.error(request, "Your account is not active. Please wait for administrator approval.")
                logout(request) # Log out inactive users
                return redirect('login')
            if request.user.user_type not in allowed_user_types:
                messages.error(request, "You are not authorized to access this page.")
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

def custom_login_view(request):
    if request.user.is_authenticated:
        if not request.user.is_active: # Check if active even if authenticated
            messages.error(request, "Your account is not active. Please wait for administrator approval.")
            logout(request)
            return redirect('login')
        # Existing redirection logic
        if request.user.user_type == "admin":
            return redirect('admin_dashboard')
        elif request.user.user_type == "staff":
            return redirect('staff_dashboard')
        elif request.user.user_type == "student":
            return redirect('student_dashboard')
        else:
            messages.error(request, "Unknown user type. Please contact administrator.")
            return redirect('logout')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if not user.is_active: # Check if active after successful authentication
                    messages.error(request, "Your account is not active. Please wait for administrator approval.")
                    logout(request)
                    return redirect('login')
                
                login(request, user)
                messages.success(request, f"Welcome, {user.first_name if user.first_name else user.username}!")
                
                if user.user_type == "admin":
                    return redirect('admin_dashboard')
                elif user.user_type == "staff":
                    return redirect('staff_dashboard')
                elif user.user_type == "student":
                    return redirect('student_dashboard')
                else:
                    messages.error(request, "Unknown user type. Please contact administrator.")
                    return redirect('logout')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        if not request.user.is_active: # Check if active even if authenticated
            messages.error(request, "Your account is not active. Please wait for administrator approval.")
            logout(request)
            return redirect('login')
        # Existing redirection logic
        if request.user.user_type == "admin":
            return redirect('admin_dashboard')
        elif request.user.user_type == "staff":
            return redirect('staff_dashboard')
        elif request.user.user_type == "student":
            return redirect('student_dashboard')
        else:
            messages.error(request, "Unknown user type. Please contact administrator.")
            return redirect('logout')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # --- CRITICAL CHANGE: Set is_active to False for new signups ---
            user.is_active = False # Account is inactive until approved by admin
            # ---------------------------------------------------------------
            user.save() # Saves the user with the user_type selected in the form

            # Auto-create profile is handled by signals, so no need here.

            messages.success(request, 'Account created successfully! Please wait for administrator approval to log in.')
            
            # --- Optional: Send email to admin for new signup notification ---
            try:
                subject = 'New User Signup for Approval'
                message = f'A new user has signed up: Username: {user.username}, Email: {user.email}, Type: {user.user_type}. Please log in to the admin panel to approve their account.'
                from_email = settings.EMAIL_HOST_USER # Or a generic email
                recipient_list = [settings.ADMINS[0][1]] if settings.ADMINS else ['admin@example.com'] # Send to first admin email
                
                # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                # print(f"Email notification sent to {recipient_list} for new user {user.username}") # For debugging
            except Exception as e:
                print(f"Error sending email notification: {e}") # Log email errors
            # -----------------------------------------------------------------

            return redirect('login') # Redirect to the login page after successful signup
        else:
            messages.error(request, 'Failed to create account. Please correct the errors.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form, 'title': 'Create Your Account'})


@login_required
@user_type_required(['admin'])
def admin_dashboard(request):
    # --- 1. Total Counts for Top Cards ---
    total_students = Student.objects.count()
    total_staffs = Staff.objects.count()
    total_courses = Course.objects.count()
    total_subjects = Subject.objects.count()

    # --- 2. Data for Student and Staff Chart (Proportion) ---
    user_type_counts = CustomUser.objects.values('user_type').annotate(count=Count('user_type'))

    student_count_chart = 0
    staff_count_chart = 0
    admin_count_chart = 0
    for item in user_type_counts:
        if item['user_type'] == 'student':
            student_count_chart = item['count']
        elif item['user_type'] == 'staff':
            staff_count_chart = item['count']
        elif item['user_type'] == 'admin':
            admin_count_chart = item['count']

    # --- 3. Data for Total Students in Each Course Chart ---
    students_per_course_query = Student.objects.values(
        'course_id__course_name'
    ).annotate(
        student_count=Count('id')
    ).order_by('course_id__course_name')

    course_names_students = []
    students_in_courses = []
    for item in students_per_course_query:
        if item['course_id__course_name']:
            course_names_students.append(item['course_id__course_name'])
            students_in_courses.append(item['student_count'])

    students_without_course_count = Student.objects.filter(course_id__isnull=True).count()
    if students_without_course_count > 0:
        course_names_students.append('Unassigned')
        students_in_courses.append(students_without_course_count)


    # --- 4. Data for Total Subjects in Each Course Chart ---
    subjects_per_course_query = Subject.objects.values(
        'course_id__course_name'
    ).annotate(
        subject_count=Count('id')
    ).order_by('course_id__course_name')

    course_names_subjects = []
    subjects_in_courses = []
    for item in subjects_per_course_query:
        if item['course_id__course_name']:
            course_names_subjects.append(item['course_id__course_name'])
            subjects_in_courses.append(item['subject_count'])

    subjects_without_course_count = Subject.objects.filter(course_id__isnull=True).count()
    if subjects_without_course_count > 0:
        course_names_subjects.append('Unassigned')
        subjects_in_courses.append(subjects_without_course_count)


    # --- 5. Data for Total Students in Each Subject Chart ---
    students_per_subject_query = Subject.objects.annotate(
        student_count=Count('result__student_id', distinct=True) 
    ).values(
        'subject_name', 'student_count'
    ).order_by('subject_name')

    subject_names_students = [item['subject_name'] for item in students_per_subject_query]
    students_in_subjects = [item['student_count'] for item in students_per_subject_query]


    context = {
        'total_students': total_students,
        'total_staffs': total_staffs,
        'total_courses': total_courses,
        'total_subjects': total_subjects,

        'student_count_chart': student_count_chart,
        'staff_count_chart': staff_count_chart,
        'admin_count_chart': admin_count_chart, 

        'course_names_students': course_names_students,
        'students_in_courses': students_in_courses,

        'course_names_subjects': course_names_subjects,
        'subjects_in_courses': subjects_in_courses,

        'subject_names_students': subject_names_students,
        'students_in_subjects': students_in_subjects,
    }
    return render(request, 'core/admin_dashboard.html', context)

# --- Admin Views for User Approval (Paginator exception fix) ---
@login_required
@user_type_required(['admin'])
def manage_pending_users(request):
    pending_users = CustomUser.objects.filter(is_active=False).order_by('-date_joined')
    
    paginator = Paginator(pending_users, 10)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    # --- CRITICAL CHANGE: Use InvalidPage here ---
    except InvalidPage: # Catches both PageNotInteger and EmptyPage
        users = paginator.page(1)
    # ---------------------------------------------
    
    context = {
        'pending_users': users,
        'title': 'Manage Pending User Approvals'
    }
    return render(request, 'core/manage_pending_users.html', context)

@login_required
@user_type_required(['admin'])
def approve_user(request, user_id):
    user_to_approve = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        user_to_approve.is_active = True
        user_to_approve.save()

        # --- Optional: Send email to approved user ---
        try:
            subject = 'Your Account Has Been Approved!'
            message = f'Dear {user_to_approve.first_name if user_to_approve.first_name else user_to_approve.username},\n\nYour account on the Student Management System has been approved. You can now log in using your credentials.\n\nThank you.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user_to_approve.email]
            
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            # print(f"Email notification sent to {user_to_approve.email} for approval.") # For debugging
        except Exception as e:
            print(f"Error sending approval email: {e}")
        # ---------------------------------------------

        messages.success(request, f"User '{user_to_approve.username}' has been approved and activated.")
        return redirect('manage_pending_users')
    
    context = {
        'user_to_approve': user_to_approve,
        'title': 'Confirm User Approval'
    }
    return render(request, 'core/confirm_approve_user.html', context)


def custom_logout_view(request):
    logout(request) # Django's built-in logout function
    messages.info(request, "You have been logged out.")
    return redirect('login') # Redirect to the login page


@login_required
@user_type_required(['staff'])
def staff_dashboard(request):
    staff_profile = None
    students_for_staff = Student.objects.none() # Initialize an empty queryset
    try:
        staff_profile = Staff.objects.get(admin=request.user)
        
        # --- CRITICAL QUERY TO ATTACH STUDENTS TO STAFF ---
        # 1. Get the list of Course IDs for all subjects this staff member teaches
        courses_taught_ids = Subject.objects.filter(staff_id=staff_profile).values_list('course_id', flat=True).distinct()
        
        # 2. Get all students who are enrolled in any of those courses
        students_for_staff = Student.objects.filter(
            course_id__in=courses_taught_ids
        ).select_related('admin', 'course_id', 'session_year_id').order_by('admin__first_name')
        # We use select_related() to optimize the query and avoid fetching user/course/session data multiple times
        # --------------------------------------------------

    except Staff.DoesNotExist:
        messages.error(request, "Your staff profile could not be found. Please contact an administrator.")
        logout(request)
        return redirect('login')
    
    # --- Other data for the dashboard (already implemented) ---
    total_subjects_taught = Subject.objects.filter(staff_id=staff_profile).count()
    students_in_my_courses = students_for_staff.count() # Use the filtered count
    pending_my_leaves = Leave.objects.filter(user_id=request.user, status=0).count()
    feedback_sent_by_me = Feedback.objects.filter(user_id=request.user).count()

    context = {
        'staff_profile': staff_profile,
        'total_subjects_taught': total_subjects_taught,
        'students_in_my_courses': students_in_my_courses,
        'pending_my_leaves': pending_my_leaves,
        'feedback_sent_by_me': feedback_sent_by_me,
        'students_for_staff': students_for_staff, # <-- Pass the filtered student list to the template
        'title': 'Staff Dashboard'
    }
    return render(request, 'core/staff_dashboard.html', context)


@login_required
@user_type_required(['student'])
def student_dashboard(request):
    student_profile = None
    context = {}

    try:
        student_profile = Student.objects.get(admin=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Your student profile could not be found. Please contact an administrator.")
        return redirect('logout')
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}. Please contact support.")
        return redirect('logout')

    context = {
        'student_profile': student_profile,
    }
    return render(request, 'core/student_dashboard.html', context)
