# feedback_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage 

from core.views import user_type_required
from .forms import FeedbackForm, ReplyFeedbackForm
from .models import Feedback

@login_required
@user_type_required(['staff', 'student']) # Staff and students can send feedback
def send_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user_id = request.user # Link feedback to the logged-in user
            feedback.save()
            messages.success(request, "Feedback submitted successfully. Thank you!")
            return redirect('send_feedback')
        else:
            messages.error(request, "Failed to submit feedback. Please correct the errors.")
    else: # GET request
        form = FeedbackForm()
    
    # Show user's own feedback history
    user_feedback_history = Feedback.objects.filter(user_id=request.user).order_by('-created_at')

    context = {
        'form': form,
        'user_feedback_history': user_feedback_history,
        'title': 'Send Feedback'
    }
    return render(request, 'feedback_app/send_feedback.html', context)

@login_required
@user_type_required(['admin']) # Only admin can manage/view all feedback
def manage_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-created_at') # Most recent first
    
    paginator = Paginator(feedback_list, 10) # 10 feedbacks per page
    page = request.GET.get('page')

    try:
        feedbacks = paginator.page(page)
    except InvalidPage :
        feedbacks = paginator.page(1)

    context = {
        'feedbacks': feedbacks,
        'title': 'View Feedback'
    }
    return render(request, 'feedback_app/manage_feedback.html', context)

@login_required
@user_type_required(['admin'])
def reply_feedback(request, feedback_id): # This view handles the reply functionality
    feedback_item = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        form = ReplyFeedbackForm(request.POST, instance=feedback_item)
        if form.is_valid():
            form.save() # Saves reply_message and updates status (if checkbox checked)
            messages.success(request, "Feedback replied to and updated successfully.")
            return redirect('manage_feedback')
        else:
            messages.error(request, "Failed to reply to feedback. Please correct the errors.")
    else: # GET request
        form = ReplyFeedbackForm(instance=feedback_item) # Pre-populate with existing data
    
    context = {
        'form': form,
        'feedback_item': feedback_item,
        'title': 'Reply to Feedback'
    }
    return render(request, 'feedback_app/reply_feedback.html', context)