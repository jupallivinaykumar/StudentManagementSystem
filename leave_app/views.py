# leave_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage 

from core.views import user_type_required
from .forms import LeaveApplicationForm, LeaveApprovalForm
from .models import Leave

@login_required
@user_type_required(['staff', 'student']) # Both staff and students can apply for leave
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user_id = request.user # Link the leave request to the logged-in user
            leave_request.save()
            messages.success(request, "Leave application submitted successfully. Awaiting admin approval.")
            return redirect('apply_leave') # Redirect back to the same page or a confirmation page
        else:
            messages.error(request, "Failed to submit leave application. Please correct the errors.")
    else: # GET request
        form = LeaveApplicationForm()
    
    # Also show user's own pending/approved/rejected leaves on this page
    user_leaves = Leave.objects.filter(user_id=request.user).order_by('-leave_date')
    
    context = {
        'form': form,
        'user_leaves': user_leaves,
        'title': 'Apply for Leave'
    }
    return render(request, 'leave_app/apply_leave.html', context)

@login_required
@user_type_required(['admin']) # Only admin can manage/approve leave requests
def manage_leave(request):
    leave_list = Leave.objects.all().order_by('-created_at') # Order by most recent
    
    paginator = Paginator(leave_list, 10) # 10 leaves per page
    page = request.GET.get('page')

    try:
        leaves = paginator.page(page)
    except InvalidPage :
        leaves = paginator.page(1)

    context = {
        'leaves': leaves,
        'title': 'Manage Leave Applications'
    }
    return render(request, 'leave_app/manage_leave.html', context)

@login_required
@user_type_required(['admin'])
def approve_reject_leave(request, leave_id): # This view handles approval/rejection
    leave_request = get_object_or_404(Leave, id=leave_id)
    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, instance=leave_request)
        if form.is_valid():
            form.save() # Saves the updated status
            messages.success(request, f"Leave request for {leave_request.user_id.username} updated to {leave_request.get_status_display()}.")
            return redirect('manage_leave')
        else:
            messages.error(request, "Failed to update leave status. Please correct the errors.")
    else: # GET request
        form = LeaveApprovalForm(instance=leave_request) # Pre-populate status
    
    context = {
        'form': form,
        'leave_request': leave_request,
        'title': 'Approve/Reject Leave'
    }
    return render(request, 'leave_app/approve_reject_leave.html', context)