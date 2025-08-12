# results/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_results, name='manage_results'),
    path('add/', views.add_result, name='add_result'),
    # --- NEW URL ---
    path('check_student/', views.check_student_result, name='check_student_result'),
    # ---------------
]