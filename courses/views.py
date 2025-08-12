# courses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
# --- CRITICAL CORRECTION: Use InvalidPage to catch all pagination errors cleanly ---
from django.core.paginator import Paginator, InvalidPage
# ------------------------------------------------------------------------------------

from core.views import user_type_required
from .forms import CourseForm, SessionYearForm, SubjectForm
from .models import Course, SessionYear, Subject
from staff.models import Staff
from students.models import Student

# --- Course Management (Admin) ---
@login_required
@user_type_required(['admin'])
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Course added successfully!")
                return redirect('manage_courses')
            except IntegrityError:
                messages.error(request, "A course with this name already exists.")
            except Exception as e:
                messages.error(request, f"Error adding course: {e}")
        else:
            messages.error(request, "Failed to add course. Please check the form.")
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form, 'title': 'Add New Course'})

@login_required
@user_type_required(['admin'])
def manage_courses(request):
    course_list = Course.objects.all().order_by('course_name')
    
    paginator = Paginator(course_list, 10)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except InvalidPage:
        courses = paginator.page(1)
        # Note: We don't need a separate except EmptyPage because InvalidPage catches it
    return render(request, 'courses/manage_courses.html', {'courses': courses, 'title': 'Manage Courses'})

@login_required
@user_type_required(['admin'])
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Course updated successfully!")
                return redirect('manage_courses')
            except IntegrityError:
                messages.error(request, "A course with this name already exists.")
            except Exception as e:
                messages.error(request, f"Error updating course: {e}")
        else:
            messages.error(request, "Failed to update course. Please check the form.")
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course, 'title': 'Edit Course'})

@login_required
@user_type_required(['admin'])
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        try:
            course.delete()
            messages.success(request, "Course deleted successfully!")
        except Exception as e:
            messages.error(request, f"Cannot delete course: {e}. It might be referenced by subjects or students.")
        return redirect('manage_courses')
    return render(request, 'courses/confirm_delete.html', {'object': course, 'title': 'Confirm Delete Course'})


# --- Session Year Management (Admin) ---
@login_required
@user_type_required(['admin'])
def add_session_year(request):
    if request.method == 'POST':
        form = SessionYearForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Year added successfully!")
                return redirect('manage_session_years')
            except IntegrityError:
                messages.error(request, "This session year already exists.")
            except Exception as e:
                messages.error(request, f"Error adding session year: {e}")
        else:
            messages.error(request, "Failed to add session year. Please check the form.")
    else:
        form = SessionYearForm()
    return render(request, 'courses/add_session_year.html', {'form': form, 'title': 'Add New Session Year'})

@login_required
@user_type_required(['admin'])
def manage_session_years(request):
    session_year_list = SessionYear.objects.all().order_by('-session_start_year')
    
    paginator = Paginator(session_year_list, 10)
    page = request.GET.get('page')
    try:
        session_years = paginator.page(page)
    except InvalidPage:
        session_years = paginator.page(1)

    return render(request, 'courses/manage_session_years.html', {'session_years': session_years, 'title': 'Manage Session Years'})

@login_required
@user_type_required(['admin'])
def edit_session_year(request, session_year_id):
    session_year = get_object_or_404(SessionYear, id=session_year_id)
    if request.method == 'POST':
        form = SessionYearForm(request.POST, instance=session_year)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Year updated successfully!")
                return redirect('manage_session_years')
            except IntegrityError:
                messages.error(request, "This session year already exists.")
            except Exception as e:
                messages.error(request, f"Error updating session year: {e}")
        else:
            messages.error(request, "Failed to update session year. Please check the form.")
    else:
        form = SessionYearForm(instance=session_year)
    return render(request, 'courses/edit_session_year.html', {'form': form, 'session_year': session_year, 'title': 'Edit Session Year'})

@login_required
@user_type_required(['admin'])
def delete_session_year(request, session_year_id):
    session_year = get_object_or_404(SessionYear, id=session_year_id)
    if request.method == 'POST':
        try:
            session_year.delete()
            messages.success(request, "Session Year deleted successfully!")
        except Exception as e:
            messages.error(request, f"Cannot delete session year: {e}. It might be referenced by subjects or students.")
        return redirect('manage_session_years')
    return render(request, 'courses/confirm_delete.html', {'object': session_year, 'title': 'Confirm Delete Session Year'})

# --- Subject Management (Admin) ---
@login_required
@user_type_required(['admin'])
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Subject added successfully!")
                return redirect('manage_subjects')
            except IntegrityError:
                messages.error(request, "A subject with this name already exists in this course.")
            except Exception as e:
                messages.error(request, f"Error adding subject: {e}")
        else:
            messages.error(request, "Failed to add subject. Please check the form.")
    else:
        form = SubjectForm()
    return render(request, 'courses/add_subject.html', {'form': form, 'title': 'Add New Subject'})

@login_required
@user_type_required(['admin'])
def manage_subjects(request):
    subject_list = Subject.objects.all().order_by('subject_name')
    
    paginator = Paginator(subject_list, 10)
    page = request.GET.get('page')
    try:
        subjects = paginator.page(page)
    except InvalidPage:
        subjects = paginator.page(1)

    return render(request, 'courses/manage_subjects.html', {'subjects': subjects, 'title': 'Manage Subjects'})

@login_required
@user_type_required(['admin'])
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Subject updated successfully!")
                return redirect('manage_subjects')
            except IntegrityError:
                messages.error(request, "A subject with this name already exists for this course.")
            except Exception as e:
                messages.error(request, f"Error updating subject: {e}")
        else:
            messages.error(request, "Failed to update subject. Please check the form.")
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'courses/edit_subject.html', {'form': form, 'subject': subject, 'title': 'Edit Subject'})

@login_required
@user_type_required(['admin'])
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        try:
            subject.delete()
            messages.success(request, "Subject deleted successfully!")
        except Exception as e:
            messages.error(request, f"Cannot delete subject: {e}. It might be referenced by attendance or results.")
        return redirect('manage_subjects')
    return render(request, 'courses/confirm_delete.html', {'object': subject, 'title': 'Confirm Delete Subject'})