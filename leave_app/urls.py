# leave_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_leave, name='manage_leave'), # Admin side to manage all leave
    path('apply/', views.apply_leave, name='apply_leave'),   # Staff/Student to apply
    path('approve_reject/<int:leave_id>/', views.approve_reject_leave, name='approve_reject_leave'), # Admin approves/rejects specific leave
]