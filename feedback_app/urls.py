# feedback_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_feedback, name='send_feedback'),
    path('manage/', views.manage_feedback, name='manage_feedback'),
    path('reply/<int:feedback_id>/', views.reply_feedback, name='reply_feedback'), # Admin replies to specific feedback
]