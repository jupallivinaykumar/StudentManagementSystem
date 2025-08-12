# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # Import UserAdmin
from .models import CustomUser

# Define a custom admin class for CustomUser
class CustomUserAdmin(UserAdmin):
    # Add 'user_type' to the list display and fieldsets
    list_display = UserAdmin.list_display + ('user_type',)
    fieldsets = UserAdmin.fieldsets + (
        (('User Type', {'fields': ('user_type',)}),)
    )
    # If you want to add profile_pic to the admin form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (('Additional Info', {'fields': ('user_type', 'profile_pic')}),)
    )

# Unregister the default User model if it's there (optional, but good practice if you only use CustomUser)
# from django.contrib.auth.models import User
# admin.site.unregister(User) # Only if you want to ensure the default User is never shown

# Register your CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)