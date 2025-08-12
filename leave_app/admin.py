# leave_app/admin.py
from django.contrib import admin
from .models import Leave

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'leave_date', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'leave_date')
    search_fields = ('user_id__username', 'user_id__first_name', 'leave_message')
    raw_id_fields = ('user_id',)
    # Make status editable in list view for quick approval/rejection
    list_editable = ('status',)