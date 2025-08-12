# students/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger ,InvalidPage 

from core.views import user_type_required # Re-use the decorator
from core.models import CustomUser
from .forms import StudentUserForm, StudentProfileForm
from .models import Student

@login_required
@user_type_required(['admin'])
def add_student(request):
    if request.method == 'POST':
        user_form = StudentUserForm(request.POST, request.FILES)
        profile_form = StudentProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.user_type = 'student' # Ensure user type is set correctly
                    user.save()

                    student_profile = profile_form.save(commit=False)
                    student_profile.admin = user # Link the Student profile to the CustomUser
                    student_profile.save()

                messages.success(request, f"Student '{user.username}' added successfully!")
                return redirect('manage_students') # Redirect to the student list page
            except IntegrityError:
                messages.error(request, "A user with this username or email already exists. Please use a different one.")
            except Exception as e:
                messages.error(request, f"Error adding student: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
            # Forms are passed to context implicitly containing their errors
    else: # This is a GET request, so display empty forms
        user_form = StudentUserForm()
        profile_form = StudentProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Add New Student'
    }
    return render(request, 'students/add_student.html', context)


@login_required
@user_type_required(['admin'])
def manage_students(request):
    student_list = Student.objects.all().order_by('admin__username') # Order for consistency
    
    paginator = Paginator(student_list, 10) # Show 10 students per page
    page = request.GET.get('page')

    try:
        students = paginator.page(page)
    except InvalidPage :
        students = paginator.page(1)
    context = {
        'students': students, # This is the paginated object
        'title': 'Manage Students'
    }
    return render(request, 'students/manage_students.html', context)


@login_required
@user_type_required(['admin'])
def edit_student(request, student_id):
    student_profile = get_object_or_404(Student, id=student_id)
    user = student_profile.admin # Get the linked CustomUser object

    if request.method == 'POST':
        user_form = StudentUserForm(request.POST, request.FILES, instance=user)
        profile_form = StudentProfileForm(request.POST, instance=student_profile)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    # Handle password change: only update if a new password is provided
                    if 'password' in user_form.cleaned_data and user_form.cleaned_data['password']:
                        user.set_password(user_form.cleaned_data['password'])
                    user.save() # Save CustomUser changes (including password if updated)

                    profile_form.save() # Save Student profile changes

                messages.success(request, f"Student '{user.username}' updated successfully!")
                return redirect('manage_students')
            except IntegrityError:
                messages.error(request, "A user with this username or email already exists. Please use a different one.")
            except Exception as e:
                messages.error(request, f"Error updating student: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else: # This is a GET request, so pre-populate forms with existing data
        user_form = StudentUserForm(instance=user)
        # Note: Set password to None/empty for security in edit form
        user_form.fields['password'].initial = ""
        user_form.fields['confirm_password'].initial = ""
        
        profile_form = StudentProfileForm(instance=student_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'student_profile': student_profile, # Pass for displaying current profile pic or other details
        'title': 'Edit Student'
    }
    return render(request, 'students/edit_student.html', context)


@login_required
@user_type_required(['admin'])
def delete_student(request, student_id):
    student_profile = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Deleting the CustomUser will automatically delete the Student profile
                # due to on_delete=models.CASCADE in the Student model's 'admin' field.
                student_profile.admin.delete()
            messages.success(request, f"Student '{student_profile.admin.username}' deleted successfully!")
            return redirect('manage_students')
        except Exception as e:
            messages.error(request, f"Error deleting student: {e}. It might be linked to other records (e.g., attendance, results).")
            return redirect('manage_students') # Stay on manage page with error

    # For a GET request to /delete, render a confirmation page
    context = {
        'object': student_profile, # For the confirmation template
        'title': f'Confirm Delete Student: {student_profile.admin.username}'
    }
    # Re-use the generic confirm_delete.html template from courses app
    return render(request, 'courses/confirm_delete.html', context)