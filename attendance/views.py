# attendance/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage
from django.db import transaction

from core.views import user_type_required
from students.models import Student
from .forms import AttendanceSelectionForm, MarkAttendanceForm
from .models import Attendance, AttendanceReport, Subject, SessionYear


@login_required
@user_type_required(['admin']) # Admin view for overall management
def manage_attendance(request):
    attendance_records = Attendance.objects.all().order_by('-attendance_date', 'subject_id__subject_name')
    
    paginator = Paginator(attendance_records, 10)
    page = request.GET.get('page')
    try:
        attendances = paginator.page(page)
    except InvalidPage:
        attendances = paginator.page(1)

    context = {
        'attendances': attendances,
        'title': 'Manage All Attendance'
    }
    return render(request, 'attendance/manage_attendance.html', context)


@login_required
@user_type_required(['staff']) # Staff takes attendance
def add_attendance(request):
    attendance_selection_form = AttendanceSelectionForm()
    marking_form = None
    students_in_class = []
    
    selected_subject = None
    selected_session = None
    selected_date = None

    if request.method == 'GET' and 'subject_id' in request.GET:
        try:
            subject_id = request.GET.get('subject_id')
            session_year_id = request.GET.get('session_year_id')
            attendance_date_str = request.GET.get('attendance_date')

            selected_subject = get_object_or_404(Subject, id=subject_id)
            selected_session = get_object_or_404(SessionYear, id=session_year_id)
            selected_date = attendance_date_str

            students_in_class = Student.objects.filter(
                course_id=selected_subject.course_id,
                session_year_id=selected_session
            ).order_by('admin__first_name', 'admin__last_name')

            marking_form = MarkAttendanceForm(students=students_in_class)

            attendance_selection_form = AttendanceSelectionForm(initial={
                'subject_id': selected_subject,
                'session_year_id': selected_session,
                'attendance_date': selected_date
            })

            if not students_in_class.exists():
                 messages.info(request, "No students found for this subject and session. Please ensure students are enrolled in this course for this session.")

        except Exception as e:
            messages.error(request, f"Error fetching students: {e}")
            return redirect('add_attendance')

    elif request.method == 'POST':
        attendance_selection_form = AttendanceSelectionForm(request.POST)

        subject_id = request.POST.get('subject_id_hidden')
        session_year_id = request.POST.get('session_year_id_hidden')
        attendance_date_str = request.POST.get('attendance_date_hidden')

        if subject_id and session_year_id:
            try:
                selected_subject = get_object_or_404(Subject, id=subject_id)
                selected_session = get_object_or_404(SessionYear, id=session_year_id)
                selected_date = attendance_date_str
                
                students_in_class = Student.objects.filter(
                    course_id=selected_subject.course_id,
                    session_year_id=selected_session
                ).order_by('admin__first_name', 'admin__last_name')

                marking_form = MarkAttendanceForm(request.POST, students=students_in_class)

                if marking_form.is_valid():
                    try:
                        with transaction.atomic():
                            attendance_record, created = Attendance.objects.get_or_create(
                                subject_id=selected_subject,
                                session_year_id=selected_session,
                                attendance_date=attendance_date_str
                            )

                            AttendanceReport.objects.filter(attendance_id=attendance_record).delete()

                            for student_profile in students_in_class:
                                status = marking_form.cleaned_data.get(f'student_{student_profile.id}_status', False)
                                
                                AttendanceReport.objects.create(
                                    student_id=student_profile.admin,
                                    attendance_id=attendance_record,
                                    status=status
                                )
                        
                        messages.success(request, f"Attendance for {selected_subject.subject_name} on {selected_date} recorded successfully!")
                        return redirect('add_attendance')
                    except Exception as e:
                        messages.error(request, f"Error saving attendance: {e}")
                else:
                    messages.error(request, "Failed to save attendance. Please check the marking form.")
            except Exception as e:
                messages.error(request, f"Error processing selection for attendance: {e}")
                return redirect('add_attendance')
    
    context = {
        'attendance_selection_form': attendance_selection_form,
        'marking_form': marking_form,
        'students_in_class': students_in_class,
        'selected_subject': selected_subject,
        'selected_session': selected_session,
        'selected_date': selected_date,
        'title': 'Take Attendance'
    }
    return render(request, 'attendance/add_attendance.html', context)
@login_required
@user_type_required(['admin', 'student']) # Both admin and student can view attendance reports
def view_attendance_reports(request):
    # Determine the base template based on user type
    if request.user.user_type == 'admin':
        base_template = 'core/admin_dashboard.html'
    elif request.user.user_type == 'student':
        base_template = 'core/student_dashboard.html'
    else:
        base_template = 'core/login.html' # Fallback

    attendance_reports = AttendanceReport.objects.all().order_by('-attendance_id__attendance_date')

    if request.user.user_type == 'student':
        attendance_reports = attendance_reports.filter(student_id=request.user)

    reports = attendance_reports 

    context = {
        'reports': reports,
        'title': 'Attendance Reports',
        'base_template': base_template,
    }
    return render(request, 'attendance/view_attendance_reports.html', context)
