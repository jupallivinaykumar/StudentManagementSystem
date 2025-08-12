# feedback_app/admin.py
from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'subject', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user_id__username', 'user_id__first_name', 'feedback_message', 'subject')
    raw_id_fields = ('user_id',)
    # Make reply_message editable in list view for quick replies (if you wish)
    list_editable = ('status',)