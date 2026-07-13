from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Standard django admin (renamed for safety)
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('trips/', include('trips.urls')),
    path('destinations/', include('destinations.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('adminpanel/', include('adminpanel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
