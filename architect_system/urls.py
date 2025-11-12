
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def root_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', root_redirect),
    path('admin/', admin.site.urls),
    path('accounts/', include('app.accounts.urls')),
    path('dashboard/', include('app.dashboard.urls')),
    path('architects/', include('app.architects.urls')),
    path('notifications/', include('app.notifications.urls', namespace='notifications')),
    path('payments/', include('app.payments.urls', namespace='payments')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])