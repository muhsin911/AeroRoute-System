from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Define the main URL patterns for this Django project
urlpatterns = [
    # The Django admin site available at /admin/
    path("admin/", admin.site.urls),

    # All routes for the 'routes' app, included and namespaced under ''
    # This means the root URL ('/') loads 'routes.urls' and all its definitions
    path('', include('routes.urls', namespace='routes')),
]

# In development mode, append additional url patterns to serve user-uploaded media files
# This enables requests to MEDIA_URL (like /media/filename.jpg) to serve files from MEDIA_ROOT
# (Production should use a proper web server for this instead)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
