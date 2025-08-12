# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from students.models import Student
from staff.models import Staff

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created: # If a new CustomUser is created
        if instance.user_type == 'student':
            # Create a Student profile only if one doesn't exist already (e.g., from admin manual entry)
            Student.objects.get_or_create(admin=instance)
            # You might want to log this or add a message for debugging
            # print(f"Auto-created Student profile for {instance.username}")
        elif instance.user_type == 'staff':
            # Create a Staff profile only if one doesn't exist
            Staff.objects.get_or_create(admin=instance)
            # print(f"Auto-created Staff profile for {instance.username}")
    else: # If an existing CustomUser is updated
        # This part ensures that if user_type changes, the correct profile exists
        if instance.user_type == 'student':
            Student.objects.get_or_create(admin=instance)
            # If changing from staff, ensure staff profile is not orphaned if not used by anything else
            # (Requires more complex logic if profiles need to be deleted automatically on type change)
        elif instance.user_type == 'staff':
            Staff.objects.get_or_create(admin=instance)
        # If user_type is admin, no linked profile is usually needed, so no action here.


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # This signal receiver is typically used to save related profiles
    # if they are managed directly as attributes of the CustomUser.
    # For OneToOneField, the get_or_create in create_user_profile handles this.
    pass # No explicit save needed here given how create_user_profile is structured