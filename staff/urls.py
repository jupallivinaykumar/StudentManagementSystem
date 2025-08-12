# staff/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_staff, name='add_staff'),
    path('manage/', views.manage_staff, name='manage_staff'),
    path('edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
]