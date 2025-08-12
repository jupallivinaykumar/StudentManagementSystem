# results/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage
from django.db import transaction, IntegrityError # Ensure IntegrityError is imported

from core.views import user_type_required
from .forms import ResultForm, CheckStudentResultForm # Ensure new form is imported
from .models import Result
from students.models import Student
from courses.models import Subject, Course, SessionYear # Ensure all models are imported


@login_required
@user_type_required(['admin']) # Admin can manage all results
def manage_results(request):
    results_list = Result.objects.all().order_by('-session_year_id__session_start_year', 'student_id__admin__username')
    paginator = Paginator(results_list, 10)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except InvalidPage:
        results = paginator.page(1)
    
    context = {
        'results': results,
        'title': 'Manage All Results'
    }
    return render(request, 'results/manage_results.html', context)


@login_required
@user_type_required(['admin', 'staff']) # Admin and staff can add results
def add_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Result added successfully!")
                return redirect('manage_results')
            except IntegrityError:
                messages.error(request, "A result for this student in this subject and session already exists.")
            except Exception as e:
                messages.error(request, f"Error adding result: {e}")
        else:
            messages.error(request, "Failed to add result. Please correct the errors.")
    else:
        form = ResultForm()
    
    context = {
        'form': form,
        'title': 'Add Student Result'
    }
    return render(request, 'results/add_result.html', context)

# --- NEW VIEW FOR ADMIN TO CHECK STUDENT RESULTS ---
@login_required
@user_type_required(['admin'])
def check_student_result(request):
    form = CheckStudentResultForm(request.GET)
    results = Result.objects.none() # Empty queryset by default
    student_profile = None

    if form.is_valid():
        course = form.cleaned_data.get('course_id')
        session_year = form.cleaned_data.get('session_year_id')
        student = form.cleaned_data.get('student_id')

        if course and session_year and student:
            results = Result.objects.filter(
                student_id=student,
                session_year_id=session_year,
                subject_id__course_id=course
            ).select_related('subject_id', 'session_year_id')
            
            student_profile = student
            
            if not results.exists():
                messages.info(request, f"No results found for {student_profile.admin.get_full_name()} in {course.course_name} for {session_year}.")

    context = {
        'form': form,
        'results': results,
        'student_profile': student_profile,
        'title': 'Check Student Results'
    }
    return render(request, 'results/view_student_result.html', context)