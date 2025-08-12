# leave_app/models.py
from django.db import models
from core.models import CustomUser

class Leave(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # The user applying for leave
    leave_date = models.DateField()
    leave_message = models.TextField()
    LEAVE_STATUS_CHOICES = (
        (0, "Pending"),
        (1, "Approved"),
        (2, "Rejected"),
    )
    status = models.IntegerField(choices=LEAVE_STATUS_CHOICES, default=0) # 0: Pending, 1: Approved, 2: Rejected
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status_text = dict(self.LEAVE_STATUS_CHOICES).get(self.status, "Unknown")
        return f"Leave for {self.user_id.username} on {self.leave_date} ({status_text})"