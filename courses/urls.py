# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Course URLs
    path('add/', views.add_course, name='add_course'),
    path('manage/', views.manage_courses, name='manage_courses'),
    path('edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete/<int:course_id>/', views.delete_course, name='delete_course'),

    # Session Year URLs
    path('sessions/add/', views.add_session_year, name='add_session_year'),
    path('sessions/manage/', views.manage_session_years, name='manage_session_years'),
    path('sessions/edit/<int:session_year_id>/', views.edit_session_year, name='edit_session_year'),
    path('sessions/delete/<int:session_year_id>/', views.delete_session_year, name='delete_session_year'),

    # Subject URLs
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/manage/', views.manage_subjects, name='manage_subjects'),
    path('subjects/edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),
]