"""
URL configuration for aquafill_project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

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
