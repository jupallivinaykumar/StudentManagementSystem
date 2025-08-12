from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("student", "Student"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Add related_name to resolve clashes with Django's default User model's reverse accessors
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set", # Unique related_name
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="customuser_permissions_set", # Unique related_name
        related_query_name="customuser",
    )

    def __str__(self):
        return self.username