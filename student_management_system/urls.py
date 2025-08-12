# student_management_system/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from core import views as core_views # Ensure core_views is imported
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom Login, Signup, and Logout paths
    path('accounts/login/', core_views.custom_login_view, name='login'),
    path('', RedirectView.as_view(url='accounts/login/', permanent=False), name='home'),
    path('signup/', core_views.signup_view, name='signup'),
    path('logout/', core_views.custom_logout_view, name='logout'),

    # Django's built-in authentication URLs (includes password reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # Dashboards for different user types
    path('admin_dashboard/', core_views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', core_views.staff_dashboard, name='staff_dashboard'),
    path('student_dashboard/', core_views.student_dashboard, name='student_dashboard'),

    # --- CRUCIAL: Ensure these lines for user approval are present and uncommented! ---
    path('admin/pending_users/', core_views.manage_pending_users, name='manage_pending_users'),
    path('admin/approve_user/<int:user_id>/', core_views.approve_user, name='approve_user'),
    # ----------------------------------------------------------------------------------

    # Include URLs from your apps
    path('courses/', include('courses.urls')),
    path('staff/', include('staff.urls')),
    path('students/', include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('results/', include('results.urls')),
    path('feedback/', include('feedback_app.urls')),
    path('leave/', include('leave_app.urls')),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)