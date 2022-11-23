from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('main/admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path('leader/', include('leader.urls', namespace='leader')),
    path('worker/', include('worker.urls', namespace='worker')),
    path('admin/', include('admin_dashboard.urls', namespace='admin_dashboard')),
    path('payments/', include('payments.urls', namespace='payments')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)