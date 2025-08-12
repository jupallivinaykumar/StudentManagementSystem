# staff/admin.py
from django.contrib import admin
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'get_email', 'get_full_name', 'gender', 'address', 'date_of_birth')
    search_fields = ('admin__username', 'admin__first_name', 'admin__last_name', 'admin__email')
    list_filter = ('gender',)

    def get_username(self, obj):
        return obj.admin.username
    get_username.short_description = 'Username' # Column header

    def get_email(self, obj):
        return obj.admin.email
    get_email.short_description = 'Email'

    def get_full_name(self, obj):
        return obj.admin.get_full_name()
    get_full_name.short_description = 'Full Name'