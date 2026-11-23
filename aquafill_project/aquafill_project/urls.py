"""
URL configuration for aquafill_project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

# Strictly restrict Django Admin access exclusively to the admin user
def _admin_only_has_permission(request):
    return (
        request.user.is_active
        and request.user.is_authenticated
        and (request.user.username == 'admin' or (request.user.is_staff and request.user.is_superuser))
    )

admin.site.has_permission = _admin_only_has_permission

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root redirects to login screen
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # AquaFill Vertical Slices
    path('', include('authentication.urls')),
    path('home/', include('home.urls')),
    path('profile/', include('user_profile.urls')),
    path('settings/', include('user_settings.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
