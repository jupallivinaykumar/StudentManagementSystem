from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError # Import IntegrityError for specific error handling
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  ,InvalidPage  # For pagination

from core.views import user_type_required # Re-use the decorator
from core.models import CustomUser
from .forms import StaffUserForm, StaffProfileForm
from .models import Staff

@login_required
@user_type_required(['admin'])
def add_staff(request):
    if request.method == 'POST':
        user_form = StaffUserForm(request.POST, request.FILES)
        profile_form = StaffProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['password'])
                    user.user_type = 'staff' # Ensure user type is set correctly
                    user.save()

                    staff_profile = profile_form.save(commit=False)
                    staff_profile.admin = user
                    staff_profile.save()

                messages.success(request, f"Staff '{user.username}' added successfully!")
                return redirect('manage_staff')
            except IntegrityError: # Catch specific database integrity errors (e.g., duplicate username/email)
                messages.error(request, "A user with this username or email already exists. Please use a different one.")
            except Exception as e:
                messages.error(request, f"Error adding staff: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
            # Pass forms with errors to the template to display specific field errors
    else: # GET request
        user_form = StaffUserForm()
        profile_form = StaffProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Add New Staff'
    }
    return render(request, 'staff/add_staff.html', context)


@login_required
@user_type_required(['admin'])
def manage_staff(request):
    staff_list = Staff.objects.all().order_by('admin__username') # Order for consistency
    
    paginator = Paginator(staff_list, 10) # Show 10 staff per page
    page = request.GET.get('page')

    try:
        staff_members = paginator.page(page)
    except InvalidPage :
        # If page is not an integer, deliver first page.
        staff_members = paginator.page(1)
    context = {
        'staff_members': staff_members,
        'title': 'Manage Staff'
    }
    return render(request, 'staff/manage_staff.html', context)


@login_required
@user_type_required(['admin'])
def edit_staff(request, staff_id):
    staff_profile = get_object_or_404(Staff, id=staff_id)
    user = staff_profile.admin # Get the linked CustomUser object

    if request.method == 'POST':
        user_form = StaffUserForm(request.POST, request.FILES, instance=user)
        profile_form = StaffProfileForm(request.POST, instance=staff_profile)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    # Ensure password is not reset if not changed by admin
                    if 'password' in user_form.cleaned_data and user_form.cleaned_data['password']:
                        user.set_password(user_form.cleaned_data['password'])
                    user.save() # Save CustomUser changes

                    profile_form.save() # Save Staff profile changes

                messages.success(request, f"Staff '{user.username}' updated successfully!")
                return redirect('manage_staff')
            except IntegrityError:
                messages.error(request, "A user with this username or email already exists. Please use a different one.")
            except Exception as e:
                messages.error(request, f"Error updating staff: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
            # Pass forms with errors to the template
    else: # GET request
        user_form = StaffUserForm(instance=user)
        profile_form = StaffProfileForm(instance=staff_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'staff_profile': staff_profile, # Pass for displaying current profile pic or other details
        'title': 'Edit Staff'
    }
    return render(request, 'staff/edit_staff.html', context)


@login_required
@user_type_required(['admin'])
def delete_staff(request, staff_id):
    staff_profile = get_object_or_404(Staff, id=staff_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Deleting the CustomUser will automatically delete the Staff profile due to CASCADE
                staff_profile.admin.delete()
            messages.success(request, f"Staff '{staff_profile.admin.username}' deleted successfully!")
            return redirect('manage_staff')
        except Exception as e:
            messages.error(request, f"Error deleting staff: {e}. It might be linked to other records (e.g., subjects, attendance).")
            return redirect('manage_staff') # Stay on manage page with error

    # For a GET request to /delete, render a confirmation page
    context = {
        'object': staff_profile, # For the confirmation template
        'title': f'Confirm Delete Staff: {staff_profile.admin.username}'
    }
    # Re-use the generic confirm_delete.html template from courses app
    return render(request, 'courses/confirm_delete.html', context)