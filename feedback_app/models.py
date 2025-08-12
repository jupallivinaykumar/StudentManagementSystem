# feedback_app/models.py
from django.db import models
from core.models import CustomUser

class Feedback(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, blank=True, null=True)
    feedback_message = models.TextField()
    reply_message = models.TextField(blank=True, null=True) # Admin's reply
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False) # False for pending, True for replied/resolved

    def __str__(self):
        return f"Feedback from {self.user_id.username} - {self.subject[:50]}"